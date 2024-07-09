## AI Agent Microservice 1.0.0

AI Agent Microservice allows natural communication between the user and other microservices. This service
uses the Hugging Face LLM  Trelis/Llama-2-7b-chat-hf-function-calling-v3 to convert text commands into API
calls, process the LLM result, and call the corresponding API request.

The service requires a prompt description defining the available functions and the behavior of the LLM and a
configuration file that defines the API calls and their mapping with the prompt function. See below for more details.

### Prompt format

Prompt should follow the model prompt format, please check model documentation at
https://huggingface.co/Trelis/Llama-2-7b-chat-hf-function-calling-v3

### API configuration

The API configuration is a JSON file with the following structure:

```json
{
    "function_name": {
        "ip": "api_ip",
        "port": "api_port",
        "path": "api_request_path",
        "method": "request_method",
        "properties": {
            "prop1": "prop1 value",
            "prop2": "prop2 value"
        },
        "body": {
            "arg1": "value",
            "arg2": "value"
        }
    }
}
```
The JSON should have a function object per function described in the prompt since it will be used to
map the LLM reply function with the microservice API call. So the function_name should match one of the
functions defined in the prompt.

The arguments port, path, and method are required. Port is the port of the microservice to call, path
is the route of the specific API request and method is the method for the request can be GET, POST, PUT.

The argument ip is optional, it defines the IP of the microservice to call. If not defined localhost 127.0.0.0
will be used.

properties object defines the parameters of the API request. It is optional, add it only if the API request uses
parameters. The value of each property will be obtained from the LLM reply, so the string in the value should
match the argument name defined in the corresponding prompt function.

body object defines the API request content. It is optional, add it only if the API request needs body description.
The value of each argument in the body will be obtained from the LLM reply, so the string in the value should
match the argument name defined in the corresponding prompt function.


Check the following example:

```json
{
  "search_object": {
    "ip": "192.168.86.25",
    "port": 30080,
    "path": "genai/prompt",
    "method": "GET",
    "properties": {
      "objects": "input",
      "thresholds": 0.2
    }
  },
  "move_camera": {
    "port": 1234,
    "path": "position",
    "method": "PUT",
    "body": {
      "pan": "pan_angle",
      "tilt": "tilt_angle"
    }
  }
}
```

### Running the service

The project is configured (via setup.py) to install the service with the name __ai-agent__. So to install it run:

```bash
pip install .
```

Then you will have the service with the following options:

```bash
usage: ai-agent [-h] [--port PORT] --system_prompt SYSTEM_PROMPT --api_map API_MAP

options:
  -h, --help            show this help message and exit
  --port PORT           Port for server
  --system_prompt SYSTEM_PROMPT
                        String with system prompt or path to a txt file with the prompt
  --api_map API_MAP     Path to a JSON file with API mapping configuration
usage: ai-agent [-h] [--port PORT] [--system_prompt SYSTEM_PROMPT] [--api_map API_MAP]
```

Notice that the system_prompt and api_map are required, so to run it use the following command:

```bash
ai-agent --prompt PROMPT --api_map API_MAP
```

This will start the service in address 127.0.0.0 and port 5010. If you want to use a different port, use the __--port__ options.


## AI Agent Docker


### Build the container

We can build the gen-ai microservice container using the Dockerfile in the docker directory. This includes a base tensort
image and the dependencies to run the ai-agent microservice application.

First, we need to prepare the context directory for this build, you need to create a directory and include this repository
and the rrms-utils project. The Dockerfile will look for both packages in the context directory and copy them to the container.

```bash
ai-agent-context/
├── ai-agent
└── rrms-utils
```

Then build the container image with the following command:

```bash
DOCKER_BUILDKIT=0 docker build --network=host --tag ridgerun/ai-agent-service --file ai-agent-context/ai-agent/docker/Dockerfile ai-agent-context/
```

Change ai-agent-context/ to the path of your context and the tag to the name you want to give to your image.


### Launch the container

The container can be launched by running the following command:

```bash
docker run --runtime nvidia -it  --network host --volume /home/nvidia/config:/ai-agent-config --name ai-agent  ridgerun/ai-agent-service:latest ai-agent --system_prompt ai-agent-config/prompt.txt --api_map ai-agent-config/api_mapping.json
```

Here we are creating a container called ai-agent. Notice we are mounting the directory /home/nvidia/config into /ai-agent-config, this contains the prompt and API configuration files, you can change it to point to your configuration directory or any place where you have the required configs. Also, we are defining the ai-agent microservice application as entry point with its corresponding parameters.
