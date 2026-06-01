# 🐍 Chapter 4: Using a Coding Companion with Python

In this chapter, we turn the spotlight on **Python**—the Swiss Army knife of the data engineering world—and show how your AI coding companion (like ChatGPT) can supercharge your workflow.

Whether you're fetching data from an API, flattening nested JSON, or writing a tricky regex pattern, Python gives you the tools—and your coding companion gives you the speed.

---

## 🚀 What This Chapter Covers

- 🤖 Using AI to write and refine Python scripts for data engineering tasks.
- 🔗 Interacting with APIs like PokeAPI and Open Brewery DB.
- 🧱 Flattening deeply nested JSON into clean, structured DataFrames.
- 🔍 Writing and normalizing regular expressions (regex) with AI assistance.
- 🧠 Practicing prompt strategies like zero-shot, few-shot, and refinement loops in Python.

---

## 🧰 Key Tools & Concepts

| Tool | Purpose |
|------|---------|
| `requests` | Perform API calls to retrieve structured JSON data |
| `pandas` | Store, transform, and analyze tabular data |
| `re` | Extract and normalize string patterns using regular expressions |
| `logging` | Capture errors and debug info when working with APIs |
| ChatGPT / Coding Companion | Generate, test, and refine Python logic step-by-step |

---

## 🌐 APIs Explored

### 🔴 PokeAPI

A free and simple API that returns detailed JSON data about every Pokémon, keyed by Pokédex number.

- URL Format: `https://pokeapi.co/api/v2/pokemon/<id or name>`
- No API key needed
- Returns fields like `name`, `types`, `base_experience`, and `abilities`
- Great for exploring basic API request/response workflows

📖 [PokeAPI Documentation](https://pokeapi.co/docs/v2)

---

### 🍺 Open Brewery DB API

A public API that returns structured info about breweries across the U.S.

- URL Example: `https://api.openbrewerydb.org/v1/breweries?by_state=new_york&per_page=5`
- No API key required
- JSON-based responses include name, city, phone, website, and type

📖 [Open Brewery DB Docs](https://www.openbrewerydb.org/documentation/)

---

## 🧪 Try-It-Now Challenges (explained in the full chapter)

1. Query Pokémon data using PokeAPI and format it into a `pandas` DataFrame.
2. Enhance your API scripts with retry logic and logging using few-shot prompting.
3. Upload an API reference file (e.g., `pokeapi_reference.txt`) to guide your AI assistant toward better code.
4. Flatten deeply nested JSON data from `JSONPlaceholder` into usable table formats.
5. Extract and normalize U.S. phone numbers using Python’s `re` module.

---

## 🧠 Prompting Tips

| Strategy | When to Use |
|----------|--------------|
| **Zero-Shot** | For simple, familiar APIs or tasks your AI already knows |
| **Few-Shot** | When refining or extending code across multiple steps |
| **Chain-of-Thought** | When debugging or handling complex logic incrementally |
| **Prompt + File Upload** | When working with private or complex API docs |

---

## ✅ Chapter Outcomes

By the end of this chapter, you’ll know how to:

- ⚙️ Fetch and handle API data using `requests`
- 🧹 Clean and transform messy data into analysis-ready format
- 🔄 Iterate with your AI assistant to refine Python logic
- 🧪 Automate and debug repetitive coding tasks with confidence

---

**Next up: Put your Python + AI skills to the test in a hands-on lab using the Open Brewery DB API. 🍻**
