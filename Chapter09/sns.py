import os
import re
import boto3


class QuoteSubscription:

    def __init__(self):
        """
        Class constructor to initialize the boto3 configuration with Amazon SNS.
        """
        self.client = boto3.client(
            'sns',
            aws_access_key_id=os.environ['aws_access_key_id'],
            aws_secret_access_key=os.environ['aws_secret_access_key'],
            region_name='us-east-1')
        topic = self.client.create_topic(Name="DailyQuoteSubscription")
        self.topic_arn = topic['TopicArn']


    def subscribe(self, mobile):
        """
        This method is used to subscribe a mobile number to the Amazon SNS topic.
        Required parameters:
            :param mobile: A mobile number along with country code.
            Syntax - <country_code><mobile_number>
            Example - 919028XXXXXX
        """
        assert(bool(re.match("^(\+\d{1,3}?)?\d{10}$", mobile))), 'Invalid mobile number'
        self.client.subscribe(
            TopicArn=self.topic_arn,
            Protocol='sms',
            Endpoint=mobile,
        )


    def unsubscribe(self, mobile):
        """
        This method is used to unsubscribe a mobile number from the Amazon SNS topic.
        Required parameters:
            :param mobile: A mobile number along with country code.
            Syntax - <country_code><mobile_number>
            Example - 919028XXXXXX
        """
        assert(bool(re.match("^(\+\d{1,3}?)?\d{10}$", mobile))), 'Invalid mobile number'
        try:
            subscriptions = self.client.list_subscriptions_by_topic(TopicArn=self.topic_arn)
            subscription = list(filter(lambda x: x['Endpoint']==mobile, subscriptions['Subscriptions']))[0]
            self.client.unsubscribe(
                SubscriptionArn= subscription['SubscriptionArn']
            )
        except IndexError:
            raise ValueError('Mobile {} is not subscribed.'.format(mobile))


    def publish(self, message):
        """
        This method is used to publish a quote message on Amazon SNS topic.
        Required parameters:
            :param message: string formated data.
        """
        self.client.publish(Message=message, TopicArn=self.topic_arn)


    def send_sms(self, mobile_number, message):
        """
        This method is used to send a SMS to a mobile number.
        Required parameters:
            :param mobile_number: string formated data.
            :param message: string formated data.
        """
        self.client.publish(
            PhoneNumber=mobile_number,
            Message=message
        )