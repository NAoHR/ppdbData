import json
import requests
import os
class MakeDataSet:
    def __init__(self,data):
        self.data = data
    # proccess data to folder
    def makeEachVocFolder(self,bfFolder,yearType,num):
        folderName = f"{bfFolder}/{yearType}_{num}" if num != 0 else f"{bfFolder}/{yearType}"
        print(f"[!] begin to create folder {folderName}")
        if os.path.exists(folderName):
            print(f"[x] {folderName} already taken")
            return self.makeEachVocFolder(bfFolder,yearType,num+1)
        os.mkdir(folderName)
        print(f"[✓] successfully created folder {folderName}")
        return folderName
    
    def makeEachJsonFile(self,data,folderName):
        print("[!] begin to create each json file")
        for item in data:
            if item["data"]:
                folderYearPath = self.makeEachVocFolder(folderName,item["typeYear"],0)
                for subitem in item["data"]:
                    jsonFile = {
                        "id" : subitem["id"],
                        "name" : subitem["name"],
                        "gender" : subitem["gender"],
                        "school" : subitem["school"]
                    }
                    dumpJson = json.dumps(jsonFile,indent=4)
                    fileName = f"{subitem['vocType']}-{item['typeYear']}.json"
                    with open(f"{folderYearPath}/{fileName}","w") as jsonedFile:
                        jsonedFile.write(dumpJson)
                        print(f"[✓] {fileName} successfully created")
                        jsonedFile.close()
    def makeFolderMain(self,name,num):
        folderName = f"{name}_{num}"
        print(f"[!] begin creating folder {folderName}")
        if os.path.exists(folderName):
            print(f"[x] {folderName} already taken")
            return self.makeFolderMain(name,num+1)
        os.mkdir(folderName)
        print(f"[✓] successfully created folder {folderName}")
        return folderName

    # make Data from requested API
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
            "id" : [],
            "name" : [],
            "gender" : [],
            "school" : []
        }
        for studentId in studentList:
            subDataBucket["id"].append(studentId)
            try:
                req = requests.get(f"{apiLink}{studentId}",timeout=3) if yearType == "current" else requests.get(f"{apiLink}{studentId}",timeout=3,headers=headers)
                jsoned = req.json()
                nameData = jsoned[0][3][2][-1]
                genderData = jsoned[0][3][3][-2]
                schoolData = jsoned[0][3][6][3]
                subDataBucket["name"].append(nameData)
                subDataBucket["gender"].append(genderData)
                subDataBucket["school"].append(schoolData)
                print(f"[✓] {studentId}\t\tDone")
            except Exception as e:
                subDataBucket["name"].append(None)
                subDataBucket["gender"].append(None)
                subDataBucket["school"].append(None)
                print(f"[x] {studentId}\t\tFailed")
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
                        afterAlleachBucket["data"] = False
                requestBucket.append(afterAlleachBucket)
            return requestBucket
        else:
            return False


    def make(self,arg):
        try:
            tobeReturned = self.makeReqToApi(arg)
            if tobeReturned != False:
                makeFolderMain = str(input("[?] begin to make dataset (y/n) :"))
                if makeFolderMain.lower() == "y":
                    fdName = self.makeFolderMain("outputDataSet",0)
                    print()
                    self.makeEachJsonFile(tobeReturned,fdName)
                    return True
                return False
            return False
        except KeyboardInterrupt:
            print("[x] Adios")