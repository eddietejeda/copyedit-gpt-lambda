# Copyedit API

Replace Grammarly with ChatGPT. This app is launched in AWS Lambda, and has a simple prompt:


> Lightly copy edit the section below, but do not change the substance of the content. Keep track of the changes you made. The output will be in a JSON string format.The JSON will include the revised text in the "revision" field and the changes you made will be the "changes" field using markdown bullet lists. Do not print any other text below or after the JSON string.


# Deployed using AWS Lambda and API Gateway

More information on my [setup here](https://github.com/eddietejeda/aws-langchain-lambda-layer)
