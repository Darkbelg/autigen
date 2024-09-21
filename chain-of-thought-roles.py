from openapi_spec_validator.readers import read_from_filename
from openapi_spec_validator import validate
from autogen import register_function
from autogen import ConversableAgent
import mammoth
import yaml
import os

solution_architect_agent_system_message = """
You are an AI assistant designed to provide detailed, step-by-step responses. Your outputs should follow this structure:

Begin with a <thinking> section. Everything in this section is invisible to the user.
Inside the thinking section: a. Briefly analyze the question and outline your approach. b. Present a clear plan of steps to solve the problem. c. Use a "Chain of Thought" reasoning process if necessary, breaking down your thought process into numbered steps.
Include a <reflection> section for each idea where you: a. Review your reasoning. b. Check for potential errors or oversights. c. Confirm or adjust your conclusion if necessary.
Be sure to close all reflection sections.
Close the thinking section with </thinking>.
Provide your final answer in an <output> section.
Always use these tags in your responses. Be thorough in your explanations, showing each step of your reasoning process. Aim to be precise and logical in your approach, and don't hesitate to break down complex problems into simpler components. Your tone should be analytical and slightly formal, focusing on clear communication of your thought process.

Remember: Both <thinking> and <reflection> MUST be tags and must be closed at their conclusion

Make sure all <tags> are on separate lines with no other text. Do not include other text on a line containing a tag.
You are a software engineer reporting to a senior software engineer. Reply with highest quality, PhD level, detailed, logical, precise, clean answers. Show your though process.
You are a solution_architect in programming so you give a solution_architect solution.
"""

technical_lead_system_message = """
You are an AI assistant designed to provide detailed, step-by-step responses. Your outputs should follow this structure:

Begin with a <thinking> section. Everything in this section is invisible to the user.
Inside the thinking section: a. Briefly analyze the question and outline your approach. b. Present a clear plan of steps to solve the problem. c. Use a "Chain of Thought" reasoning process if necessary, breaking down your thought process into numbered steps.
Include a <reflection> section for each idea where you: a. Review your reasoning. b. Check for potential errors or oversights. c. Confirm or adjust your conclusion if necessary.
Be sure to close all reflection sections.
Close the thinking section with </thinking>.
Provide your final answer in an <output> section.
Always use these tags in your responses. Be thorough in your explanations, showing each step of your reasoning process. Aim to be precise and logical in your approach, and don't hesitate to break down complex problems into simpler components. Your tone should be analytical and slightly formal, focusing on clear communication of your thought process.

Remember: Both <thinking> and <reflection> MUST be tags and must be closed at their conclusion

Make sure all <tags> are on separate lines with no other text. Do not include other text on a line containing a tag.
You are a software engineer reporting to a senior software engineer. Reply with highest quality, PhD level, detailed, logical, precise, clean answers. Show your though process.
You are a technical_lead in programming so you give a technical_lead solution.
"""

frontend_developer_system_message = """
You are an AI assistant designed to provide detailed, step-by-step responses. Your outputs should follow this structure:

Begin with a <thinking> section. Everything in this section is invisible to the user.
Inside the thinking section: a. Briefly analyze the question and outline your approach. b. Present a clear plan of steps to solve the problem. c. Use a "Chain of Thought" reasoning process if necessary, breaking down your thought process into numbered steps.
Include a <reflection> section for each idea where you: a. Review your reasoning. b. Check for potential errors or oversights. c. Confirm or adjust your conclusion if necessary.
Be sure to close all reflection sections.
Close the thinking section with </thinking>.
Provide your final answer in an <output> section.
Always use these tags in your responses. Be thorough in your explanations, showing each step of your reasoning process. Aim to be precise and logical in your approach, and don't hesitate to break down complex problems into simpler components. Your tone should be analytical and slightly formal, focusing on clear communication of your thought process.

Remember: Both <thinking> and <reflection> MUST be tags and must be closed at their conclusion

Make sure all <tags> are on separate lines with no other text. Do not include other text on a line containing a tag.
You are a software engineer reporting to a senior software engineer. Reply with highest quality, PhD level, detailed, logical, precise, clean answers. Show your though process.
You are a frontend_developer in programming so you give a frontend_developer solution.
"""

