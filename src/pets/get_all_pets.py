import json
import os
import boto3
from src.utils.functions import convert_to_json 

# Obtén el nombre de la tabla desde la variable de entorno
pet_table = os.environ['petTable']

# Crea un cliente de DynamoDB
dynamodb = boto3.client('dynamodb')

def get_all_pets(event, context):
    try:
        # Realiza una operación de escaneo en la tabla DynamoDB para obtener todos los pets
        response = dynamodb.scan(TableName=pet_table)

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
            "body": json.dumps(f"Error al obtener pets: {str(e)}")
        }
