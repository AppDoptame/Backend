import json
from openai import OpenAI
import time



def add_message(event, context):
    # Extract message and thread ID from event
    client = OpenAI(api_key='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')
    body = json.loads(event["body"])
    user_input = body['message']
    thread_id = body['thread_id']

    thread_message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input
    )

#     thread_message_dict = {
#     "id": thread_message.id,
#     "assistant_id": thread_message.assistant_id,
#     "content": [
#         {
#             "text": content.text.value,
#             "type": content.type
#         } for content in thread_message.content
#     ],
#     "created_at": thread_message.created_at,
#     "file_ids": thread_message.file_ids,
#     "metadata": thread_message.metadata,
#     "object": thread_message.object,
#     "role": thread_message.role,
#     "run_id": thread_message.run_id,
#     "thread_id": thread_message.thread_id
# }

    # print(thread_message_dict)

    # assistant_id = body['assistant_id']

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id="asst_Ad0jBD3sHZEcaMcsHhcu57oV",
        # instructions="Please address the user as Jane Doe. The user has a premium account."
    )
    # print(run)

    
    run_completed = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run.id
    )
    estado_peticion = run_completed.status

    while estado_peticion != "completed":
        run_completed = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        estado_peticion = run_completed.status
        print(estado_peticion)
        if(estado_peticion=="cancelling" or estado_peticion=="cancelled" or estado_peticion=="expired" or estado_peticion=="requires_action" or estado_peticion=="failed"):
            codigo_error = run_completed.last_error.code
            # if codigo_error == "rate_limit_exceeded":
                # time.sleep(21)
                # continue
            # print(codigo_error)
            mensaje_error = run_completed.last_error.message
            # print(mensaje_error)
            return {
                'statusCode': 429, #Too many requests
                # 'body': json.dumps(messages)
                'body': "Ocurrio un error: "+ mensaje_error
            }
        time.sleep(3)

    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    # print(messages)

    # for i in messages:
    #     print(i)

    response_message = messages.data[0]
    response_message = response_message.content[0].text.value


    return {
        'statusCode': 200,
        # 'body': json.dumps(messages)
        'body': (response_message)
    }