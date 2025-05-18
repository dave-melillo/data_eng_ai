## 🛠️ Environment Variable Setup Guide (for `os.getenv()` in Python)

### Step 1: Why use environment variables?
When working with APIs like OpenAI or NewsAPI, you *never* want to hardcode your API keys directly in your scripts. That’s like leaving your house key taped to the front door. Instead, store them as environment variables and access them securely in your Python code.

---

### Step 2: Set your environment variable

#### ✅ Option A: Set it directly in your terminal

This will make it available only during your session.

**Mac/Linux:**
```bash
export OPENAI_API_KEY="your-secret-api-key"
```

**Windows (CMD):**
```cmd
set OPENAI_API_KEY=your-secret-api-key
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="your-secret-api-key"
```

---

### Step 3: Access the key in your Python script

In your Python script or notebook, do this:

```python
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
```

This pulls the key from your environment and keeps it out of your code.

---

### Step 4: (Optional) Use a `.env` file for local development

For convenience, you can store keys in a `.env` file and load them automatically using `python-dotenv`.

**1. Create a `.env` file:**

```
OPENAI_API_KEY=your-secret-api-key
```

**2. Install `python-dotenv`:**

```bash
pip install python-dotenv
```

**3. Load it in your script:**

```python
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
```

---

### Step 5: Confirm it’s working

Print your key (carefully!) or just check that it’s not `None`:

```python
print("Key loaded:", openai.api_key is not None)
```

---

### 🔐 Pro Tip

Never commit `.env` files or keys to GitHub. Add this to your `.gitignore`:

```
.env
```