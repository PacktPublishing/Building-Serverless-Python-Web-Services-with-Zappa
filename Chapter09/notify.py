import os
import boto3


def unhandled_exceptions(e, event, context):
    client = boto3.client('sns', aws_access_key_id=os.environ['aws_access_key_id'],
                            aws_secret_access_key=os.environ['aws_secret_access_key'],
                            region_name='us-east-1')
    topic = client.create_topic(Name="UnhandledException")
    client.publish(Message={'exception': e, 'event': event}, TopicArn=topic['TopicArn'])
    return True # Prevent invocation retry
