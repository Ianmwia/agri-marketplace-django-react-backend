from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
import requests
import base64
import stripe
from datetime import datetime
from django.conf import settings
from .models import MpesaRequest, MpesaResponse, MpesaCallBack
from .serializers import MpesaRequestSerializer, MpesaResponseSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from orders.models import Order
from accounts.helpers import normalize_phone_number
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
@api_view(['post'])
@permission_classes([IsAuthenticated])
def stk_push(request):
    serializer = MpesaRequestSerializer(data=request.data)
    if serializer.is_valid():
        mpesa_request = serializer.save()
        response_data = initialize_stk_push(mpesa_request)
        #print(f"DEBUG SAFARICOM RESPONSE: {response_data}")
        mpesa_response = MpesaResponse.objects.create(
            request = mpesa_request,
            merchant_request_id = response_data.get('MerchantRequestID', ''),
            checkout_request_id = response_data.get('CheckoutRequestID', ''),
            response_code = response_data.get('ResponseCode', ''),
            response_description = response_data.get('ResponseDescription', ''),
            customer_message = response_data.get('CustomerMessage', ''),
            #timestamp = response_data.get('TimeStamp', ''),
        )
        if response_data.get('ResponseCode') == '0':
            return Response(MpesaResponseSerializer(mpesa_response).data)#201
        return Response(response_data)#400

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def initialize_stk_push(mpesa_request):
    access_token = get_access_token()
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = generate_password(timestamp)

    headers = {
        "Authorization": f'Bearer {access_token}'
    }
    payload = {
        "Password": password,
        "BusinessShortCode": settings.MPESA_EXPRESS_SHORTCODE,
        "Timestamp": timestamp,
        "Amount": int(mpesa_request.amount),
        "PartyA": normalize_phone_number(mpesa_request.phone_number),
        "PartyB": settings.MPESA_EXPRESS_SHORTCODE,
        "TransactionType": "CustomerPayBillOnline",
        "PhoneNumber": normalize_phone_number(mpesa_request.phone_number),
        "TransactionDesc": mpesa_request.transaction_description,
        "AccountReference": mpesa_request.account_reference,
        "CallBackURL": "https://abc12345.ngrok-free.app/api/mpesa/callback"
        }
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def get_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(api_url, auth=(consumer_key, consumer_secret))
    access_token = response.json().get('access_token')
    return access_token

def generate_password(timestamp):
    shortcode = settings.MPESA_EXPRESS_SHORTCODE
    passkey = settings.MPESA_PASSKEY
    #timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = shortcode + passkey + timestamp
    encoded_string = base64.b64encode(data_to_encode.encode())
    return encoded_string.decode('utf-8')

@api_view(['post'])
@permission_classes([AllowAny])
def mpesa_callback(request):
    data = request.data.get('Body', {}).get('stkCallBack', {})
    result_code = data.get('ResultCode')
    checkout_id = data.get('CheckoutRequestID')

    if result_code == 0:
        try:
            mpesa_res = MpesaResponse.objects.get(checkout_request_id=checkout_id)
            order = mpesa_res.request.order
            
            order.status = 'paid'
            order.save()

            #reduce stock
            #batch = order.batch
            #batch.quantity -= order.quantity
            #batch.save()

            return Response({'ResultDesc': 'Success'})
        except Order.DoesNotExist:
            return Response({'ResultDesc':'Order not found'})
    return Response({'ResultDescription':'Payment Failed'})

# use stripe webhook metadata to not create a serializer
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def stripe_checkout(request):
    try:
        order = Order.objects.get(id=request.data.get('order_id'))

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data':{
                    'currency': 'kes',
                    'product_data': {'name': f"Order #{order.id}"},
                    'unit_amount': int(order.total_price *100)
                },
                'quantity': 1
            }],
            mode='payment',
            success_url='https://agri-marketplace-app-react.vercel.app/market',
            cancel_url='https://agri-marketplace-app-react.vercel.app/market',
            metadata={'order_id': order.id} # save the id in stripe
        )
        return Response({'url': session.url}, status=status.HTTP_200_OK) #200ok
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
#allow stripe access without token
@api_view(['POST'])
@permission_classes([AllowAny])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        return Response(status=400)
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session['metadata']['order_id']

        #update order model
        order = Order.objects.get(id=order_id)
        order.status = 'paid'
        order.save()

    return Response(status=200)