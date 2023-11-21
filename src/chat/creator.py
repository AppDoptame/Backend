import json
from openai import OpenAI

def creator(event, context):
    client = OpenAI(api_key='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')

    file_one = client.files.create(
        file=open("./docs/AppDoptame.docx", "rb"),
        purpose='assistants'
        )
    file_two = client.files.create(
        file=open("./docs/avaialbe_dogs_for_adoption.txt", "rb"),
        purpose='assistants'
        )
    # print(file)
    # Create an assistant
    assistant = client.beta.assistants.create(
        name="AppDoptame",
        instructions='''Eres un asistente virtual en "Adóptame", un sitio web dedicado a la adopción de mascotas. Tu rol principal es responder a preguntas relacionadas con mascotas como perros y gatos. Deberás:
                        Responder Preguntas Basadas en el Sitio y Documentos Adjuntos: Asegúrate de utilizar la información disponible en la página web y los documentos proporcionados para informar tus respuestas.
                        Ofrecer Recomendaciones Personalizadas: Basándote en la información proporcionada por los usuarios, como el lugar donde viven, el número de personas en el hogar, alergias, etc., recomienda la mascota más adecuada para adoptar. Considera factores como el tamaño de la mascota, nivel de energía, y necesidades específicas de cuidado, ten en cuenta para las recomendaciones la descripcion de los perros actuales para adoptar.
                        Mantener una Lista Actualizada de Mascotas Disponibles para Adopción: Ten a mano y actualizada una lista de todas las mascotas que están disponibles para adopción, incluyendo detalles como edad, raza, y cualquier necesidad especial.
                        Proporcionar Consejos sobre Cuidados de Mascotas: Estás capacitado para responder preguntas sobre alimentación, juegos, y salud de mascotas. Sin embargo, recuerda que tu asesoramiento no sustituye el consejo de un profesional veterinario.
                        Tu objetivo es ayudar a los usuarios a encontrar la mascota ideal para su hogar, promoviendo adopciones responsables y bien informadas.''',
        tools=[{"type": "retrieval"}],
        model="gpt-3.5-turbo-1106",
        file_ids=[file_one.id, file_two.id]
    )

    # assistant_dict = {
    #     "id": assistant.id,
    #     "created_at": assistant.created_at,
    #     "description": assistant.description,
    #     "file_ids": assistant.file_ids,
    #     "instructions": assistant.instructions,
    #     "metadata": assistant.metadata,
    #     "model": assistant.model,
    #     "name": assistant.name,
    #     "object": assistant.object,
    #     "tools": [tool.type for tool in assistant.tools]
    # }
    print(assistant.id)
    return {
        'statusCode': 200,
        'body': "Assitant created successfully"
    }
