from openapi_spec_validator import validate_spec,OpenAPIV30SpecValidator
from openapi_spec_validator.readers import read_from_filename
from autogen import ConversableAgent, UserProxyAgent
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

# Configuration for the language model
config_list = [
    {
        "model": "gpt-4o",
        "api_key": os.environ.get("OPENAI_API_KEY"),
        "cache_seed": None,
    }
]

# Create a user proxy agent
user_proxy = UserProxyAgent(
    name="User",
    llm_config=False,
    human_input_mode="NEVER",
    code_execution_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
)

openapi_generator_system_message = """
    You are an expert in creating OpenAPI specifications.
    When asked to generate or fix a 3.0.x OpenAPI spec, provide it in a YAML code block. 
    The YAML code block will be saved in a file called openapi.yml.
    ONLY ONE CODE BLOCK PER ANSWER. Or you will get stuck in an infinite loop.
    
    1. Print the given markdown file.
    2. Generate a 3.0.x OpenAPI spec YAML code block with the functional specs of the markdown file. Before validating the file. If the file doesn't exist you can't validate it.
    3. Validate the file generated.
    4. If there is an error. Think through the error, reflect and fix the error.
    
    When finished end your message with TERMINATE.
"""

# Create an assistant agent for OpenAPI generation
openapi_generator = ConversableAgent(
    name="OpenAPIGenerator",
    system_message=openapi_generator_system_message,
    llm_config={"config_list": config_list},
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
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

def process_message_before_send_and_extract_yaml(sender,message,recipient,silent):
    print('process_message_before_send_and_extract_yaml')
    # for message in messages:
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
openapi_generator.register_for_llm(name="validate_openapi_file", description="Validates an OpenAPI file.")(validate_openapi_file)

user_proxy.register_for_execution(name="print_file_content")(print_file_content)
user_proxy.register_for_execution(name="validate_openapi_file")(validate_openapi_file)

# Initiate the chat
chat_result = user_proxy.initiate_chat(
    openapi_generator,
    message="Create specs from petstore.md.",
    max_turns = 10
)

print(chat_result.cost)


# for result in chat_result:
    # print(result.cost)

## Get the last message from the conversation
#last_message = user_proxy.last_message()

# # Check if the last message contains a YAML block and save it
# if "```yaml" in last_message["content"] and "```" in last_message["content"].split("```yaml", 1)[1]:
#     yaml_content = last_message["content"].split("```yaml", 1)[1].split("```", 1)[0].strip()
#     save_yaml_to_file(yaml_content)

# openapi_generator.register_for_llm(name="validate_openapi_file", description="Validates a  or OpenAPI YAML file.")(validate_openapi_file)

# user_proxy.register_for_execution(name="validate_openapi_file")(validate_openapi_file)

# # openapi_generator.system_message = openapi_generator_system_message

# user_proxy.initiate_chat(
#     openapi_generator,
#     message="Validate the spec openapi.yml. If there is an error print the content and fix it.",
#     max_turns = 10
# )

# # Get the last message from the conversation
# last_message = user_proxy.last_message()

# # Check if the last message contains a YAML block and save it
# if "```yaml" in last_message["content"] and "```" in last_message["content"].split("```yaml", 1)[1]:
#     yaml_content = last_message["content"].split("```yaml", 1)[1].split("```", 1)[0].strip()
#     save_yaml_to_file(yaml_content)

