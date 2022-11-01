import json
import re


def read_orders_file():

    with open("orders_with_usernames.txt", "r", encoding="utf-8-sig") as f:
        data = f.read()

    eval_data = eval(data)
    for order in eval_data:
        print(order['userId'])

    return eval_data


def read_users_file():
    with open("files/users.txt", "r", encoding="utf-8-sig") as f:
        user_data = f.read()

    eval_user_data = eval(user_data)
    for user in eval_user_data:
        print(user["id"])
        print(user["username"])

    return eval_user_data


def add_usernames():
    eval_data = read_orders_file()
    eval_user_data = read_users_file()
    for order in eval_data:
        for user in eval_user_data:
            if order['userId'] == user['id']:
                order['username'] = user['username']

    for order in eval_data:
        print(order['userId'])
        print(order['username'])

    return eval_data


def new_orders_list_creating():
    new_order_list = []
    eval_data = add_usernames()
    for order in eval_data:
        new_order_list.append(order)

    with open("files/new_orders_with_usernames.txt", "w", encoding="utf-8-sig") as f:
        f.write(str(new_order_list))


def quotes_in_orders_file_changing():
    with open("files/new_orders_with_usernames.txt", "r", encoding="UTF-8-sig") as f:
        data = f.read();

        newdata = re.sub(r"{'id': \d+, 'p", "{'p", data)
        newdata = newdata.replace("\'", "\"")
        newdata = newdata.replace("n\"s", "n\'s")
        newdata = newdata.replace("L\"O", "L\'O")
        newdata = newdata.replace("},  ,", "},")

    with open("files/new_orders_with_usernames_without_ids.txt", "w", encoding="UTF-8-sig") as f:
        f.write(newdata)


def validity_check():
    with open("files/new_orders_with_usernames_without_ids.txt", "r", encoding="UTF-8-sig") as f:
        read_data = f.read()
        jsn = json.loads(read_data)
    for order in jsn:
        print(order)
        print(type(order))