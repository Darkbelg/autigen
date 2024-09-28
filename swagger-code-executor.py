from openapi_spec_validator.readers import read_from_filename
from autogen.coding import LocalCommandLineCodeExecutor
from autogen import ConversableAgent,register_function
from openapi_spec_validator import OpenAPIV30SpecValidator
from openapi_spec_validator import validate_spec

from openapi_spec_validator import validate
import tempfile
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

# def validate_swagger_or_openapi_file(file_path: str) -> str:
#     """
#     Validates a Swagger or OpenAPI file.
    
#     Args:
#     file_path (str): The path to the file to be validated.
    
#     Returns:
#     str: A success message if the file is valid, or an error message indicating what's wrong.
#     """
#     try:
#         spec_dict, _ = read_from_filename(file_path)
#         validate(spec_dict)
#         return f"Swagger/OpenAPI file {file_path} is valid"
#     except Exception as e:
#         return f"Error: {e}"
#     except yaml.YAMLError as e:
#         return f"Error parsing YAML file: {e}"
#     except IOError as e:
#         return f"Error reading file: {e}"

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
        validate_spec(spec_dict, cls=OpenAPIV30SpecValidator)
        
        # If we reach this point, the file is valid
        return f"Success: The OpenAPI 3.0 file '{file_path}' is valid."
    
    except yaml.YAMLError as e:
        return f"Error: Unable to parse YAML in '{file_path}'. Details: {str(e)}"
    
    except IOError as e:
        return f"Error: Unable to read file '{file_path}'. Details: {str(e)}"
    
    except Exception as e:
        return f"Error: Validation failed for '{file_path}'. Details: {str(e)}"
    

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
    except Exception as e:
        # Handle any other unexpected errors
        return f"Unexpected error occurred: {e}"


swagger_agent_system_message = """
You are a OpenApi specification assistant. You generate version 3.1.x specifications in YML.
Do this step by step:
1 Convert the word document to a readme file.
2 read the generated markdown file.
3 generate the yml in a markdown code block.
5 compile the yml and put it into a file called api.py NOT api.yml.
6 validate the yml file.
7 If you get any errors reflect and fix any mistakes that come out of the validator.

Convert 'petstore.md' to openapi specs.
"""
#ADD AN ERROR IN THE SPEC TO TEST THE VALIDATION

# Create a temporary directory to store the code files.
temp_dir = 'openapi/'

# Create a local command line code executor.
executor = LocalCommandLineCodeExecutor(
    timeout=10,  # Timeout for each code execution in seconds.
    work_dir=temp_dir,  # Use the temporary directory to store the code files.
)

# Create an agent with code executor configuration.
code_executor_agent = ConversableAgent(
    "code_executor_agent",
    llm_config=False,  # Turn off LLM for this agent.
    code_execution_config={"executor": executor},  # Use the local command line code executor.
    human_input_mode="ALWAYS",  # Always take human input for this agent for safety.
)

# The code writer agent's system message is to instruct the LLM on how to use
# the code executor in the code executor agent.
code_writer_system_message = """You are a helpful AI assistant.
Solve tasks using your coding and language skills.
In the following cases, suggest python code (in a python coding block) or shell script (in a sh coding block) for the user to execute.
1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself.
2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly.
Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill.
When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user.
If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.
Reply 'TERMINATE' in the end when everything is done.
"""

swagger_code_writer_system_message = """You are a helpful AI assistant.
If you want the user to save the open api specification in a file, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
Reply 'TERMINATE' in the end when everything is done.
"""

swagger_agent_system_message_error = """
Validate api.yml file
"""

code_writer_agent = ConversableAgent(
    "code_writer_agent",
    system_message=code_writer_system_message,
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": os.environ["OPENAI_API_KEY"]}]},
    code_execution_config=False,  # Turn off code execution for this agent.
)

# chat_result = code_executor_agent.initiate_chat(
#     code_writer_agent,
#     message="Write Python code to calculate the 14th Fibonacci number.",
# )

swagger_agent= ConversableAgent(
    name="Swagger_Agent",
    system_message=swagger_code_writer_system_message,
    llm_config={"config_list": [{"model": "gpt-4o", "temperature": 0 ,"api_key": os.environ["OPENAI_API_KEY"]}], "cache_seed": None,},
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    code_execution_config=False,  # Use the local command line code executor.
)

user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
    code_execution_config={"last_n_messages": 3, "work_dir": "openapi", "use_docker": False},
)

swagger_agent.register_for_llm(name="print_file_content", description="Print the content of a file.")(print_file_content)
#swagger_agent.register_for_llm(name="save_yaml_to_file", description="Saves YAML content to a file.")(save_yaml_to_file)
swagger_agent.register_for_llm(name="validate_swagger_or_openapi_file", description="Validates a Swagger or OpenAPI YAML file.")(validate_swagger_or_openapi_file)
swagger_agent.register_for_llm(name="convert_word_to_markdown", description="Converts a Word document to a markdown file.")(convert_word_to_markdown)

user_proxy.register_for_execution(name="print_file_content")(print_file_content)
#user_proxy.register_for_execution(name="save_yaml_to_file")(save_yaml_to_file)
user_proxy.register_for_execution(name="validate_swagger_or_openapi_file")(validate_swagger_or_openapi_file)
user_proxy.register_for_execution(name="convert_word_to_markdown")(convert_word_to_markdown)

chat_result = user_proxy.initiate_chat(swagger_agent, message = swagger_agent_system_message, max_turns = 20)

print(chat_result.cost)