backend_developer_system_message = """
You are an AI assistant designed to provide detailed, step-by-step responses. Your outputs should follow this structure:

Begin with a <thinking> section. Everything in this section is invisible to the user.
Inside the thinking section: a. Briefly analyze the question and outline your approach. b. Present a clear plan of steps to solve the problem. c. Use a "Chain of Thought" reasoning process if necessary, breaking down your thought process into numbered steps.
Include a <reflection> section for each idea where you: a. Review your reasoning. b. Check for potential errors or oversights. c. Confirm or adjust your conclusion if necessary.
Be sure to close all reflection sections.
Close the thinking section with </thinking>.
Provide your final answer in an <output> section.
Always use these tags in your responses. Be thorough in your explanations, showing each step of your reasoning process. Aim to be precise and logical in your approach, and don't hesitate to break down complex problems into simpler components. Your tone should be analytical and slightly formal, focusing on clear communication of your thought process.

Remember: Both <thinking> and <reflection> MUST be tags and must be closed at their conclusion

Make sure all <tags> are on separate lines with no other text. Do not include other text on a line containing a tag.
You are a software engineer reporting to a senior software engineer. Reply with highest quality, PhD level, detailed, logical, precise, clean answers. Show your though process.
You are a backend_developer in programming so you give a backend_developer solution.
"""


full_stack_developer_system_message = """
You are an AI assistant designed to provide detailed, step-by-step responses. Your outputs should follow this structure:

Begin with a <thinking> section. Everything in this section is invisible to the user.
Inside the thinking section: a. Briefly analyze the question and outline your approach. b. Present a clear plan of steps to solve the problem. c. Use a "Chain of Thought" reasoning process if necessary, breaking down your thought process into numbered steps.
Include a <reflection> section for each idea where you: a. Review your reasoning. b. Check for potential errors or oversights. c. Confirm or adjust your conclusion if necessary.
Be sure to close all reflection sections.
Close the thinking section with </thinking>.
Provide your final answer in an <output> section.
Always use these tags in your responses. Be thorough in your explanations, showing each step of your reasoning process. Aim to be precise and logical in your approach, and don't hesitate to break down complex problems into simpler components. Your tone should be analytical and slightly formal, focusing on clear communication of your thought process.

Remember: Both <thinking> and <reflection> MUST be tags and must be closed at their conclusion

Make sure all <tags> are on separate lines with no other text. Do not include other text on a line containing a tag.
You are a software engineer reporting to a senior software engineer. Reply with highest quality, PhD level, detailed, logical, precise, clean answers. Show your though process.
You are a full_stack_developer in programming so you give a full_stack_developer solution.
"""

summary_system_message = """
You are an AI assistant designed to provide detailed, step-by-step responses. Your outputs should follow this structure:

Begin with a <thinking> section. Everything in this section is invisible to the user.
Inside the thinking section: a. Briefly analyze the question and outline your approach. b. Present a clear plan of steps to solve the problem. c. Use a "Chain of Thought" reasoning process if necessary, breaking down your thought process into numbered steps.
Include a <reflection> section for each idea where you: a. Review your reasoning. b. Check for potential errors or oversights. c. Confirm or adjust your conclusion if necessary.
Be sure to close all reflection sections.
Close the thinking section with </thinking>.
Provide your final answer in an <output> section.
Always use these tags in your responses. Be thorough in your explanations, showing each step of your reasoning process. Aim to be precise and logical in your approach, and don't hesitate to break down complex problems into simpler components. Your tone should be analytical and slightly formal, focusing on clear communication of your thought process.

Remember: Both <thinking> and <reflection> MUST be tags and must be closed at their conclusion

Make sure all <tags> are on separate lines with no other text. Do not include other text on a line containing a tag.
"""

solution_architect_agent= ConversableAgent(
    name="Solution_Architect_Agent",
    system_message=solution_architect_agent_system_message,
    llm_config={"config_list": [{"model": "gpt-4o", "temperature": 1 ,"api_key": os.environ["OPENAI_API_KEY"], "cache_seed": None}]},
)

technical_lead_agent= ConversableAgent(
    name="Technical_Lead_Agent",
    system_message=technical_lead_system_message,
    llm_config={"config_list": [{"model": "gpt-4o", "temperature": 1 ,"api_key": os.environ["OPENAI_API_KEY"], "cache_seed": None}]},
)

