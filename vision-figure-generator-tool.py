import os
import autogen

# Configuration for the language model
config_list = [
    {
        "model": "gpt-4o-mini",
        "api_key": os.environ.get("OPENAI_API_KEY"),
    }
]

# Create a user proxy agent
user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=0
)

# Create an assistant agent for OpenAPI generation
openapi_generator = autogen.AssistantAgent(
    name="OpenAPIGenerator",
    system_message="You are an expert in creating OpenAPI specifications. When asked to generate a 3.0.x OpenAPI spec, provide it in a YAML code block. End your message with TERMINATE.",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    llm_config={"config_list": config_list},
)

# Function to save YAML content to a file
def save_yaml_to_file(content):
    with open('openapi.yml', 'w') as file:
        file.write(content)

# Initiate the chat
user_proxy.initiate_chat(
    openapi_generator,
    message="Generate an OpenAPI specification for a simple weather API with endpoints for current weather and forecast."
)

# Get the last message from the conversation
last_message = user_proxy.last_message()

# Print the last message
print("Last message:")
print(last_message["content"])

# Check if the last message contains a YAML block and save it
if "```yaml" in last_message["content"] and "```" in last_message["content"].split("```yaml", 1)[1]:
    yaml_content = last_message["content"].split("```yaml", 1)[1].split("```", 1)[0].strip()
    save_yaml_to_file(yaml_content)
    print("\nYAML content saved to openapi.yml")


