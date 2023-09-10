from optparse import OptionParser

import src.tokentools as tt
import src.gentools as gt
import src.reform as frm


parser = OptionParser()

# parser.add_option("-d", "--debug", dest="debug", default=False, action="store_true", help="Debug mode")
parser.add_option("-o", "--output", dest="output", default="stdout", help="Output file")
parser.add_option("-i", "--input", dest="input", default="example.c", help="Input file")
parser.add_option("-n", "--nlmode", dest="nlmode", default="keep", help="Newline mode", choices=["keep", "compact", "aerial"])
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help="Verbose mode")

options = parser.parse_args()[0]

code_to_format = gt.get_file_content(options.input) + '\n'
if code_to_format is None:
    print(f"Error: File {options.input} not found")
    exit(1)

split = tt.smart_split(code_to_format)
split = tt.add_type(split)
split = tt.join_long_comments(split)
split = tt.join_short_comments(split)
split = tt.join_strings(split)
split = tt.remove_space(split)
split = tt.format_short_comments(split)
if options.verbose:
    gt.nice_token_print("TOKENS", split)


print(f"\n---\n{frm.reform(split)}")
