# utils/gemini_api.py
import requests
import config

API_KEY = config.GEMINI_API_KEY
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# def query_gemini(prompt):
#     headers = {"Content-Type": "application/json"}
#     data = {
#         "contents": [{"parts": [{"text": prompt}]}]
#     }
#     response = requests.post(GEMINI_ENDPOINT, headers=headers, json=data)

#     if response.status_code == 200:
#         return response.json()["candidates"][0]["content"]["parts"][0]["text"]
#     else:
#         raise Exception(f"Gemini API Error: {response.status_code} | {response.text}")


def query_gemini(prompt):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(GEMINI_ENDPOINT, headers=headers, json=data)

    if response.status_code == 200:
        json_response = response.json()
        try:
            content = json_response.get("candidates", [{}])[0].get("content", {})
            parts = content.get("parts", [])
            if parts and "text" in parts[0]:
                return parts[0]["text"]
            else:
                raise Exception("No 'text' found in Gemini response.")
        except Exception as e:
            raise Exception(f"Unexpected Gemini response structure: {e} | Full response: {json_response}")
    else:
        raise Exception(f"Gemini API Error: {response.status_code} | {response.text}")
