import yaml


data_to_yaml = {
    "action": ["left", "right", "up", "down"],
    "number": 150,
    "my_dict": {1: "€", 2: "я", 3: "ф"},
}


with open("data_write.yaml", "w") as f_n:
    yaml.dump(data_to_yaml, f_n, default_flow_style=False, allow_unicode=True)

with open("data_write.yaml") as f_n:
    print(f_n.read())
