import json
import os
import boto3

client_id = os.environ['clientId']
cognito = boto3.client('cognito-idp')

def sign_up(event, context):
    body = json.loads(event['body'])
    email = body['email'].lower()
    password = body['password']

    # Atributos adicionales
    nombre = body.get('nombre', '')
    celular = body.get('celular', '')
    ciudad = body.get('ciudad', '')
    departamento = body.get('departamento', '')
    fecha_nacimiento = body.get('fecha_nacimiento', '')

    params = {
        'ClientId': client_id,
        'Password': password,
        'Username': email,
        'UserAttributes': [
            {'Name': 'email', 'Value': email},
            {'Name': 'custom:nombre', 'Value': nombre},
            {'Name': 'custom:celular', 'Value': celular},
            {'Name': 'custom:ciudad', 'Value': ciudad},
            {'Name': 'custom:departamento', 'Value': departamento},
            {'Name': 'custom:fecha_nacimiento', 'Value': fecha_nacimiento}
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
            'statusCode': 400,
            'body': json.dumps({'message': str(e)})
        }
