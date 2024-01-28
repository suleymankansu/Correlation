import json


def txt_to_json(txtName, jsonName):
    f = open(txtName, "r")

    lines = f.readlines()
    dictionary = {}

    coin = ""
    correlations = {}
    for line in lines:
        if line[0] == "*":
            coin = line.strip("*").split(" ")[2].split("*")[0]
            correlations.clear()
        elif line.split(" ")[0] == "Name:":
            dictionary[coin] = correlations.copy()
        else:
            correlations[line.split(" ")[0]] = line.split(" ")[-1].strip("\n")

    with open(jsonName, "w") as outfile:
        json.dump(dictionary, outfile)
        outfile.close()

    f.close()
