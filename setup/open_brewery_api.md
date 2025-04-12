# 🍺 Open Brewery DB API Overview

The **Open Brewery DB API** is a free, public API that provides structured information about breweries in the United States. It’s perfect for building data pipelines, testing API integrations, or just exploring data with Python and Jupyter.

🔗 **Official Docs:** https://www.openbrewerydb.org/documentation/

---

## 📦 What You Can Access

Each API response may include:

- 🏷️ `name` – Brewery name  
- 🏙️ `city`, `state`, `country` – Location details  
- ☎️ `phone` – Contact number  
- 🌐 `website_url` – Website address  
- 🍻 `brewery_type` – Type of brewery (micro, nano, brewpub, etc.)  
- 🆔 `id` – Unique brewery ID

---

## 🔗 Example Endpoint

```http
GET https://api.openbrewerydb.org/v1/breweries?by_state=new_york&per_page=5
```

📥 Returns JSON with details of 5 breweries from New York.

---

## 🔧 Getting Started

You don’t need an API key. Just use standard HTTP requests. Great for fast prototyping!

### ✅ Requirements for Local Use

- Python 3.7+
- Internet connection
- `requests` and `pandas` libraries (optional but useful)

### 📦 Install Dependencies

```bash
pip install requests pandas
```

---

## 💡 Handy Query Parameters

| Parameter        | Description                                 |
|------------------|---------------------------------------------|
| `by_state`       | Filter breweries by U.S. state              |
| `by_city`        | Filter by city                              |
| `by_type`        | Filter by brewery type                      |
| `per_page`       | Limit results per page (default: 20)        |
| `by_postal`      | Filter by ZIP code                          |
| `by_name`        | Search by name (partial match supported)    |

📚 See the full list at the [official API docs](https://www.openbrewerydb.org/documentation/).

---

## 📁 Sample Response

```json
[
  {
    "id": 9094,
    "name": "Against the Grain Brewery",
    "brewery_type": "brewpub",
    "city": "Louisville",
    "state": "Kentucky",
    "phone": "5025150174",
    "website_url": "http://www.atgbrewery.com"
  },
  ...
]
```

---

## ⚠️ Notes

- ❌ No authentication required
- ✅ CORS enabled (works in browser-based apps)
- 📄 Returns `application/json` by default

---

## 📎 Useful Links

- [Open Brewery DB Homepage](https://www.openbrewerydb.org/)
- [API Documentation](https://www.openbrewerydb.org/documentation/)
- [GitHub Repo](https://github.com/openbrewerydb/openbrewerydb)

---

**Explore breweries. Build data workflows. Cheers! 🍻**