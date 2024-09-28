from openapi_spec_validator import validate_spec,OpenAPIV30SpecValidator
from openapi_spec_validator.readers import read_from_filename
from autogen import ConversableAgent, UserProxyAgent
from autogen import GroupChat, GroupChatManager
import yaml
import os


def validate_openapi_file(file_path: str) -> str:
    """
    Validates an OpenAPI file.
    
    Args:
    file_path (str): The path to the file to be validated.
    
    Returns:
    str: A success message if the file is valid, or an error message indicating what's wrong.
    """
    try:
        spec_dict, _ = read_from_filename(file_path)
        validate_spec(spec_dict, cls=OpenAPIV30SpecValidator)
        
        # If we reach this point, the file is valid
        return f"Success: The OpenAPI 3.0 file '{file_path}' is valid."
    
    except yaml.YAMLError as e:
        return f"Error: Unable to parse YAML in '{file_path}'. Details: {str(e)}"
    
    except IOError as e:
        return f"Error: Unable to read file '{file_path}'. Details: {str(e)}"
    
    except Exception as e:
        return f"Error: Validation failed for '{file_path}'. Details: {str(e)}"

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

openapi_generator_system_message = """
You are an expert in creating OpenAPI specifications.
When asked to generate or fix a 3.0.x OpenAPI spec, provide it in a YAML code block. 
The YAML code block will be saved in a file called openapi.yml.
ONLY ONE CODE BLOCK PER ANSWER. Or you will get stuck in an infinite loop.

Take the feedback of OpenAPIReviewer.
Print the openapi.yml
Write out the FULL corrected yml in one code block.
"""

openapi_reviewer_system_message = """
You are a helpful AI assistant.

You look for issues between the the functional specifications in petstore.md and the openapi specifications in openapi.yml.

Print the markdown file and the openapi.yml.

Tell OpenAPIGenerator where the issue is and what to fix.

Make this into a table in markdown.

Reply 'NO_ISSUES' in the end when everything is done.
"""

# Configuration for the language model
config_list = [
    {
        "model": "gpt-4o",
        "api_key": os.environ.get("OPENAI_API_KEY"),
        "cache_seed": None,
    }
]

# Create an assistant agent for OpenAPI generation
openapi_generator = ConversableAgent(
    name="OpenAPIGenerator",
    system_message=openapi_generator_system_message,
    llm_config={"config_list": config_list},
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: msg.get("content") is not None and "NO_ISSUES" in msg["content"],
)

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
)

# Function to save YAML content to a file
def save_yaml_to_file(content):
    with open('openapi.yml', 'w') as file:
        file.write(content)

def extract_and_save_yaml(message_content):
    print("extract_and_save_yaml")
    if "```yaml" in message_content and "```" in message_content.split("```yaml", 1)[1]:
        yaml_content = message_content.split("```yaml", 1)[1].split("```", 1)[0].strip()
        save_yaml_to_file(yaml_content)
        return True
    return False

def process_messages_and_extract_yaml(messages):
    print('process_messages_and_extract_yaml')
    for message in messages:
        if isinstance(message, dict) and "content" in message:
            extract_and_save_yaml(message["content"])
    return messages

def process_message_before_send_and_extract_yaml(sender, message, recipient, silent):
    if isinstance(message, dict) and "content" in message:
        if message["content"] is not None:
            extract_and_save_yaml(message["content"])
    else:
        extract_and_save_yaml(message)
    return message

# Register the hook for processing the last received message
openapi_generator.register_hook(
    hookable_method="process_message_before_send",
    hook=process_message_before_send_and_extract_yaml
)

openapi_generator.register_for_llm(name="print_file_content", description="Print the content of a file.")(print_file_content)
openapi_reviewer.register_for_llm(name="print_file_content", description="Print the content of a file.")(print_file_content)
openapi_generator.register_for_llm(name="validate_openapi_file", description="Validates an OpenAPI file.")(validate_openapi_file)

user_proxy.register_for_execution(name="print_file_content")(print_file_content)
user_proxy.register_for_execution(name="validate_openapi_file")(validate_openapi_file)

openapi_generator.description="Generates Open API specs."
openapi_reviewer.description="Review functional specification with the open api specifaction."
user_proxy.description="Has all the tools."

group_chat = GroupChat(
    agents=[openapi_generator, openapi_reviewer, user_proxy],
    messages=[],
    max_round=10,
)

group_chat_manager = GroupChatManager(
    groupchat=group_chat,
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
)

chat_result = openapi_reviewer.initiate_chat(
    openapi_generator,
    message="Start with printing the specifications",
    summary_method="reflection_with_llm",
)

print(chat_result.cost)
