from utils.makeDataSet import MakeDataSet
import json

with open("data.json","r") as file:
    data = json.load(file)
    file.close()

mDs = MakeDataSet(data)
# print(mDs.makeEachVocFolder("outputDataSet_0","2020",0))
mDs.make("testing")