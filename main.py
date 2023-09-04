with open('/home/pf4/Documents/GitHub/sulfur_lang/src/parser.c', 'r') as f:
    code_to_format = f.read()

split_things = {
    '(': 'parenthesis',
    ')': 'parenthesis',
    '{': 'curly_bracket',
    '}': 'curly_bracket',
    ';': 'semicolon',
    ',': 'comma',
    ' ': 'space',
    '\n': 'newline',
    '\t': 'tab',
    '!': 'exclamation',
    '<': 'less_than',
    '>': 'greater_than',
    '=': 'equal',
    '+': 'plus',
    '-': 'minus',
    '*': 'asterisk',
    '/': 'slash',
    '%': 'percent',
    '&': 'ampersand',
    '|': 'pipe',
    '^': 'caret',
    '~': 'tilde',
    '[': 'square_bracket',
    ']': 'square_bracket',
    '?': 'question_mark',
    ':': 'colon',
    '"': 'double_quote',
    '\'': 'single_quote',
    '\\': 'backslash',
    '#': 'hash',
    '.': 'dot'
}

keywords = ["for", "if", "while", "do", "else"]
space_with = ["less_than", "greater_than", "equal", "exclamation"]
space_when_duplicated = ["pipe", "ampersand"]

split_at = set(split_things.keys())

def smart_split(code):
    tokens = []
    current_token = ''
    for char in code:
        if char in split_at:
            if current_token:
                tokens.append(current_token)
                current_token = ''
            tokens.append(char)
        else:
            current_token += char
    if current_token:
        tokens.append(current_token)
    return tokens

def add_type(tokens):
    for i, token in enumerate(tokens):
        if token in split_things:
            tokens[i] = (token, split_things[token])
        else:
            tokens[i] = (token, 'word')
    return tokens

def join_strings(tokens):
    in_string = False
    string = ''
    pos = 0
    for i, token in enumerate(tokens):
        if token[1] == 'double_quote':
            if not in_string:
                if (i > 0 and tokens[i-1][1] == 'backslash'):
                    continue
                in_string = True
                string = token[0]
                pos = i
            else:
                string += token[0]
                in_string = False
                tokens[pos] = (string, 'string')
                # move the rest of the tokens back
                for _ in range(i-pos):
                    tokens[pos+1] = None
                    pos += 1
                string = ''
        elif in_string:
            string += token[0]
    tokens = [t for t in tokens if t is not None]
    return tokens

def join_short_comments(tokens):
    in_comment = False
    comment = ''
    pos = 0
    for i, token in enumerate(tokens):
        if token[1] == 'slash' and tokens[i+1][1] == 'slash' and not in_comment:
            in_comment = True
            comment = token[0]
            pos = i
        elif token[1] == 'newline' and in_comment:
            in_comment = False
            tokens[pos] = (comment, 'short_comment')
            # move the rest of the tokens back
            for _ in range(i-pos - 1):
                tokens[pos+1] = None
                pos += 1
            comment = ''
        elif in_comment:
            comment += token[0]
    tokens = [t for t in tokens if t is not None]
    return tokens

def join_long_comments(tokens):
    in_comment = False
    comment = ''
    pos = 0
    for i, token in enumerate(tokens):
        if token[1] == 'slash' and tokens[i+1][1] == 'asterisk' and not in_comment:
            in_comment = True
            comment = token[0]
            pos = i
        elif in_comment and tokens[i][1] == 'slash' and tokens[i-1][1] == 'asterisk':
            in_comment = False
            comment += token[0]
            tokens[pos] = (comment, 'long_comment')
            # move the rest of the tokens back
            for _ in range(i-pos):
                tokens[pos+1] = None
                pos += 1
            comment = ''
        elif in_comment:
            comment += token[0]
    tokens = [t for t in tokens if t is not None]
    return tokens

def remove_space(tokens):
    tokens = [t for t in tokens if t[1] != 'space' and t[1] != 'tab']
    return tokens

def remove_newline(tokens):
    tokens = [t for t in tokens if t[1] != 'newline']
    return tokens

def format_short_comments(tokens):
    for i, token in enumerate(tokens):
        if token[1] == 'short_comment' and token[0][2] != ' ':
            tokens[i] = (token[0][:2] + ' ' + token[0][2:], 'short_comment')
    return tokens

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
    multi_nl = False
    generated_code = ''
    for i, token in enumerate(tokens[:-1]):
        if token[1] == 'newline':
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
                if all([t == ' ' for t in generated_code[-4:]]):
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
        elif (token[1] == 'semicolon' and in_for):
            generated_code += ' '

    return generated_code


def nice_print(extra, tokens):
    print(end = extra)
    for token in tokens:
        t = token[0].replace('\n', '\\n')
        print(end = f"({token[1]}, '{t}') ")
    print()

code_to_format += '\n'
split = smart_split(code_to_format)
print("Split: ", split)

split = add_type(split)
nice_print("Split with types: ", split)

split = join_long_comments(split)
nice_print("Split with long comments: ", split)

split = join_short_comments(split)
nice_print("Split with short comments: ", split)

split = join_strings(split)
nice_print("Split with strings: ", split)

split = remove_space(split)
nice_print("Split without space: ", split)

split = format_short_comments(split)
print(f"\n---\n{reform(split)}")
