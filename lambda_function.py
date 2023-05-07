import os
import json
from langchain.llms import OpenAI
from langchain import PromptTemplate


def copyedit(user_input):

    llm = OpenAI(model_name="text-davinci-003")

    template = """
    Lightly copy edit the following text: {user_input}

    The output will be in a JSON string format, where the revised text will go in a 'revision' field, and the list of changes will go in the 'changes' field using markdown bullets syntax.
    """

    prompt = PromptTemplate(
        input_variables=["user_input"],
        template=template,
    )

    final_prompt = prompt.format(user_input=user_input)

    return json.loads(llm(final_prompt))
    

def lambda_handler(event, context):
    body = json.loads(event.get('body'))
    content = copyedit(body['user_input'])

    return {
        'statusCode': 200,
        'headers' : {
            'Content-Type': 'application/json'
        },
        'body': {
            'changes': content['changes'],
            'revision': content['revision']
        }
    }



if os.environ.get("ENV") == "development":
    openai_api_key = os.getenv("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    user_input = input("Enter your text: \n\n")
    event = {
        "user_input": user_input
    }

    response = lambda_handler(event)

    print(f"\n\nRevised text:\n\n{response['body']['revision']}\n\nChanges:\n{response['body']['changes']}")
