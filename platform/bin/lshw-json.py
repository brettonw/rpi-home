#! /usr/local/rpi_home/python3/bin/python3

# read the lshw text format and make a valid json (because the programmatic option in lshw  is broken)

import json
import re
import sys


def parse_lshw_output(lshw_text):
    stack = []

    def debug(line: str) -> None:
        indent = "  " * len(stack)
        # print(f"{indent}{line}")

    lines = lshw_text.splitlines()
    debug(f"{len(lines)} lines of input")

    line_indent_pattern = re.compile(r'\s*(\*-)?')
    new_array_pattern = re.compile(r'\s*\*-([\w-]+):(\d+)\s*(.*)\s*$')
    new_object_pattern = re.compile(r'\s*\*-([^:]+)$')
    new_kv_pattern = re.compile(r'\s*([^:]+):\s*(.*)')

    # read the first line and create the root element
    name: str = lines[0].strip()
    debug(f"name: {name}")
    root: dict = {name: {}}
    stack = [root[name]]

    for line in lines[1:]:
        # get the current indent
        line_indent_pattern.match(line)
        if line_indent_pattern:
            indent = (len(line_indent_pattern.match(line).group(0)) - 1) / 3
            # debug(f"indent {indent}")

            # if the stack is longer than the current indent, pop
            while len(stack) > indent:
                stack.pop()

        # get the current object
        current_object = stack[-1]

        # check if this line is creating a new array
        new_array_match = new_array_pattern.match(line)
        if new_array_match:
            new_object_name = new_array_match.group(1)
            new_object_index = int(new_array_match.group(2))
            if new_object_name not in current_object:
                debug(f"Array ({new_object_name})")
                current_object[new_object_name] = []
            debug(f"Object ({new_object_name}) at index {new_object_index}")
            assert new_object_index == len(current_object[new_object_name])

            new_object = {}
            if new_array_match.group(3) != "":
                new_object["_tag"] = new_array_match.group(3)

            current_object[new_object_name].append(new_object)
            stack.append(new_object)
        else:
            # new object?
            new_object_match = new_object_pattern.match(line)
            if new_object_match:
                # create a new object add it to the current
                new_object_name = new_object_match.group(1)
                if new_object_name not in current_object:
                    debug(f"Object ({new_object_name})")
                    new_object = {}
                    current_object[new_object_name] = new_object
                    stack.append(new_object)
            else:
                # new key value
                new_kv_match = new_kv_pattern.match(line)
                if new_kv_match:
                    current_object[new_kv_match.group(1)] = new_kv_match.group(2)
                    debug(f"KV ({new_kv_match.group(1)} = {new_kv_match.group(2)})")

    return root


# read the input file
with open(sys.argv[1], 'r') as file:
    lshw_text = file.read()

# convert it to dictionary formats
parsed_data = parse_lshw_output(lshw_text)

# write the resulting json
with open(sys.argv[2], 'w') as json_file:
    json.dump(parsed_data, json_file, indent=4)
