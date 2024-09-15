import os

from autogen import ConversableAgent
import yaml


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

def save_yaml_to_file(yaml_content: str, file_path: str) -> str:
    """
    Saves YAML content to a file.
    
    Args:
    yaml_content (str): The YAML content to be saved.
    file_path (str): The path to the file where the YAML content will be saved.
    
    Returns:
    str: A success message if the file is saved successfully, or an error message if not.
    """
    if not file_path.endswith('.yml') and not file_path.endswith('.yaml'):
        return "Error: File must have a .yml or .yaml extension"

    try:
        with open(file_path, 'w') as file:
            yaml.dump(yaml.load(yaml_content, Loader=yaml.FullLoader), file)
            return f"YAML content saved to {file_path} successfully"
    except IOError as e:
        return f"Error saving YAML content to file: {e}"
    except yaml.YAMLError as e:
        return f"Error parsing YAML content: {e}"

swagger_agent_system_message = """
You are a swagger OpenApi documentation generator. You generate docs in YML.
Generate the yml in a markdown code block.
Then save that yml into a file
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
swagger_agent.register_for_llm(name="save_yaml_to_file", description="Saves YAML content to a file.")(save_yaml_to_file)

user_proxy.register_for_execution(name="print_md_file_content")(print_md_file_content)
user_proxy.register_for_execution(name="save_yaml_to_file")(save_yaml_to_file)

chat_result = user_proxy.initiate_chat(swagger_agent, message="Convert 'api.md' to openapi specs.")
