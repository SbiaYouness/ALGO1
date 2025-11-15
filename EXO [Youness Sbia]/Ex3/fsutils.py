from pathlib import Path
import string
import unicodedata

def list_text_files(directory: Path) -> list[Path]:
    return sorted(directory.glob("*.txt"))

def read_all_files(files: list[Path]) -> list[tuple[Path, str]]:
    data = []
    for file_path in files:
        with open(file_path, 'rt') as f:
            data.append((file_path, f.read()))
    return data

def write_glossary(files: list[Path], output: Path) -> None:
    occ = {}
    unique_words_all = set()
    for file_path in files:
        with open(file_path, 'rt', encoding='utf-8') as f:
            data = f.read()
        lowered = data.lower()
        decomposed = unicodedata.normalize("NFD", lowered)
        no_accents = ''.join(ch for ch in decomposed if unicodedata.category(ch) != 'Mn')
        cleanedtext = ''.join(ch for ch in no_accents if ch not in string.punctuation)
        words = cleanedtext.split()
        for w in words:
            occ[w] = occ.get(w, 0) + 1
        unique_words_all.update(words)
    with open(output, 'wt', encoding='utf-8') as out:
        for w in sorted(unique_words_all):
            out.write(f"{w}:{occ[w]}\n")

