
translit_map = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "yo",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "sch",
    "ъ": "",
    "ы": "y",
    "ь": "",
    "э": "ie",
    "ю": "yu",
    "я": "ya",
    " ": "_"
}

reverse_map = {v: k for k, v in translit_map.items() if v}

def quote(word: str) -> str:
    result = []
    for char in word.lower():
        result.append(translit_map.get(char, char))
    return ''.join(result)

def unquote(hashed: str) -> str:
    result = []
    i = 0
    while i < len(hashed):
        found = False
        for length in [3, 2, 1]:  # Проверяем самые длинные комбинации первыми
            part = hashed[i:i+length]
            if part in reverse_map:
                result.append(reverse_map[part])
                i += length
                found = True
                break
        if not found:
            result.append(hashed[i])
            i += 1
    return ''.join(result)