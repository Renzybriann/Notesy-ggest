import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
GEMINI_API_URL = os.getenv("GEMINI_API_URL")

def generate_subtasks_with_gemini(content: str):
    headers = {
        "Content-Type": "application/json",
    }

    data = {
    "contents": [
        {
            "role": "user",
            "parts": [
                {
                    "text": f"Generate exactly 3 clear and concise subtasks for this note: '{content}'. Return them as a bullet point list. Do not include any introduction or explanation—only the list."
                }
            ]
        }
    ]
}


    response = requests.post(GEMINI_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        subtasks = [line.strip("-• ") for line in text.split("\n") if line.strip()]
        return subtasks
    else:
        print(response.text)
        return ["Failed to generate subtasks"]
