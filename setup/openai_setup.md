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
4. Generate a new API key and **store it securely** (you won't be able to view it again).

### 2.2 Install OpenAI Python SDK
Ensure you have Python installed, then install the OpenAI package:
```sh
pip install openai
```

> **Note:** This book uses OpenAI Python SDK v1.0.0+. If you have an older version, upgrade with:
> ```sh
> pip install --upgrade openai
> ```

### 2.3 Verify Installation
Test if the package is working by running:
```python
from openai import OpenAI

client = OpenAI()
print(client.models.list())
```

If no errors appear, your setup is correct.

### 2.4 Using Your API Key in Code

#### Set Your API Key as Environment Variable (Recommended)
```sh
export OPENAI_API_KEY="your-api-key-here"
```

#### Basic Usage
```python
from openai import OpenAI

# Client automatically uses OPENAI_API_KEY environment variable
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello, AI!"}]
)

print(response.choices[0].message.content)
```

#### Structured Outputs (Used in Later Chapters)
The book uses OpenAI's structured outputs feature for reliable data extraction:
```python
from openai import OpenAI
from pydantic import BaseModel

class MovieReview(BaseModel):
    title: str
    rating: float
    summary: str

client = OpenAI()

response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Review the movie Inception"}],
    response_format=MovieReview
)

review = response.choices[0].message.parsed
print(f"{review.title}: {review.rating}/10")
```

### 2.5 Secure Your API Key

**Never hardcode your API key in source code.** Use environment variables:

```sh
# Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
export OPENAI_API_KEY="your-api-key"
```

Or use a `.env` file with `python-dotenv`:
```python
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # Loads OPENAI_API_KEY from .env file
client = OpenAI()
```

Your OpenAI access is now configured for both web-based ChatGPT and programmatic API usage!

---

## API Version Reference

This book uses the **OpenAI Python SDK v1.0.0+** (released November 2023). Key differences from older versions:

| Feature | Old API (v0.x) | New API (v1.0.0+) |
|---------|----------------|-------------------|
| Import | `import openai` | `from openai import OpenAI` |
| Client | `openai.api_key = "..."` | `client = OpenAI()` |
| Chat | `openai.ChatCompletion.create()` | `client.chat.completions.create()` |
| Embeddings | `openai.Embedding.create()` | `client.embeddings.create()` |
| Models | `openai.Model.list()` | `client.models.list()` |

If you encounter code examples online using the old syntax, refer to the [OpenAI Migration Guide](https://github.com/openai/openai-python/discussions/742).
