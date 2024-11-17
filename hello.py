import random
print("Hello World")

numbers = {}

count = 100000
sum =0
for x in range(count):
    rand = random.randint(1,6)
    sum += rand
    numbers.setdefault(rand,0)
    numbers[rand] += 1


print(sum/count)
print("------------------")
print(numbers)