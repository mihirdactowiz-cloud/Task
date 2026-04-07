import json

data =  {"name" : "Mihir", "age" : 21 }

with open("data.json", "w") as file:
    json.dump(data, file)