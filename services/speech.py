import azure.cognitiveservices.speech as speechsdk
from config import SPEECH_KEY, SPEECH_REGION

voice_map = {
    "hi": "hi-IN-MadhurNeural",
    "fr": "fr-FR-DeniseNeural",
    "de": "de-DE-KatjaNeural",
    "es": "es-ES-ElviraNeural",
    "ja": "ja-JP-NanamiNeural",
}

def speak(text, lang):

    cfg = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)

    cfg.speech_synthesis_voice_name = voice_map.get(lang, "en-US-JennyNeural")

    synth = speechsdk.SpeechSynthesizer(speech_config=cfg)

    synth.speak_text_async(text).get()