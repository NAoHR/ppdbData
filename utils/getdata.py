import requests
import time


class ParseData:
    def __init__(self,jsonedData):
        self.jsonedData = jsonedData
    # get a certain data on data.py file based on argument you type
    def getData(self,yearType):
        return self.jsonedData if yearType == "all" else [item for item in self.jsonedData if item["yearType"] == yearType]

    # this method allow you to parse ppdb data based of a given list id with yeartype classification.
    # at first i thought ppdb stored all their data,but no,you can only get detail of a student in range only current year and a year before it
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
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36" # add your own userAgent
            }
            try:
                getSchoolName = requests.get(f"{getSchool}{id}",timeout=3) if yearType == "current" else requests.get(f"{getSchool}{id}",timeout=3,headers=headers)
                jsoned = getSchoolName.json()
                school = jsoned[0][3][6][3]
                print(f"[✓] {id} : {school}")
                return jsoned[0][3][6][3]
            except Exception as e:
                print(f"[x] {id} : Error,Cant retrify data")
                return "Error, cant retrified data"
        except KeyboardInterrupt:
            raise("Stopped")

    # this is a main method to execute the data and return a list which contain all the needed data
    def mainProccess(self,yearType="all"):

        def parseGivenList(list):
            try:
                tobeReturned = {}
                if list:
                    for school in list:
                        print(f"[?] processing {school['yearType']} data")
                        tobeReturned[school["yearType"]] = "pending"
                        eachVocType = []
                        for apiData in school["sourceDataLink"]:
                            print(f"[?] Begin {apiData['vocType']}")
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
        
        start = time.time()
        print(f"[!] Process started at {time.ctime(start)}")
        dataToBeRequested = self.jsonedData if yearType == "all" else [item for item in self.jsonedData if item["yearType"] == yearType]
        proccesData = parseGivenList(dataToBeRequested)
        end = time.time()
        print(f"[!] Process ended at {time.ctime(end)} and took {end-start} ms")
        return proccesData
