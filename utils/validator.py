import json
class ValidateInput():
    def __init__(self,dataList):
        self.dataList = dataList
    
    def propperUse(self):
        print("""
How To Use:

> -y : to specify the year you want to use on this programm
> -t : to specify what kind of type you want to parse, ex: jhs,gender
> -h : help
> python3 -f <your json file> -y <yeartype> -t <type>
        """)
        return False

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
                print(f"[x] {fileName} Not Found")
                return False

    def validateOtherTag(self,wantToCheck,validType):
        try:
            ind = self.dataList.index(wantToCheck)
            if ind == len(self.dataList) -1:
                if wantToCheck == "-y":
                    print("[x] you didn't specify year type,now using the default value 'all' ")
                else:
                    print("[x] you didn't specify data type,now using the default value 'jhs' ")
                return "jhs" if wantToCheck == "-t" else "current"
            else:
                validType.append("all") if wantToCheck == "-y" else None
                if self.dataList[ind+1] in validType:
                    return self.dataList[ind+1]
                return False
        except ValueError:
            return True
    def validateArgv(self):
        if len(self.dataList) == 1 :
            self.propperUse()
            return 0
        else:
            if len(self.dataList) == 2 and self.dataList[1] == "-f":
                return self.propperUse()
            else:
                if(self.dataList[1] == "-f" and len(self.dataList) >= 3):
                    toBeReturned = {
                        "data" : False,
                        "year" : "current",
                        "type" : "jhs"
                    }
                    fileCheck = self.validateFile(self.dataList[2])
                    if fileCheck == False:
                        return False
                    else:
                        toBeReturned["data"] = fileCheck
                        tagYCheck = self.validateOtherTag("-y",[item["yearType"] for item in toBeReturned["data"]])
                        tagTCheck = self.validateOtherTag("-t",["jhs","gender"])
                        if tagYCheck == False and tagTCheck == False:
                            print("[x] your argument on -y and -t option didnt pass any on list")
                            return False
                        elif tagYCheck != False and tagTCheck != False:
                            print(tagTCheck,tagYCheck)
                            toBeReturned["year"] = "current" if tagYCheck == True else tagYCheck
                            toBeReturned["type"] = "jhs" if tagTCheck == True else tagTCheck
                            if tagYCheck == True:
                                print("[!] you didnt specify any -y option,now you are using current as a default value")
                            if tagTCheck == True:
                                print("[!] you didnt specify any -t option,now you are using jhs as a default value")
                            return toBeReturned
                        errM = f"[x] your argument on {'-y' if tagYCheck == False and tagTCheck != False else '-t'} option didnt pass any on list"
                        print(errM)
                        return False
                else:
                    self.propperUse()
                    return 0