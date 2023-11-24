from infobip_channels.sms.channel import SMSChannel
from django.conf import settings

BASE_URL = settings.BASE_URL_INFOBIP
API_KEY = settings.API_KEY_INFOBIP

def send_verification_phone_number(code, phone_number):
    channel = SMSChannel.from_auth_params(
        {
            "base_url": BASE_URL,
            "api_key": API_KEY,
        }
    )

    sms_response = channel.send_sms_message(
        {
            "messages": [
                {
                    "destinations": [{"to": str(phone_number)}],
                    "text": f"Ваш код: {code}",
                }
            ]
        }
    )

    query_parameters = {"limit": 10}
    delivery_reports = channel.get_outbound_sms_delivery_reports(query_parameters)
    return delivery_reports