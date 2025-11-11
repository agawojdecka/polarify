from pathlib import Path

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def get_prompt(file_name: str) -> str:
    file_path = PROMPTS_DIR / file_name
    with open(file_path, "r", encoding="utf-8") as f:
        prompt_str = f.read()
    return prompt_str
