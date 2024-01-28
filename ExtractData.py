import json

# Opening JSON file
f = open('correlations.json')

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list
count = 0
for i in data:
    for j in data[i]:
        print(data[i][j])
    #if(i["symbol"][-4:] == "USDT"):
    #    print(i["symbol"])

print(count)