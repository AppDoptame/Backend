import json
from openai import OpenAI

def thread(event, context):
    # Assuming client is initialized
    client = OpenAI(api_key='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')
    thread = client.beta.threads.create()
    thread_dict = {
        "id": thread.id,
        "created_at": thread.created_at,
        "metadata": thread.metadata,
        "object": thread.object,
    }

    return { 
        'statusCode': 200,
        'body': json.dumps(thread_dict)
    }
