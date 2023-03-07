from .core_api import gpt_chat_msg, gpt_chat

DEFAULT_TOP_OBJECTIVE = ""


class BetterChat:
    raw_context = []

    def __init__(self, top_objective=DEFAULT_TOP_OBJECTIVE):
        self.top_objective = top_objective

    def new_input(self, text):
        text = text.strip()
        new_message = {
            "role": "user",
            "content": text,
        }
        self.raw_context.append(new_message)

    def chat_classification(self, text):
        text = text.strip()
        # 발화 의도 파악 (의문문, 명령문, 평서문)
        text = (
            "Decide prompt is question:Q or statement:S or command:C\nPrompt: %s\nDecision: "
            % text
        )
        answer = gpt_chat(text, 2, 0.2)
        print("chat_classification: %s" % answer)
