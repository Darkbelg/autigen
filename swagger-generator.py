import os

from autogen import ConversableAgent

import os

def print_md_file_content(path):
    if not path.endswith('.md'):
        raise ValueError("File must have a .md extension")

    try:
        with open(path, 'r') as file:
            file_content = file.read()
            print(file_content)
    except IOError as e:
        print(f"Error reading file: {e}")


swagger_agent= ConversableAgent(
    name="Swagger_Agent",
    system_message="You are a swagger OpenApi documentation generator. You generate docs in YML. Generate the yml in a markdown code block. Return 'TERMINATE' when the task is done.",
    llm_config={"config_list": [{"model": "gpt-4o", "temperature": 0 ,"api_key": os.environ["OPENAI_API_KEY"]}]},
)

user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)


reply = swagger_agent.generate_reply(messages=[{"content": "Generate swagger documentation based on the url https://example.test/pet/{petId}/uploadImage response 200 petId  id de pet id abd file should be formdata.", "role": "user"}])

print(reply)
