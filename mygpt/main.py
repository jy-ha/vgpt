from . import code_gen
from .core_api import gpt3_text_completion


def ask_simple_question(text):
    text = text.strip()
    answer = gpt3_text_completion(text, "text-davinci-003", 256, 0.4)
    return answer


def is_excutable_command(text):
    text = text.strip()
    text = """Decide prompt is either excutable command(Y) using internet and computer or not(N).

Prompt: Find how to get to the library.
Decision: Y

Prompt: I like an apple.
Decision: N

Prompt: what is color of the sky
Decision: Y

Prompt: %s\n
Decision: """ % text
    answer = gpt3_text_completion(text, "text-babbage-001", 256, 0.2)
    if answer == "N":
        return False
    return True


def create_code(quest):
    quest = quest.strip()

    # 1. 코드 템플릿 생성 (함수 기반)
    # code_template = generate_template(quest)
    code_template = """while True:
    # Generate Python code
    code = generate_code_using_openai_api()

    # Save file
    save_file(code)

    # Execute
    output = execute_code(code)

    # Evaluate
    result = evaluate_output(output)

    # Fix
    if result != 'success':
        code = fix_code(code)"""

    # 2. 생성해야할 함수 목록 생성
    #undefined_functions = extract_functions(code_template)
    undefined_functions = ["generate_code_using_openai_api", "save_file", "execute_code", "evaluate_output", "fix_code"]
    
    for undefined_function in undefined_functions:
        # 3. 개별 함수 코드 생성
        sub_functions = code_gen.recursive_function_generation(code_template, undefined_function)
        
        # 4. 개별 함수 코드 조합
        pass

    # 6. 최종 함수 생성
    return


# DEBUG
if __name__ == "__main__":
    # list_models()
    commands = [
        "Continuous loop to Generate, SaveFile, Excute, Evaluate, and Fix Python codes using openai API.",
        # "I want to go to the library.",
        # "let me know todays news.",
        # "search and read todays news.",
        # "write a letter to my friend.",
        # "call my mom",
        # "how to get to the city hall",
        # "crash the car",
    ]
    for text in commands:
        # if is_excutable_command(text, model="text-babbage-001"):
        command = create_code(text)
        # text-davinci-003   code-davinci-002   text-curie-001
        # command = gpt3_request_text_completion(text, model="text-davinci-003", max_tokens=1024)
        # print("====================================")
        # print(text)
        # print(command)