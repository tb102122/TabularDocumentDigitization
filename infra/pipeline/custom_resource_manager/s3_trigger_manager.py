# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import boto3

client = boto3.session.Session(profile_name="cardess-dev").client
from os import getenv

S3Client = client('s3', region_name="eu-central-1")

TRIGGER_S3_ARN = getenv('TRIGGER_S3_ARN')
STORE_DOCUMENT = getenv('STORE_DOCUMENT')


def lambda_handler(event, context):

    print(event)

    request_type = event['RequestType']

    if request_type == 'Create': return on_create(event)
    if request_type == 'Update': return on_update(event)
    if request_type == 'Delete': return on_delete(event)

    raise Exception('Invalid Request Type: %s' % request_type)


def on_create(event):

    response = S3Client.put_bucket_notification_configuration(
        Bucket=STORE_DOCUMENT,
        NotificationConfiguration={
            'LambdaFunctionConfigurations': [{
                'LambdaFunctionArn':
                TRIGGER_S3_ARN,
                'Events': ['s3:ObjectCreated:acquire/']
            }]
        })


def on_update(event):

    response = S3Client.put_bucket_notification_configuration(
        Bucket=STORE_DOCUMENT,
        NotificationConfiguration={
            'LambdaFunctionConfigurations': [{
                'LambdaFunctionArn':
                TRIGGER_S3_ARN,
                'Events': ['s3:ObjectCreated:acquire/']
            }]
        })


def on_delete(event):

    response = S3Client.put_bucket_notification_configuration(
        Bucket=STORE_DOCUMENT,
        NotificationConfiguration={'LambdaFunctionConfigurations': []})
