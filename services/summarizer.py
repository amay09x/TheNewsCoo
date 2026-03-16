from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from config import TEXT_KEY, TEXT_ENDPOINT

text_client = TextAnalyticsClient(
    endpoint=TEXT_ENDPOINT,
    credential=AzureKeyCredential(TEXT_KEY)
)

def summarize(text):
    poller = text_client.begin_extract_summary([text])
    result = poller.result()

    summary = ""
    for doc in result:
        if not doc.is_error:
            for s in doc.sentences:
                summary += s.text + " "

    return summary.strip()