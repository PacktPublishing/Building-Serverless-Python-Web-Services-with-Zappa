import random
from zappa.async import task
from sns import QuoteSubscription
from models import OTPModel


@task
def async_subscribe(mobile_number):
    quote_subscription = QuoteSubscription()
    quote_subscription.subscribe(mobile=mobile_number)


@task
def async_unsubscribe(mobile_number):
    quote_subscription = QuoteSubscription()
    quote_subscription.unsubscribe(mobile=mobile_number)


@task
def async_publish(message):
    quote_subscription = QuoteSubscription()
    quote_subscription.publish(message=message)


@task
def async_send_otp(mobile_number):
    otp = None
    quote_subscription = QuoteSubscription()
    data = OTPModel.select().where(OTPModel.mobile_number == mobile_number, OTPModel.is_verified == False)
    if data.exists():
        data = data.get()
        otp = data.otp
    else:
        otp = random.randint(1000,9999)
        OTPModel.create(**{'mobile_number': mobile_number, 'otp': otp})
    message = "One Time Password (OTP) is {} to verify the Daily Quote subscription.".format(otp)
    quote_subscription.send_sms(mobile_number=mobile_number, message=message)
