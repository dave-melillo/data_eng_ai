
# **Data Engineering with AI in a Month of Lunches**  

## **Overview**  
🚀 *Data Engineering with AI in a Month of Lunches* is a practical, hands-on guide to integrating **AI and large language models (LLMs)** into modern **data engineering workflows**. Designed for data professionals, this book explores how AI can **automate, optimize, and enhance** key data engineering tasks—from **writing SQL queries** to **data cleaning, transformation, and generation**.  

This repo contains all the **code listings, labs, and resources** that accompany the book.  

## **📖 Book Structure**  

### **🟢 Part 1: Core Concepts of Data Engineering with AI**  
Lays the foundation for understanding **AI’s role in data engineering**, key benefits, and prompt engineering techniques for SQL and Python workflows.  
- Understanding the data engineer's new relationship with AI  
- Zero-shot, few-shot, chain-of-thought, and other prompting styles  
- Coding SQL and Python with AI  
- Using the OpenAI API inside data pipelines  
- **Includes labs on SQL, Python, and AI-driven sentiment analysis**

### **🟠 Part 2: Data Cleaning and Transformation Pipelines with AI**  
Explores AI-assisted approaches to improving **data quality**, normalization, and transformation.  
- Detecting inconsistencies and fixing missing data  
- Standardizing formats and applying transformations  
- Building production-grade cleaning workflows with AI support  

### **🔵 Part 3: Generating Data with AI**  
Demonstrates how AI can help **create new datasets** by augmenting existing ones or extracting unstructured data from the web.  
- AI-powered web scraping techniques  
- Structuring messy text into clean tabular format  
- Strategies for enriching data automatically  

### **🟣 Part 4: Agentic Workflows in Data Engineering with AI**  
Introduces **agentic workflows**, where AI becomes an autonomous operator in your pipeline—making decisions, activating APIs, and triggering next steps.  
- Introduction to agentic workflows for data engineers  
- Generating subject matter expertise with AI  
- Decision trees, prompt chains, and data activation  
- Practical application: AI-driven outreach for marketing and sales  

Merci for the detail, cher—now we cookin’ with some real roux. Here’s the corrected **How to Use This Repo** section that reflects the repo’s structure with folders for each chapter, subfolders, notebooks, and the setup guide:



## **💡 How to Use This Repo**  
This repo mirrors the structure of the book, with **one main folder per chapter**, and supporting materials organized for easy access and hands-on learning. Here's how it's laid out:  

- Each **chapter folder** contains:
  - `images/` – Figures and visuals used in the chapter  
  - `listings/` – Numbered code listings referenced in the book  
  - `notebooks/` –  
    - `GUIDE` notebook: A consolidated walkthrough of the chapter’s concepts as a complete pipeline  
    - `LAB` notebook: Deep dive into the chapter lab, with line-by-line answers and explanations  
  - `setup/` – Any chapter-specific configs or data assets  
  - `README.md` – A short intro and instructions tailored to the chapter  

- The **top-level `setup/` folder** contains all **global installation instructions** for:
  - Tools and environments (e.g., Python, Jupyter, virtualenvs)  
  - API setup (e.g., OpenAI, NewsAPI)  
  - Credential management (e.g., `.env` files)  

To get started:  
1. Follow the global setup guide in `/setup` to configure your environment.  
2. Pick a chapter and explore the `GUIDE` notebook first to understand the concepts.  
3. Dive into the `LAB` notebook to practice with the code.  
4. Use the `listings/` folder to reference any specific code snippets from the book.  

> 💬 **Pro tip:** Notebooks are meant to be tweaked—don’t be shy. Adjust prompts, try new APIs, and modify pipelines to fit your real-world projects.


## **📌 Prerequisites**  
- Python 3.x  
- OpenAI API key (for LLM integrations)  
- `pandas`, `tqdm`, `openai`, `requests`, and other dependencies (install via `requirements.txt`)  