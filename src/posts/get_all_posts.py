import json
import os
import boto3
from src.utils.functions import convert_to_json 

# Obtén el nombre de la tabla desde la variable de entorno
posts_table = os.environ['postsTable']

# Crea un cliente de DynamoDB
dynamodb = boto3.client('dynamodb')

def get_all_posts(event, context):
    try:
        # Realiza una operación de escaneo en la tabla DynamoDB para obtener todos los posts
        response = dynamodb.scan(TableName=posts_table)

        # Los resultados del escaneo se encuentran en la propiedad 'Items' de la respuesta
        posts = response.get('Items', [])

        # Convierte cada elemento de DynamoDB a JSON utilizando la función de conversión
        posts_json = [convert_to_json(item) for item in posts]

        return {
            "statusCode": 200,
            "body": json.dumps(posts_json)
        }

    except Exception as e:
        # En caso de error, retorna un código de estado HTTP 400
        return {
            "statusCode": 400,
            "body": json.dumps(f"Error al obtener posts: {str(e)}")
        }