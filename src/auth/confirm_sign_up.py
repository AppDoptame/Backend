import json
import os
import boto3

client_id = os.environ['clientId']
cognito = boto3.client('cognito-idp')

def confirm_sign_up(event, context):
    body = json.loads(event['body'])
    email = body['email'].lower()
    confirmation_code = body['confirmationCode']

    params = {
        'ClientId': client_id,
        'Username': email,
        'ConfirmationCode': confirmation_code
    }

    try:
        result = cognito.confirm_sign_up(**params)
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': str(e)})
        }