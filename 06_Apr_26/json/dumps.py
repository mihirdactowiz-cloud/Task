import json

data = {
    "name": "Alice",
    "age": 30,
}

json_string =  json.dumps(data)

print(json_string)