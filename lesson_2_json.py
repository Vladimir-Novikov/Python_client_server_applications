import json


def write_order_to_json(item, quantity, price, buyer, date):
    dict_to_json = {"item": item, "quantity": quantity, "price": price, "buyer": buyer, "date": date}

    # открываю файл в режиме а, т.к. может быть много заказов - дозаписываем

    with open("orders.json", "a") as f:
        json.dump(dict_to_json, f, indent=4)


if __name__ == "__main__":
    write_order_to_json("клавиатура", 3, 754, "Иванов", "05.02.2020")
    with open("orders.json") as f:
        print(f.read())
