import os

def get_file_content(file):
    if not os.path.isfile(file):
        return None

    with open(file, 'r') as f:
        return f.read()

def nice_token_print(extra, tokens):
    print(end = extra)
    for token in tokens:
        t = token[0].replace('\n', '\\n')
        print(end = f"({token[1]}, '{t}') ")
    print()
