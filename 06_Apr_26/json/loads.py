import json

json_data = '{"name" :  "Mihir", "age"  :  21 }'
data = json.loads(json_data)

print(data)
print(type(data))