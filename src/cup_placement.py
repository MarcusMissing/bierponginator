import random


def random_number():
    return round(random.uniform(0, 1))


position_array = []
result_array = [[]]

for i in range(100):
    for j in range(10):
        position_array.append(random_number())
    result_array.append(position_array)
    position_array = []

result_array.pop(0)
for i in result_array:
    print(i)
