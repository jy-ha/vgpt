import traceback

from .core_api import gpt3_text_completion


def generate_template(text):
    text = (
        """Generate Python code to return an answer for the prompt or excute the prompt.
If code is too long or fuctionally seperatable, using custom function name. You don't have to define it.
Prompt: %s\n\n"""
        % text
    )
    answer = gpt3_text_completion(text, "text-davinci-003", 1024, 0.5)
    return answer


def extract_functions(text):
    text = (
        """Find and List undefined functions from the Python code and join string with ','.
If there is no undefined function, say 'no'.
Prompt: %s
Undefined functions: """
        % text
    )
    answer = gpt3_text_completion(text, "text-davinci-003", 512, 0.5)
    if answer == "no":
        return []
    answer = answer.split(",")
    return answer


def generate_function(code_template, function_name):
    text = """Define proper Python function '%s' for a given code.
If code is too long or fuctionally seperatable, using custom function name. You don't have to define it.
Entire code:\n%s\n\n""" % (
        function_name,
        code_template,
    )
    answer = gpt3_text_completion(text, "text-davinci-003", 1024, 0.5)
    return answer


def recursive_function_generation(code_template, function_name):
    function_list = [generate_function(code_template, function_name)]
    undefined_functions = extract_functions(function_list[0])
    for undefined_function in undefined_functions:
        sub_function = recursive_function_generation(
            function_list[0], undefined_function
        )
        function_list.append(sub_function)

    # concat sub_functions
    final_function = "\n\n".join(function_list)

    # Evaluate generated function
    try:
        exec(final_function)
    except Exception:
        print(traceback.format_exc())

    return final_function


def create_code(quest):
    quest = quest.strip()

    # 1. Create code template
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

    # 2. Extract undefined functions from code template
    # undefined_functions = extract_functions(code_template)
    undefined_functions = [
        "generate_code_using_openai_api",
        "save_file",
        "execute_code",
        "evaluate_output",
        "fix_code",
    ]

    for undefined_function in undefined_functions:
        # 3. generate each function
        sub_function = recursive_function_generation(code_template, undefined_function)

    # 6. Create Final code
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
