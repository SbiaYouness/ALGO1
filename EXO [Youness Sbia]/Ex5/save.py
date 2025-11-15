import json
from pathlib import Path

def save_game(data: dict, path: Path) -> None:
    with open(path, 'wt') as f:
        json.dump(data, f, indent=2, ensure_ascii=False) 

def load_game(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, 'rt') as f:
        data = json.load(f)
    return data
