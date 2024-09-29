from openapi_spec_validator import validate_spec,OpenAPIV30SpecValidator
from openapi_spec_validator.readers import read_from_filename
from autogen import ConversableAgent, UserProxyAgent
import yaml
import os
import re

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

# Configuration for the language model
config_list = [
    {
        "model": "gpt-4o",
        "api_key": os.environ.get("OPENAI_API_KEY"),
        "temperature": 0.2,
        "cache_seed": None,
    }
]

# Create a user proxy agent
user_proxy = UserProxyAgent(
    name="User",
    llm_config=False,
    human_input_mode="NEVER",
    code_execution_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
)

laravel_generator_system_message = """
You are a helpful AI assistant.
You write boilerplate laravel php code based on open api specifications according to the adapter pattern.

Use markdown code blocks to write PHP code. One code block per answer.
When writing php, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify.
Put // filename: <filepath/filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result.

1. print out the open api spec openapi.yml
2. Respond to the USER with a small technical specification on the different resource you should create before generating the code. Group the urls with the same structure like a CRUD resource.
3. Then execute the technical specification.
    1. Create a data class for the adapter
    2. Create an interface for the adapter class
    3. Create the adapter class implementing the interface
        - In the constructor add dependency injection. Add a property public Api $api.
    4. Create a data class for the service
    5. Create an service class that is a pass through to the adapter class. The user will change this code in the future for specific logic.
        - Add the adapter as dependency injection. (Do not worry about the specifics in appserviceprovider this is for the user.)
4. Respond with your answer.
5. Repeat step 3 until you have done all URL resources.
6. Reflect

Example:
```php
// filenam: app/Example/Adapter/Contract/ExampleData.php
<?php

namespace App\Example\Adapter\Contract;

use Spatie\LaravelData\Attributes\MapInputName;
use Spatie\LaravelData\Data;

class ExampleData extends Data
{
    public function __construct(
        #[MapInputName('id')]
        public int $id,

        #[MapInputName('username')]
        public string $username,

        #[MapInputName('firstName')]
        public string $firstName,

        #[MapInputName('lastName')]
        public string $lastName,

        #[MapInputName('email')]
        public string $email,

        #[MapInputName('password')]
        public string $password,

        #[MapInputName('phone')]
        public string $phone,

        #[MapInputName('userStatus')]
        public int $userStatus,
    ) {}
}
```

```php
// filenam: app/Example/Adapter/Contract/ExampleAdapter.php
<?php 
namespace App\Example\Adapter\Contract;

use Api;
use App\Example\Adapter\Contract\ExampleData;

interface ExampleAdapter
{

    public function index(
        int $page = 1,
        int $limit = 10
    ){
    };

    public function show(string $id){
    }:ExampleData;

    public function create(array $exampleObject){
    };

    public function update(array $exampleObject){
    };

    public function delete(string $id){
    };

    public function setIsSick(string $id, bool $isSick){
    };
}
```

```php
// filenam: app/Example/Adapter/ExampleAdapter.php
<?php 
namespace App\Example\Adapter;

use Api;
use App\Example\Adapter\Contract\ExampleAdapter as ExampleAdapterInterface;
use App\Example\Adapter\Contract\ExampleData;

class ExampleAdapter implements ExampleAdapterInterface {

    use ResponseProcessingTrait;

    public function __construct(
        public string $url  = 'exampleBaseUrl',
        public Api $api
    ) {
    }

    public function index(
        int $page = 1,
        int $limit = 10
    ){
        $response = $this->api->get(
            [
                'page' => $page,
                'limit' => $limit
            ]
        );

        if(!$response->isSuccesull()){
            $this->handleResponseTrait($response);
        }

        return collect($response['items'])->map(fn ($item) => ExampleData::from($item));
    }

    public function show(string $id){
        $response = $this->api->get($id);

        if(!$response->isSuccesull()){
            $this->handleResponseTrait($response);
        }

        return collect($response['item'])->map(fn ($item) => ExampleData::from($item));
    }

    public function create(array $exampleObject){
        $response = $this->api->post($exampleObject);
        if(!$response->isSuccesull()){
            $this->handleResponseTrait($response);
        }

        return collect($response['item'])->map(fn ($item) => ExampleData::from($item));
    }

    public function update(array $exampleObject){
        $response = $this->api->put($exampleObject);
        if(!$response->isSuccesull()){
            $this->handleResponseTrait($response);
        }

        return collect($response['item'])->map(fn ($item) => ExampleData::from($item));
    }

    public function delete(string $id){
        $response = $this->api->delete($id);
        if(!$response->isSuccesull()){
            $this->handleResponseTrait($response);
        }
    }

    public function setIsSick(string $id, bool $isSick){
        $response = $this->api->post(['id' => $id, 'sick' => $isSick]);
        if(!$response->isSuccesull()){
            $this->handleResponseTrait($response);
        }

        return collect($response['item'])->map(fn ($item) => ExampleData::from($item));
    }
}
```

```php
// filenam: app/Example/Service/Contract/ExampleData.php
<?php

namespace App\Example\Service\Contract;

use Spatie\LaravelData\Attributes\MapInputName;
use App\Example\Adapter\Contract\ExampleData as ExampleDataAdapter;
use Spatie\LaravelData\Data;

class ExampleData extends Data
{
    public function __construct(
        public readonly ExampleDataAdapter $adapter,
    ) {}

    public static function fromExampleDataAdapter(ExampleDataAdapter $exampleDataAdapter){
        return new self($exampleDataAdapter);
    }
}
```

```php
// filenam: app/Example/Service/ExampleService.php
<?php 
namespace App\Example\Service;

use Api;
use App\Example\Adapter\ExampleAdapter;
use App\Example\Service\Contract\ExampleData;

class ExampleService
{
    public function __construct(
        public ExampleAdapter $exampleAdapter
    ) {
    }

    public function index(){
        return collect($this->exampleAdapter->index())->map(fn($items) => ExampleData::from($item));
    }

    public function show(string $id){
        return ExampleData::from($this->exampleAdapter->show($id));
    }

    public function create(array $exampleObject){
        return ExampleData::from($this->exampleAdapter->create($exampleObject));
    }

    public function update(array $exampleObject){
        return ExampleData::from($this->exampleAdapter->update($exampleObject));
    }

    public function delete(string $id){
        return $this->exampleAdapter->delete($id);
    }

    public function setIsSick(string $id, bool $isSick){
        return ExampleData::from($this->exampleAdapter->setIsSick($id, $isSick));
    }
}
```

The user is counting on you to write a draft of the code as accurate as possible.    
Reply 'TERMINATE' in the end when everything is done.
"""


