#!/usr/bin/python3

import json
import sys
import jsonschema
from jsonschema import validate

# verify that we are actually supplied a json string
# note: this method may clobber quote characters depending on how it is read
# by something like xargs. TODO: switch to reading from stdin?
argc = len(sys.argv)
if (argc < 2):
    print("Json string must be provided")
    exit(-1)

# load the schema
schema_file = open("schema.json", "r")
# attempt to parse schema to dictionary 
try:
    parsed_schema_dict = json.loads(schema_file.read())
except json.decoder.JSONDecodeError as e:
    print("json unable to decode schema. error: ")
    print(e)
    exit(-2)

# attempt to parse to dictionary
input_json = " ".join(sys.argv[1:])
print("input json string is " + input_json)
try:
    parsed_dict = json.loads(input_json)
except json.decoder.JSONDecodeError as e:
    print("json unable to decode. error: ")
    print(e)
    exit(-3)

print("the parsed dict is")
print(parsed_dict)

try: 
    validate(instance=parsed_dict, schema=parsed_schema_dict)
except jsonschema.exceptions.ValidationError as e:
    print("Json does not match schema. Error: ")
    print(e)
    exit(-4)

print("json valid from schema ")



