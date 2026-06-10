# Chapter 2: Advantages & Disadvantages of Using an AI/LLM Coding Companion

This chapter explores how large language models (LLMs) like ChatGPT can assist with data engineering tasks—from rapid code generation to automating complex transformations. It also highlights the potential risks and blind spots when relying too heavily on AI-generated code.

---

## 📌 What You’ll Learn

- Understanding the coding companion mental model
- Key benefits: speed, prototyping, and error reduction
- Limitations: lack of context, hallucinations, and edge case failures
- Practical use cases with JSON and the Pagila PostgreSQL dataset
- Prompt engineering for Python and SQL generation
- Hands-on lab using ChatGPT, Jupyter, and pgAdmin

---

## ⚙️ Setup Requirements

To complete the exercises in this chapter, make sure you’ve installed:

- **PostgreSQL** with the **Pagila** sample dataset  
  → [Setup instructions](https://github.com/dave-melillo/data_eng_ai/blob/main/setup/postgres_setup.md)

- **Jupyter Lab** for Python notebooks  
  → [Setup instructions](https://github.com/dave-melillo/data_eng_ai/blob/main/setup/jupyter_setup.md)

- **OpenAI account** with API access or ChatGPT interface (preferably GPT-4)  
  → [OpenAI setup](https://github.com/dave-melillo/data_eng_ai/blob/main/setup/openai_setup.md)

---

## 🧪 Lab Exercises

### SQL (run in pgAdmin)

1. Query number of copies per film title using a **subquery**  
2. Create a **view** named `title_count` using the previous query  
3. Select film titles with **exactly 7 copies** from the view

### Python (run in Jupyter Lab)

Using the provided nested `orders` JSON:

4. Normalize the JSON into a DataFrame  
5. Calculate **total revenue per order** using tax-adjusted prices  
6. Identify the **top brand by total revenue**

---

## 📂 Files in This Folder

- `chapter_02_notebook.ipynb` – Python exercises and AI-generated solutions  
- `pagila-schema.sql` – Schema (tables, views, functions) for the Pagila database  
- `pagila-insert-data.sql` – Seed data for the Pagila database (load after the schema)  
- `sample_prompts.md` – Suggested prompts to feed ChatGPT  
- `chapter_02_lab_answers.md` – Reference solutions to SQL and Python exercises

---

## ✅ After Completing This Chapter

You’ll be able to:

- Use ChatGPT to accelerate SQL and Python coding tasks
- Spot where AI outputs can go wrong without schema awareness
- Use prompt iteration to refine AI responses
- Integrate AI into structured, testable workflows for data pipelines

---

> “AI is your sous-chef, not your replacement—still gotta taste the gumbo before you serve it.”

