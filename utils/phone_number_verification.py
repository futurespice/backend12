"""
Module for phone number verification
"""

import secrets

import jwt
from django.conf import settings
from django.utils import timezone
from twilio.rest import Client
from utils.infobip import send_verification_phone_number

from apps.accounts.models import CustomUser, PhoneNumberVerification


def send_phone_number_verification(user_id):
    """
    Create verification code and send it to user phone number
    """
    user = CustomUser.objects.get(id=user_id)
    code = generate_code()
    expiration = timezone.now() + timezone.timedelta(minutes=10)
    verification = PhoneNumberVerification.objects.create(
        code=code, user=user, expiration=expiration
    )
    send_verification_phone_number(code, user.phone_number)
    return verification


# def send_verification_phone_number(code, phone_number):
#     """
#     Send verification code to user phone number
#     """
#     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#     print(f"Отправка кода подтверждения на номер {phone_number}. Код: {code}")
#     message = client.messages.create(
#         to=f"{phone_number}",
#         from_=settings.TWILIO_SERVICE_SID,
#         body=f"Ваш код: {code}",
#     )

#     return message.sid


def generate_code():
    """
    Generate 4-digit code
    """
    return "".join([str(secrets.randbelow(10)) for _ in range(4)])


def generate_pre_2fa_token(user):
    """
    Generate token for pre 2fa auth
    """
    payload = {
        "id": user.id,
        "phone_number": str(user.phone_number),
        "pre_2fa_auth": True,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def get_user_by_token(token):
    """
    Get user by token
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = CustomUser.objects.get(id=payload["id"])
        return user
    except CustomUser.DoesNotExist:
        return None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.DecodeError:
        return None
    except jwt.InvalidTokenError:
        return None
