from openapi_spec_validator.readers import read_from_filename
from openapi_spec_validator import validate
from autogen import register_function
from autogen import ConversableAgent
import mammoth
import yaml
import os

beginner_agent_system_message = """
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
You are a beginner in programming so you give a beginner solution.
"""

medior_system_message = """
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
You are a medior in programming so you give a medior solution.
"""

master_system_message = """
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
You are a master in programming so you give a master solution.
"""

expert_system_message = """
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
You are a expert in programming so you give a expert solution.
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

beginner_agent= ConversableAgent(
    name="Beginner_Agent",
    system_message=beginner_agent_system_message,
    llm_config={"config_list": [{"model": "gpt-4o", "temperature": 1 ,"api_key": os.environ["OPENAI_API_KEY"], "cache_seed": None}]},
)

medior_agent= ConversableAgent(
    name="Medior_Agent",
    system_message=medior_system_message,
    llm_config={"config_list": [{"model": "gpt-4o", "temperature": 1 ,"api_key": os.environ["OPENAI_API_KEY"], "cache_seed": None}]},
)

master_agent= ConversableAgent(
    name="Master_Agent",
    system_message=master_system_message,
    llm_config={"config_list": [{"model": "gpt-4o", "temperature": 1 ,"api_key": os.environ["OPENAI_API_KEY"], "cache_seed": None}]},
)

expert_agent= ConversableAgent(
    name="Export_Agent",
    system_message=expert_system_message,
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
            "recipient": beginner_agent,
            "message": "Using laravel exeptions show me how you would save the logs only if an exception is thrown through out the code flow.",
            "max_turns": 1
        },
        {
            "recipient": medior_agent,
            "message": "Take the answer of the beginner and give your medior solution.",
            "max_turns": 1
        },
        {
            "recipient": master_agent,
            "message": "Take the answer of the beginner and medior and give your master solution.",
            "max_turns": 1
        },
        {
            "recipient": expert_agent,
            "message": "Take the answer of the beginner, medior and master and give your expert solution.",
            "max_turns": 1
        },
        {
            "recipient": summarize_agent,
            "message": "Take the answers and summarize the solution. Give code example if there is one.",
            "max_turns": 1
        },
    ]
    )

# print(chat_result.cost)
for result in chat_result:
    print(result.cost)