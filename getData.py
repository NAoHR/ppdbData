import requests
from data import allData



class ParseData:
    def __init__(self,jsonedData):
        self.jsonedData = jsonedData

    def getData(self,yearType):
        return [item for item in self.jsonedData if item["yearType"] == yearType]

    def mainProccess(self,yearType="all"):
        def parseEachData(id,returnedList):
            try:
                getSchool = "https://api.siap-ppdb.com/cari?no_daftar=" if yearType == "current" else f"https://arsip.siap-ppdb.com/{yearType}/api/cari?no_daftar="
                print(getSchool)
            except KeyboardInterrupt:
                return 0

        def parseGivenList(list):
            try:
                allStudentId = {}
                if list:
                    for school in list:
                        print(f"==== proccessing {school['yearType']} ====")
                        allStudentId[school["yearType"]] = "pending"
                        toAllStudentIDSchool = []
                        for apiData in school["sourceDataLink"]:
                            try:
                                r = requests.get(apiData["api"],timeout=3)
                                students = r.json()
                                toAllStudentIDSchool.append({
                                    apiData["vocType"] : [item[3] for item in students["data"]]
                                })
                                print(f"{apiData['vocType']}\t\tDone")
                            except Exception as e:
                                toAllStudentIDSchool.append({
                                    apiData["vocType"] : "Error"
                                })
                                print(f"{apiData['vocType']}\t\tFailed")
                        allStudentId[school["yearType"]] = toAllStudentIDSchool
                        toAllStudentIDSchool = []
                        print()
                    print(allStudentId)
                    return 1
                return False
            except KeyboardInterrupt:
                return False

        dataToBeRequested = self.jsonedData if yearType == "all" else [item for item in self.jsonedData if item["yearType"] == yearType]
        return parseGivenList(dataToBeRequested)



begin = ParseData(allData)
begin.mainProccess("current")