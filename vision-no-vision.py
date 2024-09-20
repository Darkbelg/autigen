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

agent_no_vision = AssistantAgent(name="Regular LLM Agent", llm_config={"config_list": [{"model": "gpt-4", "temperature": 1 ,"api_key": os.environ["OPENAI_API_KEY"]}]})

agent_with_vision = AssistantAgent(name="Regular LLM Agent with Vision Capability", llm_config={"config_list": [{"model": "gpt-4o", "temperature": 1 ,"api_key": os.environ["OPENAI_API_KEY"]}]})
vision_capability = VisionCapability(lmm_config={"config_list": [{"model": "gpt-4o", "temperature": 1 ,"api_key": os.environ["OPENAI_API_KEY"]}]})
vision_capability.add_to_agent(agent_with_vision)


user = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=0,
    code_execution_config={"use_docker": False},
)

message = """Write a poet for my image:
                        <img https://th.bing.com/th/id/R.422068ce8af4e15b0634fe2540adea7a?rik=y4OcXBE%2fqutDOw&pid=ImgRaw&r=0>."""
                        
user.send(message=message, recipient=agent_no_vision, request_reply=True)

user.send(message=message, recipient=agent_with_vision, request_reply=True)