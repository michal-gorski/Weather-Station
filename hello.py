import random
import requests
from bs4 import BeautifulSoup

print("Hello World")

numbers = {}

count = 100
sum =0
for x in range(count):
    rand = random.randint(1,6)
    sum += rand
    numbers.setdefault(rand,0)
    numbers[rand] += 1


print(sum/count)
print("------------------")
print(dict(sorted(numbers.items())))


url = 'https://weather.com/weather/tenday/l/93409ef628e2eccc8fe84493beb24470c722d12ef4632a9c49250af345ba81ef'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
mydivs = soup.find_all("div")

for div in mydivs:
        classes = div.get('class')
        if classes:
            filtered_classes = [cls for cls in classes if cls.startswith('Daily')]
            if filtered_classes:
                
                print(f"Class: {filtered_classes}")




print(soup.p['class'])