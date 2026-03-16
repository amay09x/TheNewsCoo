import requests
from config import TRANSLATOR_KEY, TRANSLATOR_REGION

def translate(text, lang_code):

    url = f"https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to={lang_code}"

    headers = {
        "Ocp-Apim-Subscription-Key": TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": TRANSLATOR_REGION,
        "Content-type": "application/json",
    }

    resp = requests.post(url, headers=headers, json=[{"text": text}])

    translated = resp.json()[0]["translations"][0]["text"]

    return translated