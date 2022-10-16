

if __name__ == '__main__':

    with open("orders_with_usernames.txt", "r", encoding="utf-8-sig") as f:
        data = f.read()

    print(data)
    print(type(data))
    eval_data = eval(data)
    print(eval_data)
    print(type(eval_data))
    for order in eval_data:
        print(order['userId'])

    with open("users.txt", "r", encoding="utf-8-sig") as f:
        user_data = f.read()

    eval_user_data = eval(user_data)
    for user in eval_user_data:
        print(user["id"])
        print(user["username"])

    for order in eval_data:
        for user in eval_user_data:
            if order['userId'] == user['id']:
                order['username'] = user['username']

    for order in eval_data:
        print(order['userId'])
        print(order['username'])

    new_order_list = []

    for order in eval_data:
        new_order_list.append(order)

    with open("new_orders_with_usernames.txt", "w", encoding="utf-8-sig") as f:
        f.write(str(new_order_list))


