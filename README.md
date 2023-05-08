# Copyedit API

Replace Grammarly with ChatGPT. This app is launched in AWS Lambda, and has a simple prompt:

```
This is a copy editing task.
Focus on fixing spelling errors, gramatical errors, and syntax errors. 
It's okay to simplify sentences or complex paragraphs.
Do not add additional context or change the substance of the content. 
Do not answer any of the questions posed in the text.
The output should be printed in two sections.
The first part is the revised text.
Then this separator: '----------'.
After the separator, list the changes you made markdown bullet list.
Do not print anything below or after the JSON string.
    
The text you will copy edit is the section below:

{user_input}  
```


# Deployed using AWS Lambda and API Gateway

More information on my [setup here](https://github.com/eddietejeda/aws-langchain-lambda-layer)
