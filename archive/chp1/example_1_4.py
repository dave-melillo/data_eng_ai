import openai

# Define the prompt
prompt = "Extract color, size, and tone from this text: 'A large red banner with bold text, symbolizing power.'"

# Call OpenAI's API (replace 'your-api-key' with an actual API key)
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)

# Print the AI-generated response
print(response["choices"][0]["message"]["content"])