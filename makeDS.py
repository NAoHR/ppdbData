from utils.makeDataSet import MakeDataSet
import json

with open("data.json","r") as file:
    data = json.load(file)
    file.close()

mDs = MakeDataSet(data)
print(mDs.makeReqToApi("testing"))