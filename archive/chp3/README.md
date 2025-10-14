# Chapter 3: Using a Coding Companion with SQL  

## Overview  
This chapter covers techniques for using AI coding companions like ChatGPT to generate and refine SQL queries effectively. Key topics include:  

- Zero-shot prompts (no schema context, AI infers structure)  
- Few-shot prompts (providing schema details and sample data)  
- One-shot prompts (building on previous queries for iterative refinement)  
- Using Common Table Expressions (CTEs) for complex queries  

## SQL Listings  
| File Name        | Description |
|-----------------|-------------|
| `example_3_1.sql` | Calculates total revenue per customer (Zero-Shot Prompt) |
| `example_3_2.sql` | Filters only active customers when calculating revenue (Few-Shot Prompt) |
| `example_3_3.sql` | Filters for customers with total revenue above $200 (One-Shot Prompt) |
| `example_3_4.sql` | Includes customer location in revenue calculation (Few-Shot Prompt) |
| `example_3_5.sql` | Uses a CTE to calculate total revenue in the last 30 days (Few-Shot Prompt) |


