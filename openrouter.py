import requests
import json

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer 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",  
  },
  data=json.dumps({
    "model": "z-ai/glm-4.5-air:free", 
    "messages": [
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ]
  })
)
print(response.json())