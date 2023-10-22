import json
import os
import boto3
import uuid
import datetime

# Obtén el nombre de la tabla desde la variable de entorno
posts_table = os.environ['postsTable']

# Crea un cliente de DynamoDB
dynamodb = boto3.client('dynamodb')

def create_post(event, context):
    body = json.loads(event["body"])
    print(body)
    if not body:
        return {
            "statusCode": 400,
            "body": json.dumps("Solicitud sin datos")
        }

    title = body['title']
    description = body['description']
    pet_id = body["pet_id"]
    email = body['email'].lower()
    images = body["images"]
    creation_date = datetime.date.today()


    # Genera un ID único para la mascota
    post_id = str(uuid.uuid4())

    # Define el objeto de ítem para la pet con el ID
    post_item = {
    'id': {'S': post_id},
    'title': {'S': title},
    'description': {'S': description},
    'email': {'S': email},
    'pet_id': {'S': pet_id},
    'creation_date': {'S': str(creation_date)},
    'images': {'SS': images}, 
}

    try:
        # Intenta escribir el ítem en la tabla de DynamoDB
        dynamodb.put_item(TableName=posts_table, Item=post_item)
        
        # Retorna una respuesta adecuada (por ejemplo, un código de estado HTTP 200) si tiene éxito
        response = {
            "statusCode": 200,
            "body": json.dumps("Post creado exitosamente")
        }
    except Exception as e:
        # En caso de error, retorna un código de estado HTTP 400
        response = {
            "statusCode": 400,
            "body": json.dumps(f"Error al crear la pet: {str(e)}")
        }

    return response
