import json
class ValidateInput():
    def __init__(self,dataList):
        self.dataList = dataList
    
    def propperUse(self):
        print("data aint propper")

    def validateFile(self,fileName):
        splitted = fileName.split(".")[-1]
        if splitted == "json":
            try:
                with open(fileName,'r') as jsonedData:
                    loadJson = json.load(jsonedData)
                    if loadJson.get("data") == None:
                        return False
                    return loadJson["data"]

            except FileNotFoundError:
                print(f"{fileName} Not Found")
                return False

    def validateOtherTag(self,wantToCheck):
        try:
            ind = self.dataList.index(wantToCheck)
            if ind == len(self.dataList) -1:
                print("cant")
        except ValueError:
            return False
    def validateArgv(self):
        if len(self.dataList) == 1 :
            self.propperUse()
            return 0
        else:
            if(self.dataList[1] == "-f" and len(self.dataList) >= 3):
                toBeReturned = {
                    "data" : False,
                    "year" : False,
                    "type" : False
                }
                fileCheck = self.validateFile(self.dataList[2])
                if fileCheck == False:
                    return False
                self.validateOtherTag("-y")
                toBeReturned["data"] = fileCheck
                return toBeReturned
            else:
                self.propperUse()
                return 0