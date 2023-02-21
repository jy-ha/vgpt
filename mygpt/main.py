from .core_api import gpt3_text_completion


def ask_simple_question(text):
    text = text.strip()
    answer = gpt3_text_completion(text, "text-davinci-003", 256, 0.4)
    return answer


def is_excutable_command(text):
    text = text.strip()
    text = (
        """Decide prompt is either excutable command(Y) using internet and computer or not(N).

Prompt: Find how to get to the library.
Decision: Y

Prompt: I like an apple.
Decision: N

Prompt: what is color of the sky
Decision: Y

Prompt: %s\n
Decision: """
        % text
    )
    answer = gpt3_text_completion(text, "text-babbage-001", 256, 0.2)
    if answer == "N":
        return False
    return True
