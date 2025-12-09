from app.utils.prompts import PromptTypeE, get_prompt


def test_get_prompt():
    assert get_prompt(PromptTypeE.SYSTEM_INSTRUCTIONS)[:17] == "You are an expert"
