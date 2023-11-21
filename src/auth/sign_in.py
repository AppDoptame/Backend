import json
import os
import boto3

client_id = os.environ['clientId']
user_pool_id = os.environ['userPoolId']
cognito = boto3.client('cognito-idp')

def sign_in(event, context):
    body = json.loads(event["body"])

    email = body['email'].lower()
    password = body["password"]

    try:
        response = cognito.admin_initiate_auth(
            AuthFlow="ADMIN_NO_SRP_AUTH",
            UserPoolId=user_pool_id,
            ClientId=client_id,
            AuthParameters={"USERNAME": email, "PASSWORD": password}
        )

    except Exception as e:
        return {
            'statusCode':  400,
            'body': json.dumps({'message': str(e)})
        }

    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                "access_token": response["AuthenticationResult"]["IdToken"],
                "refresh_token": response["AuthenticationResult"]["RefreshToken"],
                "expires_in": response["AuthenticationResult"]["ExpiresIn"],
                "token_type": response["AuthenticationResult"]["TokenType"],
            }
        )
    }
