import requests
from data import allData



class ParseData:
    def __init__(self,jsonedData):
        self.jsonedData = jsonedData

    def getData(self,yearType):
        return self.jsonedData if yearType == "all" else [item for item in self.jsonedData if item["yearType"] == yearType]

    def parseEachData(self,id,yearType):
        try:
            getSchool = "https://api.siap-ppdb.com/cari?no_daftar=" if yearType == "current" else f"https://arsip.siap-ppdb.com/{yearType}/api/cari?no_daftar="
            try:
                getSchoolName = requests.get(f"{getSchool}{id}",timeout=3)
                jsoned = getSchoolName.json()
                print(jsoned[0][3][6][3])
                return jsoned[0][3][6][3]
            except Exception as e:
                print("Error, Cant retrify the data")
                return "Error, cant retrified data"
        except KeyboardInterrupt:
            raise("Stopped")

    def mainProccess(self,yearType="all"):

        def parseGivenList(list):
            try:
                tobeReturned = {}
                if list:
                    for school in list:
                        print(f"proccessing {school['yearType']} ====")
                        tobeReturned[school["yearType"]] = "pending"
                        eachVocType = []
                        for apiData in school["sourceDataLink"]:
                            print()
                            print(f"Begin {apiData['vocType']}  ====")
                            try:
                                r = requests.get(apiData["api"],timeout=3)
                                students = r.json()
                                studentSchool = []
                                for student in students["data"]:
                                    studentSchool.append(self.parseEachData(student[3],school["yearType"]))
                                eachVocType.append({
                                    apiData["vocType"] : studentSchool
                                })
                                studentSchool = []
                            except Exception as e:
                                eachVocType.append({
                                    apiData["vocType"] : "Error"
                                })
                                print(f"{apiData['vocType']}\t\tFailed")
                
                        tobeReturned[school["yearType"]] = eachVocType
                        eachVocType = []
                        print()
                    return tobeReturned
                return False
            except KeyboardInterrupt:
                raise("Stopped")

        dataToBeRequested = self.jsonedData if yearType == "all" else [item for item in self.jsonedData if item["yearType"] == yearType]
        return parseGivenList(dataToBeRequested)



if __name__ == "__main__":
    begin = ParseData(allData)
    finalData = begin.mainProccess("all")
    print(finalData)