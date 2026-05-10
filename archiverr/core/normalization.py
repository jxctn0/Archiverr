import re



def normalize_text(value: str):
    value = value.lower().strip()
    value = re.sub(r"\(.*?remaster.*?\)", "", value)
    value = re.sub(r"feat\..*", "", value)
    value = re.sub(r"[^a-z0-9 ]", "", value)
    value = re.sub(r"\s+", " ", value)

    return value.strip()
