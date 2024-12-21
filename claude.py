import boto3
import json

# Define the prompt
prompt_data = """

Act as a Jungian and critique the concept of Twin Flames

"""

# Initialize the Bedrock client
bedrock = boto3.client(service_name="bedrock-runtime")

# Prepare the payload according to the model's JSON structure
payload = {
    "prompt": f"\n\nHuman: {prompt_data}\n\nAssistant:",
    "max_tokens_to_sample": 5000,
    "temperature": 0.5,
    "top_k": 250,  # Aligning with provided JSON structure
    "top_p": 0.9,
    "stop_sequences": ["\n\nHuman:"],  # Matching the stop sequence from JSON
    "anthropic_version": "bedrock-2023-05-31"
}

# Convert payload to JSON string
body = json.dumps(payload)

# Specify the model ID
model_id = "anthropic.claude-v2"

# Invoke the model
response = bedrock.invoke_model(
    body=body,
    modelId=model_id,
    accept="application/json",
    contentType="application/json"
)

# Parse and extract the response body
response_body = json.loads(response.get("body").read())
response_text = response_body.get("completion", "No response generated")  # Use `completion` key from Anthropic API

# Print the model's response
print(response_text)