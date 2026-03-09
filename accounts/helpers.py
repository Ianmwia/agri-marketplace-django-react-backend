import requests
from decouple import config

def normalize_phone_number(phone):
    phone = phone.strip()
    if phone.startswith('+'):
        phone = phone[1:]
    if phone.startswith('0'):
        phone ='254' + phone[1:]
    elif not phone.startswith('254'):
        phone = '254' + phone
    return phone

#text bee send sms
def send_free_sms(phone, message):
    clean_phone = normalize_phone_number(phone)

    BASE_URL = 'https://api.textbee.dev/api/v1'
    API_KEY = config("TEXTBEE_API_KEY")
    DEVICE_ID = config('TEXTBEE_DEVICE_ID')

    response = requests.post(
    f'{BASE_URL}/gateway/devices/{DEVICE_ID}/send-sms',
    json={
        'recipients': [clean_phone],
        'message': message
    },
    headers={'x-api-key': API_KEY}
    )
    print(f'SMS Response Status: {response.status_code}')
    print(f'SMS Response Body: {response.text}')

    print(response.json())