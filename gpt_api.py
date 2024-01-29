from openai import OpenAI

client = OpenAI(api_key="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")

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)
print(response['choices'])