### 🔧 Setting Up NewsAPI for Python

To access NewsAPI from Python, you'll first need to obtain an API key and configure your environment. Follow the steps below to get started.

---

#### 1. **Create a NewsAPI Account**
Head over to the registration page and sign up for a free developer account:

**https://newsapi.org/register**

Once registered, you’ll be issued a personal API key. This key is used to authenticate requests and track your usage.

---

#### 2. **Choose an Authentication Method**

You can include your API key in one of the following ways:

- **Querystring parameter**  
  ```text
  https://newsapi.org/v2/everything?q=tesla&apiKey=your_api_key
  ```

- **HTTP Header**  
  ```http
  X-Api-Key: your_api_key
  ```

- **Authorization header (Bearer token)**  
  ```http
  Authorization: Bearer your_api_key
  ```

In most Python scripts, the querystring or header option works best for simplicity.

---

#### 3. **Install the Required Package**

If you don’t already have it:

```bash
pip install requests
```

---

#### 4. **Example Python Script**

```python
import requests
from datetime import datetime, timedelta

# Replace this with your actual key
NEWS_API_KEY = "your_api_key"

# Date range: Yesterday to today
today = datetime.now().date()
yesterday = today - timedelta(days=1)

url = (
    f"https://newsapi.org/v2/everything?"
    f"q=tesla&from={yesterday}&to={today}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
)

response = requests.get(url)

# Check for errors
if response.status_code == 200:
    articles = response.json().get("articles", [])
    print(f"Fetched {len(articles)} articles.")
else:
    print(f"Request failed. Status code: {response.status_code}")
    print(response.text)
```

---

#### 5. **Tips for Using NewsAPI in Pipelines**

- Limit your `pageSize` to control response payloads.
- Always check `status_code` and use `.get("articles", [])` to avoid key errors.
- Consider logging failures for debugging in production workflows.

