import json
import os
import boto3
from src.utils.functions import convert_to_json 

# Obtén el nombre de la tabla desde la variable de entorno
pet_table = os.environ['petTable']

# Crea un cliente de DynamoDB
dynamodb = boto3.client('dynamodb')

def get_pets_by_email(event, context):
    # Obtiene el correo electrónico de los parámetros de la solicitud
    email = event['pathParameters']['email']

    try:
        # Realiza un escaneo en la tabla DynamoDB para buscar todas las mascotas con el mismo correo electrónico
        response = dynamodb.scan(
            TableName=pet_table,
            FilterExpression='email = :email',
            ExpressionAttributeValues={':email': {'S': email}},
            ProjectionExpression='id, #n, age, vaccines, race, adopted, sex, size, sterilized, images, city, department',
            ExpressionAttributeNames={'#n': 'name'}
        )

        # Los resultados del escaneo se encuentran en la propiedad 'Items' de la respuesta
        pets = response.get('Items', [])

        pets_json = [convert_to_json(item) for item in pets]

        return {
            "statusCode": 200,
            "body": json.dumps(pets_json)
        }

    except Exception as e:
        # En caso de error, retorna un código de estado HTTP 400
        return {
            "statusCode": 400,
            "body": json.dumps(f"Error al obtener mascotas por email: {str(e)}")
        }
