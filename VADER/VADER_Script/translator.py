
import time
import pandas as pd
from langdetect import detect, LangDetectException
from deep_translator import GoogleTranslator
from tqdm import tqdm

import config


def detect_language(text: str) -> str:
    
    try:
        return detect(str(text))
    except LangDetectException:
        return "unknown"


def translate_to_english(text: str, src_lang: str) -> str:
    """Translate a single text into English; if unsuccessful, return to the original text"""
    if not text or not str(text).strip():
        return text
    for attempt in range(config.MAX_RETRIES):
        try:
            result = GoogleTranslator(source=src_lang, target="en").translate(str(text))
            time.sleep(config.TRANSLATE_DELAY)
            return result if result else text
        except Exception as e:
            if attempt < config.MAX_RETRIES - 1:
                time.sleep(1.5 * (attempt + 1))
            else:
                print(f"[WARNING] Translation failed (retried {config.MAX_RETRIES} times): {e}")
                return text
    return text


def detect_and_translate(df: pd.DataFrame, text_col: str) -> pd.DataFrame:
    """
    Perform language detection and translation on a DataFrame.
    Add new columns: detected_lang, text_for_varder
    """
    tqdm.pandas(desc="Language detection")
    df["detected_lang"] = df[text_col].progress_apply(detect_language)

    print(f"\nLanguage distribution detected：\n{df['detected_lang'].value_counts().to_string()}\n")

    translated = []
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Translate non-English texts"):
        lang = row["detected_lang"]
        text = row[text_col]
        if lang in ("en", "unknown") or not str(text).strip():
            translated.append(str(text) if pd.notna(text) else "")
        else:
            translated.append(translate_to_english(text, lang))

    df["text_for_vader"] = translated
    return df
