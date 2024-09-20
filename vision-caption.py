import json
import os
import random
import time
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

import matplotlib.pyplot as plt
import numpy as np
import requests
from PIL import Image
from termcolor import colored

import autogen
from autogen import Agent, AssistantAgent, ConversableAgent, UserProxyAgent
from autogen.agentchat.contrib.capabilities.vision_capability import VisionCapability
from autogen.agentchat.contrib.img_utils import get_pil_image, pil_to_data_uri
from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent
from autogen.code_utils import content_str

user = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=0,
    code_execution_config={"use_docker": False},
)

message = """Write a poet for my image:
                        <img https://th.bing.com/th/id/R.422068ce8af4e15b0634fe2540adea7a?rik=y4OcXBE%2fqutDOw&pid=ImgRaw&r=0>."""

def my_description(image_url: str, image_data: Image = None, lmm_client: object = None) -> str:
    """
    This function takes an image URL and returns the description.

    Parameters:
        - image_url (str): The URL of the image.
        - image_data (PIL.Image): The image data.
        - lmm_client (object): The LLM client object.

    Returns:
        - str: A description of the color of the image.
    """
    # Print the arguments for illustration purpose
    print("image_url", image_url)
    print("image_data", image_data)
    print("lmm_client", lmm_client)

    img_uri = pil_to_data_uri(image_data)  # cast data into URI (str) format for API call
    lmm_out = lmm_client.create(
        context=None,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image in 10 words."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": img_uri,
                        },
                    },
                ],
            }
        ],
    )
    description = lmm_out.choices[0].message.content
    description = content_str(description)

    # Convert the image into an array of pixels.
    pixels = np.array(image_data)

    # Calculate the average color.
    avg_color_per_row = np.mean(pixels, axis=0)
    avg_color = np.mean(avg_color_per_row, axis=0)
    avg_color = avg_color.astype(int)  # Convert to integer for color values

    # Format the average color as a string description.
    caption = f"""The image is from {image_url}
    It is about: {description}
    The average color of the image is RGB:
        ({avg_color[0]}, {avg_color[1]}, {avg_color[2]})"""

    print(caption)  # For illustration purpose

    return caption

agent_with_vision_and_func = AssistantAgent(
    name="Regular LLM Agent with Custom Func and LMM", llm_config={"config_list": [{"model": "gpt-4o", "temperature": 1 ,"api_key": os.environ["OPENAI_API_KEY"]}]}
)

vision_capability_with_func = VisionCapability(
    lmm_config={"config_list": [{"model": "gpt-4o", "temperature": 1 ,"api_key": os.environ["OPENAI_API_KEY"]}]},
    custom_caption_func=my_description,
)
vision_capability_with_func.add_to_agent(agent_with_vision_and_func)

user.send(message=message, recipient=agent_with_vision_and_func, request_reply=True)