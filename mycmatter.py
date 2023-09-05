from optparse import OptionParser

import src.tokentools as tt
import src.gentools as gt
import src.reform as frm


parser = OptionParser()

# parser.add_option("-d", "--debug", dest="debug", default=False, action="store_true", help="Debug mode")
parser.add_option("-o", "--output", dest="output", default="stdout", help="Output file")
parser.add_option("-i", "--input", dest="input", default="example.c", help="Input file")
parser.add_option("-m", "--mode", dest="mode", default="full", help="Mode of analysis", choices=["lite", "full"])
parser.add_option("-s", "--codestyle", dest="codestyle", default="compact", help="Code style", choices=["compact", "aerial"])


options = parser.parse_args()[0]

code_to_format = gt.get_file_content(options.input) + '\n'
if code_to_format is None:
    print(f"Error: File {options.input} not found")
    exit(1)

split = tt.smart_split(code_to_format)
print("Split: ", split)

split = tt.add_type(split)
gt.nice_token_print("Split with types: ", split)

split = tt.join_long_comments(split)
gt.nice_token_print("Split with long comments: ", split)

split = tt.join_short_comments(split)
gt.nice_token_print("Split with short comments: ", split)

split = tt.join_strings(split)
gt.nice_token_print("Split with strings: ", split)

split = tt.remove_space(split)
gt.nice_token_print("Split without space: ", split)

split = tt.format_short_comments(split)
gt.nice_token_print("Split with formatted short comments: ", split)


print(f"\n---\n{frm.reform(split)}")
