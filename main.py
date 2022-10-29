import json
import re

if __name__ == '__main__':

    # with open("orders_with_usernames.txt", "r", encoding="utf-8-sig") as f:
    #     data = f.read()
    #
    # print(data)
    # print(type(data))
    # eval_data = eval(data)
    # print(eval_data)
    # print(type(eval_data))
    # for order in eval_data:
    #     print(order['userId'])
    #
    # with open("users.txt", "r", encoding="utf-8-sig") as f:
    #     user_data = f.read()
    #
    # eval_user_data = eval(user_data)
    # for user in eval_user_data:
    #     print(user["id"])
    #     print(user["username"])
    #
    # for order in eval_data:
    #     for user in eval_user_data:
    #         if order['userId'] == user['id']:
    #             order['username'] = user['username']
    #
    # for order in eval_data:
    #     print(order['userId'])
    #     print(order['username'])
    #
    # new_order_list = []
    #
    # for order in eval_data:
    #     new_order_list.append(order)
    #
    # with open("new_orders_with_usernames.txt", "w", encoding="utf-8-sig") as f:
    #     f.write(str(new_order_list))


    with open("new_orders_with_usernames.txt", "r", encoding="UTF-8-sig") as f:
        data = f.read();
        print(data)
        print(type(data))
        # newdata = data.replace(r"{'id': \w+, 'p", "{'p")

        # newdata = data.replace(r"{'id': \d+, 'p", "")
        # newdata = data.replace("\\\\d", "")
        newdata = re.sub(r"{'id': \d+, 'p", "{'p", data)
        print(newdata)
        newdata = newdata.replace("\'", "\"")
        newdata = newdata.replace("n\"s", "n\'s")
        newdata = newdata.replace("L\"O", "L\'O")
        newdata = newdata.replace("},  ,", "},")
        print(newdata)

    with open("new_orders_with_usernames_without_ids.txt", "w", encoding="UTF-8-sig") as f:
        f.write(newdata)

    with open("new_orders_with_usernames_without_ids.txt", "r", encoding="UTF-8-sig") as f:
        read_data = f.read()
        jsn = json.loads(read_data)
        print(jsn)
        print(type(jsn))
    for order in jsn:
        print(order)
        print(type(order))

