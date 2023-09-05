import json
import re

def parse_using_re(input_string, str):
    pattern = r"'" + re.escape(str) + r"': '(.*?)', '"
    match = re.search(pattern, input_string)
    if match:
        parsed_data = match.group(1)
        return parsed_data
