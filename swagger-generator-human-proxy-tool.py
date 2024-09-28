from openapi_spec_validator.readers import read_from_filename
from openapi_spec_validator import validate
from autogen import register_function
from autogen import ConversableAgent
import mammoth
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

def save_yaml_to_file(yaml_content_as_dictionary: dict, file_path: str) -> str:
    """
    Saves YAML content to a file.
    
    Args:
    yaml_content_as_dictionary (dict): The YAML content as a Python dictionary.
    file_path (str): The path to the file where the YAML content will be saved.
    
    Returns:
    str: A success message if the file is saved successfully, or an error message if not.
    """
    if not isinstance(yaml_content_as_dictionary, dict):
        return "Error: yaml_content_as_dictionary must be a dictionary"

    if not file_path.endswith('.yml') and not file_path.endswith('.yaml'):
        return "Error: File must have a .yml or .yaml extension"

    try:
        with open(file_path, 'w') as file:
            yaml.dump(yaml_content_as_dictionary, file, default_flow_style=False)
        return f"YAML content saved to {file_path} successfully"
    except yaml.YAMLError as e:
        return f"Error parsing YAML content: {e}"
    except IOError as e:
        return f"Error saving YAML content to file: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

def validate_swagger_or_openapi_file(file_path: str) -> str:
    """
    Validates a Swagger or OpenAPI file.
    
    Args:
    file_path (str): The path to the file to be validated.
    
    Returns:
    str: A success message if the file is valid, or an error message indicating what's wrong.
    """
    try:
        spec_dict, _ = read_from_filename(file_path)
        validate(spec_dict)
        return f"Swagger/OpenAPI file {file_path} is valid"
    except Exception as e:
        return f"Error: {e}"
    except yaml.YAMLError as e:
        return f"Error parsing YAML file: {e}"
    except IOError as e:
        return f"Error reading file: {e}"

def convert_word_to_markdown(docx_path: str) -> str:
    """
    Converts a Word document to a markdown file.
    
    Args:
    docx_path (str): The path to the Word document to be converted.
    
    Returns:
    str: A success message if the conversion is successful, including the path of the created README file.
    """
    try:
        # Get the base name of the input file and change the extension
        base_name = os.path.splitext(docx_path)[0]
        readme_path = f"{base_name}.md"

        # Convert Word document to Markdown
        with open(docx_path, "rb") as docx_file:
            # Use mammoth to convert the document to markdown
            result = mammoth.convert_to_markdown(docx_file)
            markdown = result.value

        # Write the converted markdown to the README file
        with open(readme_path, 'w', encoding='utf-8') as readme_file:
            readme_file.write(markdown)

        # Return a success message with the path of the created file
        return f"README file created successfully at {readme_path}"

    except IOError as e:
        # Handle file reading/writing errors
        return f"Error reading/writing file: {e}"
    except mammoth.DocumentConversionError as e:
        # Handle mammoth conversion errors
        return f"Error converting document: {e}"
    except Exception as e:
        # Handle any other unexpected errors
        return f"Unexpected error occurred: {e}"

def get_last_message(message_history:str) -> str:
    """
    A tool to get the last message in the conversation.
    
    :param message_history: The full message history of the conversation
    :return: The content of the last message
    """
    if message_history:
        last_message = message_history[-2]  # -2 because -1 is the current tool call
        return f"Last message: {last_message['role']}: {last_message['content']}"
    else:
        return "No previous messages found."

swagger_agent_system_message = """
You are a assistant. You generate the documenation and specifications in YML.

Return 'TERMINATE' when the conversion is done or you can't complete the task.
"""

swagger_agent= ConversableAgent(
    name="Swagger_Agent",
    system_message=swagger_agent_system_message,
    llm_config={"config_list": [{"model": "gpt-4o", "temperature": 0 ,"api_key": os.environ["OPENAI_API_KEY"]}]},
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
)

user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

# swagger_agent.register_for_llm(name="print_file_content", description="Print the content of a file.")(print_file_content)
# swagger_agent.register_for_llm(name="save_yaml_to_file", description="Saves YAML content to a file.")(save_yaml_to_file)
# swagger_agent.register_for_llm(name="validate_swagger_or_openapi_file", description="Validates a Swagger or OpenAPI YAML file.")(validate_swagger_or_openapi_file)
# swagger_agent.register_for_llm(name="convert_word_to_markdown", description="Converts a Word document to a markdown file.")(convert_word_to_markdown)

# user_proxy.register_for_execution(name="print_file_content")(print_file_content)
# user_proxy.register_for_execution(name="save_yaml_to_file")(save_yaml_to_file)
# user_proxy.register_for_execution(name="validate_swagger_or_openapi_file")(validate_swagger_or_openapi_file)
# user_proxy.register_for_execution(name="convert_word_to_markdown")(convert_word_to_markdown)

chat_result = user_proxy.initiate_chat(swagger_agent, message = "Give me a openapi spec example openapi specs in code blocks.", max_turns = 50)

print(chat_result.cost)
