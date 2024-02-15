from openai import OpenAI
import time

def create_openai_client(api_key):
    client = OpenAI(api_key = api_key)
    return client

def wait_on_run(client, run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

def ai_compare_files(client, assistant_instructions: str, schema_input: str) -> str:
    assistant = client.beta.assistants.create(
        name = "schemahelper",
        instructions = assistant_instructions,
        model="gpt-4-turbo-preview"
    )

    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content = schema_input
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    run = wait_on_run(client, run, thread)

    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    output_string = 'Schema AI Response:\n\n'
    for message_output in messages.data:
        output_string = output_string + str(message_output.content[0].text.value) + '\n'
    
    response = client.beta.assistants.delete(assistant.id)

    return output_string