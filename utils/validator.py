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

    def validateOtherTag(self,wantToCheck,validType):
        try:
            ind = self.dataList.index(wantToCheck)
            if ind == len(self.dataList) -1:
                if wantToCheck == "-y":
                    print("you didn't specify year type,now using the default value 'all' ")
                else:
                    print("you didn't specify data type,now using the default value 'jhs' ")
                return False
            else:
                if self.dataList[ind+1] in validType:
                    return self.dataList[ind+1]
                errMessage = f"value you chose didn't pass any {'yeartype' if wantToCheck == '-y' else 'type'}, now using a default value ,{'all' if wantToCheck == '-y' else 'jhs'}"
                print(errMessage)
                return False
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
                toBeReturned["data"] = fileCheck
                toBeReturned["year"] = self.validateOtherTag("-y",[item["yearType"] for item in toBeReturned["data"]])
                toBeReturned["type"] = self.validateOtherTag("-t",["jhs","gender"])
                return toBeReturned
            else:
                self.propperUse()
                return 0