from src.resources import split_things

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
    tokens = [t for t in tokens if t[1] not in ['space', 'tab']]
    return tokens

def remove_newline(tokens):
    tokens = [t for t in tokens if t[1] != 'newline']
    return tokens

def format_short_comments(tokens):
    for i, token in enumerate(tokens):
        if token[1] == 'short_comment' and token[0][2] != ' ':
            tokens[i] = f'{token[0][:2]} {token[0][2:]}', 'short_comment'
    return tokens
