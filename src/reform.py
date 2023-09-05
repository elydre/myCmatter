keywords = ["for", "if", "while", "do", "else"]
space_with = ["less_than", "greater_than", "equal", "exclamation"]
space_when_duplicated = ["pipe", "ampersand"]

def nl_at_end(code):
    slen = len(code)
    while slen > 0:
        if code[slen-1] == '\n':
            return True
        elif code[slen-1] != ' ':
            return False
        slen -= 1
    return True

def reform(tokens):
    indent_level = 0
    in_for = False
    in_include = False
    multi_nl = False
    generated_code = ''
    for i, token in enumerate(tokens[:-1]):
        if token[1] == 'hash' and (i == 0 or tokens[i-1][1] == 'newline') and tokens[i+1][1] == 'word' and tokens[i+1][0] == 'include':
            in_include = True
        if token[1] == 'newline':
            in_include = False
            if multi_nl or not nl_at_end(generated_code):
                generated_code += '\n'
                generated_code += '    '*indent_level
            if multi_nl == False:
                multi_nl = True
            continue
        multi_nl = False

        if token[1] == 'curly_bracket':
            in_for = False

            if token[0] == '{':
                indent_level += 1
            else:
                if all(t == ' ' for t in generated_code[-4:]):
                    generated_code = generated_code[:-4]
                indent_level -= 1

            generated_code += token[0]
            generated_code += '\n'
            generated_code += '    '*indent_level
            continue

        if token[1] == 'word' and token[0] == 'for':
            in_for = True

        else:
            for t in space_when_duplicated:
                if token[1] == t and tokens[i+1][1] == t:
                    generated_code += ' '
                    break

        if token[1] == "minus" and tokens[i+1][1] == "equal":
            generated_code += ' '
        generated_code += token[0]
        if in_include:
            if token[1] == 'word' and token[0] == 'include':
                generated_code += ' '
            continue
        if token[1] == "word" and tokens[i+1][1] == "word":
            generated_code += ' '
        elif token[1] == "word" and tokens[i+1][1] == "string":
            generated_code += ' '
        elif token[1] == "word" and token[0] in keywords:
            generated_code += ' '
        elif token[1] == "comma":
            generated_code += ' '
        elif token[1] == "word" and tokens[i+1][1] in space_with:
            generated_code += ' '
        elif token[1] in space_with and tokens[i+1][1] == "word":
            generated_code += ' '
        elif any(i and tokens[i - 1][1] == t and token[1] == t for t in space_when_duplicated):
            generated_code += ' '
        elif (token[1] == "parenthesis" and token[0] == ")") and (tokens[i+1][1] == "curly_bracket" and tokens[i+1][0] == "{"):
            generated_code += ' '

        if (token[1] == 'semicolon' and not in_for) or token[1] == 'short_comment' or token[1] == 'long_comment':
            generated_code += '\n'
            generated_code += '    '*indent_level
        elif token[1] == 'semicolon':
            generated_code += ' '

    return generated_code
