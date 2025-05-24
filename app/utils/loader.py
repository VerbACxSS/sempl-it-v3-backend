from typing import List

from . import fs_utils


def load_prompt(prompt_name: str) -> str:
    return fs_utils.read_file(f'./assets/prompts/{prompt_name}.md')


def load_connectives() -> List[str]:
    hard_connectives = [c.lower() for c in fs_utils.read_file('./assets/hard_connectives.txt').split('\n')]
    hard_connectives = [c + "\\b" for c in hard_connectives if (not c.endswith("*")) or (not c.endswith("]"))]
    hard_connectives = [c.replace("a\\w*", "(a|al|allo|alla|ai|agli|alle|all')\\b") for c in hard_connectives]
    hard_connectives = [c.replace("d\\w*", "(di|del|dello|dell'|della|dei|degli|delle|dal|dallo|dall'|dalla|dai|dagli|dalle')\\b") for c in hard_connectives]
    return hard_connectives