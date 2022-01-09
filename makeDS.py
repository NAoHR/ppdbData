from utils.makeDataSet import MakeDataSet
import json

with open("automate_data.json","r") as file:
    data = json.load(file)
    file.close()

mDs = MakeDataSet(data)
mDs.make("all")