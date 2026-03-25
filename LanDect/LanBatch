from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(detect_language, df[text_column]))
df["detected_lang"] = results
