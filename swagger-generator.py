import os

from autogen import ConversableAgent

import os

def print_md_file_content(path_to_file: str) -> str:
    """
    Returns the content of a markdown file.
    
    Args:
    path_to_file (str): The path to the markdown file.
    
    Returns:
    str: The content of the file if successful, or an error message if not.
    """
    if not path_to_file.endswith('.md'):
        return "Error: File must have a .md extension"

    try:
        with open(path_to_file, 'r') as file:
            return file.read()
    except IOError as e:
        return f"Error reading file: {e}"

swagger_agent_system_message = """
You are a swagger OpenApi documentation generator. You generate docs in YML.
Generate the yml in a markdown code block.
Return 'TERMINATE' when the conversion is done or you can't complete the task.
"""

swagger_agent= ConversableAgent(
    name="Swagger_Agent",
    system_message=swagger_agent_system_message,
    llm_config={"config_list": [{"model": "gpt-4o", "temperature": 0 ,"api_key": os.environ["OPENAI_API_KEY"]}]},
)

user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

swagger_agent.register_for_llm(name="print_md_file_content", description="Print the content of a markdown file.")(print_md_file_content)

user_proxy.register_for_execution(name="print_md_file_content")(print_md_file_content)

chat_result = user_proxy.initiate_chat(swagger_agent, message="Convert 'api.md' to openapi specs.")
