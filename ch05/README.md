
# 📘 Chapter 5: Using the OpenAI API in Data Workflows

In this chapter, we take a pivotal step in your AI journey—embedding language models directly into your data pipeline. Rather than using an AI assistant on the side, you're now calling it from within your code to automate enrichment tasks like sentiment analysis.

### 🧠 What This Chapter Covers:
- Extracting live article data using [NewsAPI](https://newsapi.org)
- Preprocessing article content for structured analysis
- Using the OpenAI Chat Completions API (via Python SDK) for sentiment scoring
- Prompting for both **categorical** (e.g., “Positive”) and **numerical** (e.g., `0.5`) sentiment labels
- Logging and consolidating results into a clean, pipeline-ready DataFrame

---

## 💻 Companion Notebook

> **🧪 Want to see how every piece of code runs, line-by-line?**  
> Check out the **Chapter 5 Lab Jupyter Notebook** in this repo.  
> It contains complete, working implementations of every listing in the chapter, including:
- `extract_articles()`
- `preprocess_articles()`
- `perform_sentiment_analysis()`
- `update_with_sentiment()`

The notebook also includes enhanced prompts, logging examples, and alternate configurations to help you tweak, experiment, and explore.

---

## 🚀 Try It Yourself

Use the notebook to:
1. Query news articles for companies like **Tesla**, **NVIDIA**, or **Disney**.
2. Send that data to OpenAI’s API and receive clean sentiment labels.
3. Aggregate your results for quick insight—or build dashboards, if you’re feelin’ fancy.

By the end of this chapter, you’ll have a working AI component in your stack. It won’t just assist you—it’ll *be part of the pipeline*. ✨

---

## 🔐 Setup Checklist

- ✅ API key from [NewsAPI](https://newsapi.org)
- ✅ API key from [OpenAI](https://platform.openai.com/)
- ✅ `.env` file storing `OPENAI_API_KEY` and `NEWS_API_KEY`
- ✅ Packages installed: `openai`, `requests`, `pandas`, `dotenv`

For setup help, refer to the `env_setup.md` file in the root of the repo.

---

## 🧪 Lab Summary

The Chapter 5 lab reinforces your new skills:
- Swap the query from “Tesla” to another company.
- Modify the prompt to return **numerical sentiment scores**.
- Scale up to process **50 articles** and summarize results with `.value_counts()` or `.mean()`.

Refer to the **Chapter 5 Lab Notebook** for:
- Full solutions
- Prompt tuning examples
- Sample output from real news data

---

This chapter marks the moment where AI stops being a novelty and starts becoming a native tool in your engineering toolbox. Let's go build something smart. 🔧🧠
