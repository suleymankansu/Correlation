import json

f = open("daily_corr.json", "r")

data = json.load(f)
f.close()

count = 0
for i in data:
    count += 1
    print(i)

print(count)
