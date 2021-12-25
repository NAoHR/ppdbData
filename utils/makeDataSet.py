import json
import requests
import os
class MakeDataSet:
    def __init__(self,data):
        self.data = data

    def makeFolder(self,name,num):
        print()
        folderName = f"{name}_{num}"
        print(f"[!] begin creting folder {folderName}")
        if os.path.exists(folderName):
            print()
            return self.makeFolder(name,num+1)
        os.mkdir(folderName)
        print(f"[✓] successfully created folder {folderName}")
        return folderName

    def eachDataHandler(self,studentList,yearType,vocType):
        yearType = "current" if yearType == "testing" else yearType #for testing only
        apiLink = "https://api.siap-ppdb.com/cari?no_daftar=" if yearType == "current" else f"https://arsip.siap-ppdb.com/{yearType}/api/cari?no_daftar="
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
        subDataBucket = {
            "vocType" :vocType,
            "name" : [],
            "gender" : [],
            "school" : []
        }
        for studentId in studentList:
            try:
                req = requests.get(f"{apiLink}{studentId}",timeout=3) if yearType == "current" else requests.get(f"{apiLink}{id}",timeout=3,headers=headers)
                jsoned = req.json()
                nameData = jsoned[0][3][2][-1]
                genderData = jsoned[0][3][3][-2]
                schoolData = jsoned[0][3][6][3]
                subDataBucket["name"].append(nameData)
                subDataBucket["gender"].append(genderData)
                subDataBucket["school"].append(schoolData)
                print(f"[✓] {studentId} done")
            except Exception as e:
                subDataBucket["name"].append(None)
                subDataBucket["gender"].append(None)
                subDataBucket["school"].append(None)
        return subDataBucket


    def makeReqToApi(self,arg):
        afterParsed = self.data["data"] if arg == "all" else [item for item in self.data["data"] if item["yearType"] == arg]
        if afterParsed:
            requestBucket = []
            for item in afterParsed:
                afterAlleachBucket = {
                    "typeYear" : item["yearType"],
                    "data" : []
                }
                print(f"[!] proccessing {item['yearType']}")
                for subitem in item["sourceDataLink"]:
                    try:
                        req = requests.get(subitem["api"],timeout=3)
                        jsoned = req.json()
                        eachDataBucket = self.eachDataHandler([item[3] for item in jsoned["data"]],item["yearType"],subitem["vocType"])
                        afterAlleachBucket["data"].append(eachDataBucket)
                    except Exception as e:
                        print(e)
                requestBucket.append(afterAlleachBucket)
            return requestBucket
        else:
            return False


    def make(self,arg):
        try:
            tobeReturned = self.makeReqToApi("testing")
            if tobeReturned != False:
                makeFolder = str(input("[?] begin to make dataset (y/n) :"))
                if makeFolder.lower() == "y":
                    fdName = self.makeFolder("outputDataSet",0)
                    return True
                return False
            return False
        except KeyboardInterrupt:
            print("[x] Adios")