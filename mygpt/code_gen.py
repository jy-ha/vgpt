from .main import gpt3_text_completion


def generate_template(text):
    text = """Generate Python code to return an answer for the prompt or excute the prompt.
If code is too long or fuctionally seperatable, using custom function name. You don't have to define it.
Prompt: %s\n\n""" % text
    answer = gpt3_text_completion(text, "text-davinci-003", 1024, 0.5)
    return answer


def extract_functions(text):
    text = """Find and List undefined functions from the Python code and join string with ','.
If there is no undefined function, say 'no'.
Prompt: %s
Undefined functions: """ % text
    answer = gpt3_text_completion(text, "text-davinci-003", 512, 0.5)
    if answer == "no":
        return []
    answer = answer.split(",")
    return answer


def generate_function(code_template, function_name):
    text = """Define proper Python function '%s' for a given code.
If code is too long or fuctionally seperatable, using custom function name. You don't have to define it.
Entire code:\n%s\n\n""" % (function_name, code_template)
    # 평가도해야함
    answer = gpt3_text_completion(text, "text-davinci-003", 1024, 0.5)
    return answer


def recursive_function_generation(code_template, function_name):
    function_list = []
    function = generate_function(code_template, function_name)
    undefined_functions = extract_functions(function)
    for undefined_function in undefined_functions:
        sub_function = recursive_function_generation(function, undefined_function)
        function_list.extend(sub_function)
    return function_list
