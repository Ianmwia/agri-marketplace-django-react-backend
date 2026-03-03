def normalize_phone_number(phone):
    phone = phone.strip()
    if phone.startswith('+'):
        phone = phone[1:]
    if phone.startswith('0'):
        phone ='254' + phone[1:]
    elif not phone.startswith('254'):
        phone = '254' + phone
    return phone
