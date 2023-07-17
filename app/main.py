import re
from timeit import default_timer

import Levenshtein

from lev_engine import calc_lev

with open("dictionary.dat", "r") as file:
    dictionary = [line[:-1] for line in file.readlines()]
dictionary_set = set(dictionary)


def tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text)


def get_distance(word1, word2, max_distance=0, engine="naive") -> int | None:
    if engine == "levenshtein":
        distance = Levenshtein.distance(word1, word2)
        return (
            Levenshtein.distance(word1, word2)
            if not max_distance or distance <= max_distance
            else None
        )
    elif engine == "naive":
        return calc_lev(word1, word2, max_distance)


def prefilter(word1, word2, max_distance):
    if abs(len(word1) - len(word2)) > max_distance:
        return True
    if len(set(word1) ^ set(word2)) > max_distance / 2:
        return True
    return False


def get_typos(
    text: str, max_distance: int = 0, num_candidates: int = 3, engine: str = "naive"
) -> dict:
    start = default_timer()
    tokens: list[str] = tokenize(text)
    typos: dict[str, list[dict[str, int]]] = {}

    for token in tokens:
        token = token.lower()

        if token in dictionary_set:
            continue

        candidates = []
        for word in dictionary:
            if max_distance and prefilter(token, word, max_distance):
                continue
            if distance := get_distance(token, word, max_distance, engine):
                candidates.append({word: distance})

        if candidates:
            candidates = sorted(candidates, key=lambda option: list(option.values())[0])
            typos[token] = candidates[:num_candidates]
        else:
            typos[token] = []

    return {
        "processing_time, s": f"{default_timer() - start:.2f}",
        "typos": typos,
        "parameters": {
            "max_distance": max_distance,
            "num_candidates": num_candidates,
            "engine": engine,
        },
    }


if __name__ == "__main__":
    print(get_distance("привет", "пирвет", engine="naive"))
    text = "Яп ришёл к тебе с примммммм, расказать что сонце встало"
    print(
        get_typos(text, max_distance=3, num_candidates=5, engine="levenshtein")
    )
    print(get_typos(text, max_distance=3, num_candidates=5, engine="naive"))
