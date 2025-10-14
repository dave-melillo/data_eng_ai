# Setting Up OpenAI Access

To integrate OpenAI's services into your workflows, follow these steps to set up both general ChatGPT access and programmatic API access.

## 1. Accessing ChatGPT (Web-Based)
1. Visit [OpenAI's ChatGPT page](https://chat.openai.com/).
2. Sign up or log in to your OpenAI account.
3. Choose a free or pro plan for accessing GPT models via the web.
4. Start using ChatGPT by entering prompts and exploring its features.

## 2. Setting Up OpenAI API Access
### 2.1 Create an OpenAI Account
1. Visit [OpenAI's platform page](https://platform.openai.com/).
2. Sign in or create an account.
3. Navigate to **API Keys** under your profile settings.
4. Generate a new API key and **store it securely** (you won’t be able to view it again).

### 2.2 Install OpenAI Python SDK
Ensure you have Python installed, then install the OpenAI package:
```sh
pip install openai
```

### 2.3 Verify Installation
Test if the package is working by running:
```python
import openai

openai.Model.list()
```
If no errors appear, your setup is correct.

### 2.4 Using Your API Key in Code
In your Python scripts, use:
```python
import openai

openai.api_key = "your-api-key-here"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello, AI!"}]
)

print(response["choices"][0]["message"]["content"])
```

### 2.5 Secure Your API Key
Do not hardcode your API key. Use environment variables:
```sh
export OPENAI_API_KEY="your-api-key"
```
Or load it in Python:
```python
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
```

Your OpenAI access is now configured for both web-based ChatGPT and programmatic API usage!