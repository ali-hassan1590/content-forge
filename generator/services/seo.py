"""Readability and local SEO helpers."""


def flesch_reading_ease(text: str) -> float:
    """Flesch Reading Ease (higher = easier). Typical blog target: 60–70."""
    sentences = max(text.count(".") + text.count("!") + text.count("?"), 1)
    words = text.split()
    word_count = max(len(words), 1)
    syllables = sum(_count_syllables(w) for w in words)
    if word_count == 0 or sentences == 0:
        return 0.0
    return round(
        206.835 - 1.015 * (word_count / sentences) - 84.6 * (syllables / word_count),
        1,
    )


def _count_syllables(word: str) -> int:
    word = word.lower().strip(".,!?;:'\"")
    if len(word) <= 3:
        return 1
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if word.endswith("e") and count > 1:
        count -= 1
    return max(count, 1)


def readability_label(score: float) -> str:
    if score >= 90:
        return "Very Easy"
    if score >= 80:
        return "Easy"
    if score >= 70:
        return "Fairly Easy"
    if score >= 60:
        return "Standard"
    if score >= 50:
        return "Fairly Difficult"
    if score >= 30:
        return "Difficult"
    return "Very Difficult"
