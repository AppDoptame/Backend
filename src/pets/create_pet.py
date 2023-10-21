import json
import os
import boto3
import uuid

# Obtén el nombre de la tabla desde la variable de entorno
pet_table = os.environ['petTable']

# Crea un cliente de DynamoDB
dynamodb = boto3.client('dynamodb')

def create_pet(event, context):
    body = json.loads(event["body"])

    email = body['email'].lower()
    name = body['name']
    age = body["age"]
    vaccines = body["vaccines"]
    race = body["race"]

    # Genera un ID único para la mascota
    pet_id = str(uuid.uuid4())

    # Define el objeto de ítem para la pet con el ID
    pet_item = {
    'id': {'S': pet_id},
    'email': {'S': email},
    'name': {'S': name},
    'age': {'N': str(age)},
    'vaccines': {'SS': vaccines}, 
    'race': {'S': race}
}

    try:
        # Intenta escribir el ítem en la tabla de DynamoDB
        dynamodb.put_item(TableName=pet_table, Item=pet_item)
        
        # Retorna una respuesta adecuada (por ejemplo, un código de estado HTTP 200) si tiene éxito
        response = {
            "statusCode": 200,
            "body": json.dumps("Pet creada exitosamente")
        }
    except Exception as e:
        # En caso de error, retorna un código de estado HTTP 400
        response = {
            "statusCode": 400,
            "body": json.dumps(f"Error al crear la pet: {str(e)}")
        }

    return response
