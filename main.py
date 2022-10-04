import pandas as pd
import json
from pandas.io.json import json_normalize
import numpy as np

from CosineSimilarity import CosineSimilarity
from Request import Request

if __name__ == '__main__':

    # new_request = Request('https://dummyjson.com/carts')
    # new_request.make_json_from_data()

    # rest_api_request = Request('http://localhost:9090/order-data')
    # rest_api_request.test_request()

    a = np.array([1, 2, 3])
    print(a)
    print(a.ndim)
    b = np.array([[4, 5, 6, 9], [7, 8, 9, 4], [0, 0, 0, 0]])
    print(b)
    print(b.ndim)
    print(b.shape)
    print(b.size)
    print(b.itemsize)

    c = np.array([[1, 2, 3, 4, 5, 6, 7], [8, 9, 10, 11, 12, 13, 14]])
    print(c)
    print(c[1, 2])
    print(c[0, :])
    for i, j in enumerate(c[0, :]):
        print(i)
    print(c[:, 3])
    print(c[0, 3:6:2])
    c[0, 1] = 15
    print(c)
    c[:, 5] = [0, 1]
    print(c)

    d = np.zeros((5, 5))
    print(d)

    # e = {
    #     '1': [1,1,1,1,1],
    #     '2': [1,2],
    #     '3': [1,2,3],
    #      }
    #
    # print(len(max(e.values(), key=len)))

    print(np.random.randint(8, 9, size=(4, 4)))
    print(np.identity(5))

    f = np.ones((5, 5), int)
    g = np.zeros((3, 3))
    # g[1][1] = 9
    g[1, 1] = False
    g[2, 2] = 0.5
    f[1:4, 1:4] = g
    print(f)
    print(g)

    h = np.full((5, 5), 4)
    print(h)

    j = [0, 0, 0, 0]
    # h[:, 0] = h[:, 0] * j
    h[1:, 0] = j
    print(h)

    before = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    print(before)

    after = before.reshape((2, 2, 2))
    print(after)

    v1 = np.array([1, 2, 3, 4])
    v2 = np.array([5, 6, 7, 8])
    v3 = np.array([9, 10, 11, 12])
    v4 = np.array([13, 14, 15, 16])

    tda = np.vstack([v1, v2, v3])
    # tda.
    print(tda)
    print(tda > 6)
    list_1 = [2,3,4,5]
    list_2 = [2, 3, 7, 9, 11, 12, 14, 16, 21, 23, 24, 25, 29, 30, 32, 36, 37, 39, 45, 46, 47, 48, 53, 54, 59, 61, 64, 66, 68, 70, 75, 76, 80, 81, 83, 84, 88, 90, 91, 92, 93, 94, 96, 97, 99]

    k = np.zeros((5,46))
    print(k)
    # print(np.all(k > 7, axis=0))
    k[1:, 0] = list_1
    k[0, 1:] = list_2
    print(k)
    # k[1, 1] = 0.047619047619047616
    k[1, 1] = 1
    print(k)

    print((0.15990053726670786 + 0.10341753799900384 + 0.09304842103984709) * 1.32926316)