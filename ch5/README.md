# Lab: Using the OpenAI API in Data Engineering Workflows

## **Overview**
This chapter explores how to integrate the OpenAI API into data engineering workflows, moving beyond the ChatGPT GUI to programmatic AI-driven analysis. The focus is on extracting news articles using **NewsAPI**, preprocessing the data, and performing **sentiment analysis** using the **OpenAI Chat Completions API**. The results are then normalized and integrated into a structured dataset.

## **Listings**
The following are the Python code listings included in this chapter, numbered according to their section:

- **Listing 5.1** - Extracting news articles using **NewsAPI**.
- **Listing 5.2** - Preprocessing extracted articles for AI analysis.
- **Listing 5.3** - Sending article content to OpenAI’s API for **sentiment analysis**.
- **Listing 5.4** - Normalizing API responses to return structured **Positive, Neutral, or Negative** values.
- **Listing 5.5** - Updating the **DataFrame** with AI-generated sentiment scores.

Each listing provides **step-by-step explanations** with inline comments.

## **Requirements**
Before running the scripts, ensure you have the following Python libraries installed:  
`requests`, `pandas`, and `openai`.  

Additionally, you will need API keys for both **NewsAPI** and **OpenAI**:

- **NewsAPI Key**: Get it from [NewsAPI.org](https://newsapi.org)
- **OpenAI API Key**: Get it from [OpenAI Platform](https://platform.openai.com)

Set your API keys in the respective Python files before execution.

## **Execution Flow**
1. **Extract news articles** (Listing 5.1)
2. **Preprocess the text** (Listing 5.2)
3. **Perform sentiment analysis** using OpenAI (Listing 5.3)
4. **Normalize API responses** (Listing 5.4)
5. **Store sentiment scores in a DataFrame** (Listing 5.5)
6. **View structured sentiment analysis results**

---

### **Example Output**
After running the pipeline, the final DataFrame should look like this:

| Title                                     | Sentiment  |
|-------------------------------------------|------------|
| "Beijing unveils plans to boost..."       | Neutral    |
| "Jahresrückblick in Ostdeutschland..."    | Neutral    |
| "The 'godfather' of AI is backing..."     | Negative   |
| "Tesla stock's bumpy road through 2024..."| Positive   |
| "Les voitures électriques les plus..."    | Neutral    |

*Note:* Sentiment results may vary due to AI inference variability.

## **Next Steps**
- Extend the pipeline to **store results in a database**.
- Integrate AI-based **sentiment trends over time**.
- Enhance prompts to **extract additional metadata**.

This chapter provides a **foundational AI-driven data pipeline**, allowing data engineers to automate real-world analysis. 🚀🔥
