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
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
                "Host": "arsip.siap-ppdb.com",
                "Referer": "https://arsip.siap-ppdb.com/2020/jakarta/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Sec-GPC": "1",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
            }
            try:
                getSchoolName = requests.get(f"{getSchool}{id}",timeout=3) if yearType == "current" else requests.get(f"{getSchool}{id}",timeout=3,headers=headers)
                jsoned = getSchoolName.json()
                print(f"[✓] {id} : {jsoned[0][3][6][3]}")
                return jsoned[0][3][6][3]
            except Exception as e:
                print(f"[x] {id} : Error,Cant retrify data")
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
    finalData = begin.mainProccess("2020")
    print(finalData)