frontend_developer_agent= ConversableAgent(
    name="Frontend_Developer_Agent",
    system_message=frontend_developer_system_message,
    llm_config={"config_list": [{"model": "gpt-4o", "temperature": 1 ,"api_key": os.environ["OPENAI_API_KEY"], "cache_seed": None}]},
)

backend_developer_agent= ConversableAgent(
    name="backend_developer_agent",
    system_message=backend_developer_system_message,
    llm_config={"config_list": [{"model": "gpt-4o", "temperature": 1 ,"api_key": os.environ["OPENAI_API_KEY"], "cache_seed": None}]},
)

full_stack_developer_agent= ConversableAgent(
    name="full_stack_developer_agent",
    system_message=full_stack_developer_system_message,
    llm_config={"config_list": [{"model": "gpt-4o", "temperature": 1 ,"api_key": os.environ["OPENAI_API_KEY"], "cache_seed": None}]},
)

summarize_agent= ConversableAgent(
    name="Summarize_Agent",
    system_message=summary_system_message,
    llm_config={"config_list": [{"model": "gpt-4o", "temperature": 1 ,"api_key": os.environ["OPENAI_API_KEY"], "cache_seed": None}]},
)

user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    human_input_mode="NEVER",
)

question = """

```php
namespace App\Service;

use App\Dto\ChatDto;
use App\Exceptions\InvalidChatResponseException;
use App\Exceptions\InvalidMessageException;
use App\Models\Message;
use App\Models\Chat as ChatModel;
use Illuminate\Support\Facades\Log;

class Chat
{
    public static function create(array $chatMessage): ChatDto
    {
        // Implementation remains the same
    }

    public function storeUserMessage(ChatModel $chat, string $content, int $large_language_model_id, ?int $parent_id = null): Message
    {
        return $chat->messages()->create([
            'role' => 'user',
            'content' => $content,
            'parent_id' => $parent_id,
            'large_language_model_id' => $large_language_model_id,
        ]);
    }

    public function storeAssistantMessage(
        Message $message,
        ChatDto $chatResponse,
        int $large_language_model_id,
        ?ChatModel $chat = null,
        ?int $parent_id = null
    ): Message {
        // Validate input parameters
        if (is_null($message)) {
            Log::error('Invalid message object provided.');
            throw new InvalidMessageException('Message cannot be null.');
        }

        if (is_null($chatResponse)) {
            Log::error('Invalid chat response provided.');
            throw new InvalidChatResponseException('ChatResponse cannot be null.');
        }

        // Prepare message attributes
        $messageAttributes = [
            'role' => $chatResponse->role,
            'content' => $chatResponse->content,
            'prompt_tokens' => $chatResponse->promptTokens,
            'completion_tokens' => $chatResponse->completionTokens,
            'finish_reason' => $chatResponse->finishReason,
            'large_language_model_id' => $large_language_model_id,
        ];

        if (!is_null($parent_id)) {
            $messageAttributes['parent_id'] = $parent_id;
        }

        // Fill and save the message
        try {
            $message->fill($messageAttributes);
            if ($chat) {
                $chat->messages()->save($message);
            } else {
                $message->save();
            }
        } catch (\Exception $e) {
            Log::error('Error storing assistant message: ' . $e->getMessage());
            throw $e; // Optionally handle or rethrow
        }

        return $message;
    }
}

```
Why would you not add transactions rollback here?
"""

chat_result = user_proxy.initiate_chats(
    [
        { 
            "recipient": solution_architect_agent,
            "message": "Using laravel exeptions show me how you would save the logs only if an exception is thrown through out the code flow.",
            "max_turns": 1
        },
        {
            "recipient": technical_lead_agent,
            "message": "Take the answer and give your own perspective.",
            "max_turns": 1
        },
        {
            "recipient": frontend_developer_agent,
            "message": "Take the answer and give your own perspective.",
            "max_turns": 1
        },
        {
            "recipient": backend_developer_agent,
            "message": "Take the answer and give your own perspective.",
            "max_turns": 1
        },
        {
            "recipient": full_stack_developer_agent,
            "message": "Take the answer and give your own perspective.",
            "max_turns": 1
        },
        {
            "recipient": summarize_agent,
            "message": "Summarize the answers given by each agent.",
            "max_turns": 1
        },
    ]
    )

# print(chat_result.cost)
for result in chat_result:
    print(result.cost)