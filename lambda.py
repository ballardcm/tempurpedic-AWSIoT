import boto3
import json

client = boto3.client('iot-data', region_name='us-east-1')

def lambda_handler(event, context):
    response = client.publish(
        topic='bedcommands',
        qos=0,
        payload=str(event['bed_pos'])
    )
