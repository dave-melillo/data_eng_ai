# Listing 12.5 Agent 3: AI extraction
import openai

EXTRACTION_PROMPT = """You are a product data extraction assistant.
Given the text of a product web page, extract these fields:
- product_name, brand_name, description, price, weight,
  primary_image_url, category
Rules:
- Only extract values explicitly present in the text.
- Use null for anything you cannot find; never guess.
- For price, prefer the current/sale price with its symbol.
- For weight, include the unit (lbs, oz, kg, g).
"""  #A


@with_retries(max_attempts=2, exceptions=(openai.OpenAIError,))  #B
def extract_product(cleaned_text: str) -> ProductExtraction:  #C
    """Agent: pull structured fields from cleaned text."""
    response = openai.beta.chat.completions.parse(  #D
        model="gpt-4o",
        messages=[
            {"role": "system", "content": EXTRACTION_PROMPT},
            {"role": "user", "content": cleaned_text[:8000]},  #E
        ],
        response_format=ProductExtraction,  #F
    )
    return response.choices[0].message.parsed  #G

#A The extraction rules from Chapter 11, kept deliberately strict
#B Retry once on transient API errors; extraction is the costly call
#C The agent: clean text in, a ProductExtraction object out
#D Use the more capable model for the field-level reasoning
#E Cap input length to control tokens and cost
#F The Pydantic schema is the contract the model must satisfy
#G Return the parsed object for validation in the next agent
