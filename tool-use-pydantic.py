import os
from autogen import ConversableAgent
from typing import Annotated, Literal
from pydantic import BaseModel, Field

Operator = Literal["+", "-", "*", "/"]

# Let's first define the assistant agent that suggests tool calls.
assistant = ConversableAgent(
    name="Assistant",
    system_message="You are a helpful AI assistant. "
    "You can help with simple calculations. "
    "Return 'TERMINATE' when the task is done.",
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": os.environ["OPENAI_API_KEY"]}]},
)

# The user proxy agent is used for interacting with the assistant agent
# and executes tool calls.
user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

class CalculatorInput(BaseModel):
    a: Annotated[int, Field(description="The first number.")]
    b: Annotated[int, Field(description="The second number.")]
    operator: Annotated[Operator, Field(description="The operator.")]

def calculator(input: Annotated[CalculatorInput, "Input to the calculator."]) -> int:
    if input.operator == "+":
        return input.a + input.b
    elif input.operator == "-":
        return input.a - input.b
    elif input.operator == "*":
        return input.a * input.b
    elif input.operator == "/":
        return int(input.a / input.b)
    else:
        raise ValueError("Invalid operator")
    
assistant.register_for_llm(name="calculator", description="A calculator tool that accepts nested expression as input")(
calculator
)
user_proxy.register_for_execution(name="calculator")(calculator)

assistant.llm_config["tools"]

chat_result = user_proxy.initiate_chat(assistant, message="What is (1423 - 123) / 3 + (32 + 23) * 5?")

