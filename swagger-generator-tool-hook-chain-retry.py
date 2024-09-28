from openapi_spec_validator import validate_spec,OpenAPIV30SpecValidator
from openapi_spec_validator.readers import read_from_filename
from autogen import ConversableAgent, UserProxyAgent
from autogen import GroupChat, GroupChatManager
import yaml
import os

def print_file_content(path_to_file: str) -> str:
    """
    Returns the content of a file.
    
    Args:
    path_to_file (str): The path to the file.
    
    Returns:
    str: The content of the file if successful, or an error message if not.
    """
    try:
        with open(path_to_file, 'r') as file:
            return file.read()
    except IOError as e:
        return f"Error reading file: {e}"

openapi_reviewer_system_message = """
You are a helpful AI assistant.

You look for issues between the the functional specifications in petstore.md and the openapi specifications in openapi.yml.
Functional specifications are leading.

1. Print the markdown file and the openapi.yml.
2. Reflect on each endpoint
3. Put everything in a nice table

BE STRICT just because it says in the description it's deprecated doesn't mean it isn't an issue attribute deprecated isn't set to yes.
If a url is missing that is an issue.
If a url is marked with a certain tag and it's missing that is an issue.
Check if auth is correct.

Reply 'NO_ISSUES' in the end when everything is done.
"""

# Configuration for the language model
config_list = [
    {
        "model": "gpt-4o",
        "api_key": os.environ.get("OPENAI_API_KEY"),
        "temperature": 0,
        "cache_seed": None,
    }
]

# Create a user proxy agent
openapi_reviewer = ConversableAgent(
    name="OpenAPIReviewer",
    system_message=openapi_reviewer_system_message,
    llm_config={"config_list": config_list},
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: msg.get("content") is not None and "NO_ISSUES" in msg["content"],
)

# Create a user proxy agent
user_proxy = UserProxyAgent(
    name="User",
    llm_config=False,
    human_input_mode="NEVER",
    code_execution_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "NO_ISSUES" in msg["content"],
)

openapi_reviewer.register_for_llm(name="print_file_content", description="Print the content of a file.")(print_file_content)

user_proxy.register_for_execution(name="print_file_content")(print_file_content)

chat_result = user_proxy.initiate_chat(
    openapi_reviewer,
    message="Review the functional specifications with the open api specifications.",
    max_turns = 10
)

print(chat_result.cost)
