import re

def _normalize_text(text: str) -> str:
    """Нормализует текст для лучшего поиска"""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s@]', '', text)
    return text

def contains_bad_words(text: str) -> bool:
    """Проверяет наличие нецензурных слов"""
    bad_words = ['дурак', 'идиот', 'мудак', 'придурок', 'сволочь']
    normalized = _normalize_text(text)
    return any(bad_word in normalized for bad_word in bad_words)

