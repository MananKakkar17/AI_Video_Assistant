import whisper
import os

_model=None

def load_model():

    global _model

    if _model is None:
        whisper_model = os.getenv("WHISPER_MODEL","small")
        print(f"loading model ...")
        _model=whisper.load_model(whisper_model)
        print("whisper model loaded successfully")

    
    return _model

def should_translate(language_or_translate=False) -> bool:
    if isinstance(language_or_translate, bool):
        return language_or_translate

    if language_or_translate is None:
        return False

    return str(language_or_translate).strip().lower() in {
        "translate",
        "translation",
        "english_translation",
        "to_english",
    }

def transcribe_chunk(chunk_path:str,translate:bool=False)-> str:

    model=load_model()

    task="translate" if translate else "transcribe"

    result=model.transcribe(chunk_path,task=task)

    return result['text']

def transcribe_all(chunks:list,language_or_translate=False):
    full_transcript=""
    translate = should_translate(language_or_translate)

    for i,chunk in enumerate(chunks):
        print(f"Transcribing chunk {i+1}")
        text=transcribe_chunk(chunk,translate=translate)

        full_transcript += text + " "
        print("Transcription completed")

    return full_transcript

