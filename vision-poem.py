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

agent1 = MultimodalConversableAgent(
    name="image-explainer-1",
    max_consecutive_auto_reply=10,
    llm_config={"config_list": [{"model": "gpt-4o", "temperature": 1 ,"api_key": os.environ["OPENAI_API_KEY"], "max_tokens": 300}]},
    system_message="Your image description is poetic and engaging.",
)
agent2 = MultimodalConversableAgent(
    name="image-explainer-2",
    max_consecutive_auto_reply=10,
    llm_config={"config_list": [{"model": "gpt-4o", "temperature": 1 ,"api_key": os.environ["OPENAI_API_KEY"], "max_tokens": 300}]},
    system_message="Your image description is factual and to the point.",
)

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="Desribe image for me.",
    human_input_mode="TERMINATE",  # Try between ALWAYS, NEVER, and TERMINATE
    max_consecutive_auto_reply=10,
    code_execution_config={
        "use_docker": False
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
)

# We set max_round to 5
groupchat = autogen.GroupChat(agents=[agent1, agent2, user_proxy], messages=[], max_round=5)

vision_capability = VisionCapability(lmm_config={"config_list": [{"model": "gpt-4o", "temperature": 1 ,"api_key": os.environ["OPENAI_API_KEY"], "max_tokens": 300}]})
group_chat_manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"config_list": [{"model": "gpt-4o", "temperature": 1 ,"api_key": os.environ["OPENAI_API_KEY"]}]})
vision_capability.add_to_agent(group_chat_manager)

rst = user_proxy.initiate_chat(
    group_chat_manager,
    message="""Write a poet for my image:
                        <img https://th.bing.com/th/id/R.422068ce8af4e15b0634fe2540adea7a?rik=y4OcXBE%2fqutDOw&pid=ImgRaw&r=0>.""",
)