# You are a helpful AI assistant.
# Solve tasks using your coding and language skills.
# In the following cases, suggest python code (in a python coding block) or shell script (in a sh coding block) for the user to execute.
# 1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself.
# 2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly.
# Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill.
# When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user.
# If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user.
# If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
# When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.
# Reply 'TERMINATE' in the end when everything is done.

# Create an assistant agent for OpenAPI generation
laravel_generator = ConversableAgent(
    name="OpenAPIGenerator",
    system_message=laravel_generator_system_message,
    llm_config={"config_list": config_list},
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

def save_content_to_file(content, filename):
    # Create directories if they don't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as file:
        file.write(content)

def extract_code_blocks(message_content):
    # Regular expression to match code blocks and their file names
    pattern = r'```(\w+)\n// filename: (.+?)\n(.*?)```'
    matches = re.findall(pattern, message_content, re.DOTALL)
    
    code_blocks = []
    for lang, filename, content in matches:
        code_blocks.append({
            'language': lang,
            'filename': filename.strip(),
            'content': content.strip()
        })
    
    return code_blocks

def process_and_save_code_blocks(message_content):
    code_blocks = extract_code_blocks(message_content)
    saved_files = []

    for block in code_blocks:
        filename = block['filename']
        content = block['content']
        save_content_to_file(content, filename)
        saved_files.append(filename)

    return saved_files

def process_message_before_send_and_extract_code(sender, message, recipient, silent):
    print('process_message_before_send_and_extract_code')
    
    if isinstance(message, dict) and "content" in message:
        if message["content"] is not None:
            saved_files = process_and_save_code_blocks(message["content"])
            if saved_files:
                print(f"Saved files: {', '.join(saved_files)}")
    elif isinstance(message, str):
        saved_files = process_and_save_code_blocks(message)
        if saved_files:
            print(f"Saved files: {', '.join(saved_files)}")
    
    return message

# Register the hook for processing the last received message
laravel_generator.register_hook(
    hookable_method="process_message_before_send",
    hook=process_message_before_send_and_extract_code
)

laravel_generator.register_for_llm(name="print_file_content", description="Print the content of a file.")(print_file_content)

user_proxy.register_for_execution(name="print_file_content")(print_file_content)

# Initiate the chat
chat_result = user_proxy.initiate_chat(
    laravel_generator,
    message="Create boilerplate for openapi.yml",
    max_turns = 10
)

print(chat_result.cost)
