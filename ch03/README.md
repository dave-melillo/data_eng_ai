# Chapter 3: Using a Coding Companion with SQL

This chapter explores how to use ChatGPT and other LLMs as coding companions for writing, debugging, and improving SQL queries. You’ll learn how to frame your prompts effectively and use advanced prompting strategies to handle complex SQL tasks with accuracy and consistency.

---

## 📘 What You'll Learn

- Crafting effective SQL prompts using zero-shot, few-shot, chain-of-thought, and other strategies
- Guiding AI through joins, subqueries, CTEs, and aggregations
- Uploading schema/data files to improve prompt accuracy
- Comparing multiple AI-generated solutions to validate correctness
- Improving SQL readability and maintainability with prompt engineering

---

## ⚙️ Setup Requirements

To complete the exercises in this chapter, make sure you’ve got:

- **PostgreSQL with Pagila dataset installed**  
  → [Postgres Setup](https://github.com/dave-melillo/data_eng_ai/blob/main/setup/postgres_setup.md)

- **pgAdmin** or another SQL client for running queries

- **ChatGPT** (preferably GPT-4) or an OpenAI API-enabled environment  
  → [OpenAI Setup](https://github.com/dave-melillo/data_eng_ai/blob/main/setup/openai_setup.md)

---

## 🧪 Prompting Techniques Covered

### 🔹 Zero-Shot Prompting
Give the model a single, plain-language instruction and test its ability to generate a SQL query without examples.

### 🔹 Few-Shot Prompting
Provide multiple example prompts to guide the model toward producing consistent, formatted SQL output—especially with CTEs.

### 🔹 Chain-of-Thought Prompting
Ask the AI to reason step-by-step before writing the query. This reveals assumptions and improves transparency.

### 🔹 Self-Consistency Prompting
Request two different solutions to the same problem and compare the results for reliability.

### 🔹 Tree-of-Thought Prompting
Guide the model to generate, evaluate, and choose from multiple approaches—then recommend the best one.


---

## 🧠 Lab Exercises

1. **Chain-of-Thought:**  
   Average number of rentals per customer (exclude customers with zero rentals)

2. **Few-Shot:**  
   Top five film categories by revenue using a report-style format

3. **Self-Consistency:**  
   Top five films with the longest average rental duration (two approaches)

---

## ✅ After This Chapter

You’ll be able to:

- Prompt ChatGPT to generate correct and readable SQL for complex queries
- Use structured approaches to improve accuracy and debuggability
- Compare AI-generated solutions and decide which is best
- Prepare for more advanced prompting and programmatic AI workflows later in the book

---

> “Prompting is half science, half art. Ask better, get better.”

