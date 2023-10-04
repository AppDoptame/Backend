import json
import os
import boto3

client_id = os.environ['clientId']
cognito = boto3.client('cognito-idp')

def sign_up(event, context):
    body = json.loads(event['body'])
    email = body['email'].lower()
    password = body['password']

    params = {
        'ClientId': client_id,
        'Password': password,
        'Username': email,
        'UserAttributes': [
          {'Name': 'given_name', 'Value': 'John'},  # Nombre del usuario
          {'Name': 'family_name', 'Value': 'Doe'}  # Apellido del usuario
      ]
    }

    try:
        result = cognito.sign_up(**params)
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except Exception as e:
        return {
            'statusCode': e.response['ResponseMetadata']['HTTPStatusCode'],
            'body': json.dumps({'message': str(e)})
        }
