import json
import requests
import os
import csv
class MakeDataSet:
    def __init__(self,data,fileType):
        self.data = data
        self.fileType = fileType
        self.logError = {
            "errorVoc" : [],
            "errorId" : [],
            "errReport" : []
        }
        # 
        # errorVoc format => {
        #   "yearType" : ___
        #   "vocType" : ___
        # }

        # errorId format => {
        #   "id" : ___
        #   "yearType" : ___
        #   "vocType" : ___
        # }
    # proccess data to folder
            
    def makeEachVocFolder(self,bfFolder,yearType,num):
        folderName = f"{bfFolder}/{yearType}_{num}" if num != 0 else f"{bfFolder}/{yearType}"
        print()
        print(f"[!] begin to create folder {folderName}")
        if os.path.exists(folderName):
            print(f"[x] {folderName} already taken")
            return self.makeEachVocFolder(bfFolder,yearType,num+1)
        os.mkdir(folderName)
        print(f"[✓] successfully created folder {folderName}")
        return folderName

    def makeItJson(self,pathFile,dtToCreate):
        with open(pathFile,"w") as fileJson:
            dumped = json.dumps(dtToCreate,indent=4)
            fileJson.write(dumped)
            fileJson.close()
            return True
            
    def makeItCsv(self,pathFile,dtToCreate):
        with open(pathFile,"w",encoding="UTF-8",newline='') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=dtToCreate["head"])
            writer.writeheader()
            writer.writerows(dtToCreate["data"])
            return True

    def makeEachDataSet(self,data,folderName):
        print("[!] begin to create each json file")
        tobeMergedAll = {
            "id" : [],
            "name": [],
            "gender" : [],
            "school" : []
        } if self.fileType == "json" else {
            "head" : [],
            "data" : []
        }

        for item in data:
            if item["data"]:
                folderYearPath = self.makeEachVocFolder(folderName,item["typeYear"],0)
                tobeMergedEachVoc = {
                    "id" : [],
                    "name": [],
                    "gender" : [],
                    "school" : []
                } if self.fileType == "json" else {
                    "head" : item["head"],
                    "data" : []
                }
                for subitem in item["data"]:
                    if subitem["error"] == False:
                        if self.fileType == "json":
                            jsonFile = {
                                "id" : subitem["id"],
                                "name" : subitem["name"],
                                "gender" : subitem["gender"],
                                "school" : subitem["school"]
                            }
                            tobeMergedEachVoc["id"] = tobeMergedEachVoc["id"] + subitem["id"]
                            tobeMergedEachVoc["name"] = tobeMergedEachVoc["name"] + subitem["name"]
                            tobeMergedEachVoc["gender"] = tobeMergedEachVoc["gender"] + subitem["gender"]
                            tobeMergedEachVoc["school"] = tobeMergedEachVoc["school"] + subitem["school"]

                            fileName = f"{subitem['vocType']}-{item['typeYear']}.json"
                            subitemJson = self.makeItJson(f"{folderYearPath}/{fileName}",jsonFile)
                            if subitemJson:
                                print(f" ➥ [✓] {fileName} successfully created")
                        else:
                            tobeMergedEachVoc["data"] = tobeMergedEachVoc["data"] + subitem["csvData"]
                            fileName = f"{subitem['vocType']}-{item['typeYear']}.csv"
                            subitemCsv = self.makeItCsv(f"{folderYearPath}/{fileName}",{
                                "head" : item["head"],
                                "data" : subitem["csvData"]
                            })
                            if subitemCsv:
                                print(f" ➥ [✓] {fileName} successfully created")
                mergedJson = self.makeItJson(f"{folderYearPath}/merged-{item['typeYear']}.json",tobeMergedEachVoc) if self.fileType == "json" else self.makeItCsv(f"{folderYearPath}/merged-{item['typeYear']}.csv",tobeMergedEachVoc)
                if mergedJson:
                    print(f" ➥ [✓] succesfully merged data and create merged-{item['typeYear']}")
                
                if self.fileType == "json":
                    tobeMergedAll["id"] = tobeMergedAll["id"] + tobeMergedEachVoc["id"]
                    tobeMergedAll["name"] = tobeMergedAll["name"] + tobeMergedEachVoc["name"]
                    tobeMergedAll["gender"] = tobeMergedAll["gender"] + tobeMergedEachVoc["gender"]
                    tobeMergedAll["school"] = tobeMergedAll["school"] + tobeMergedEachVoc["school"]
                else:
                    tobeMergedAll["head"] = tobeMergedEachVoc["head"]
                    tobeMergedAll["data"] = tobeMergedAll["data"] + tobeMergedEachVoc["data"]
        
        mergedAll = self.makeItJson(f"{folderName}/all-merged.json",tobeMergedAll) if self.fileType == "json" else self.makeItCsv(f"{folderName}/all-merged.csv",tobeMergedAll)
        if mergedAll:
            print(f"[✓] Successfully Merged All Data To One Json File")
        return True
    

    # def makeEachDataSetcsv(self,data,mainPath):
    #     for item in data:
    #         for subitem in item["data"]:
    #             folderYearPath = 

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
        dataBucket = {
            "vocType" :vocType,
            "error" : False,
            "id" : [],
            "name" : [],
            "gender" : [],
            "school" : []
        } if self.fileType == "json" else {
            "vocType" : vocType,
            "error" : False,
            "csvData" : []
        }

        for studentId in studentList:
            try:
                req = requests.get(f"{apiLink}{studentId}",timeout=3) if yearType == "current" else requests.get(f"{apiLink}{studentId}",timeout=3,headers=headers)
                jsoned = req.json()
                nameData = jsoned[0][3][2][-1]
                genderData = jsoned[0][3][3][-2]
                schoolData = jsoned[0][3][6][3]
                if jsoned[-1][3][3][-1] != "Tidak Lapor Diri":
                    if self.fileType == "json":
                        dataBucket["id"].append(studentId)
                        dataBucket["name"].append(nameData)
                        dataBucket["gender"].append(genderData)
                        dataBucket["school"].append(schoolData)
                    else:
                        dataBucket["csvData"].append(
                            {
                                "id" : studentId,
                                "name" : nameData,
                                "gender" : genderData,
                                "school" : schoolData
                            }
                        )
                    print(f"  ➥ [✓] {studentId}\t\tOK")
                else:
                    self.logError["errReport"].append({
                        "id" : studentId,
                        "yearType" : yearType,
                        "vocType" : vocType
                    })
                    print(f"  ➥ [x] {studentId}\t\tFalse")
            except Exception as e:
                self.logError["errorId"].append({
                    "id" : studentId,
                    "yearType" : yearType,
                    "vocType" : vocType
                })
                print(f"  ➥ [x] {studentId}\t\tFailed")
        return dataBucket


    def makeReqToApi(self,arg):
        afterParsed = self.data["data"] if arg == "all" else [item for item in self.data["data"] if item["yearType"] == arg]
        if afterParsed:
            requestBucket = []
            for item in afterParsed:
                afterAlleachBucket = {
                    "typeYear" : item["yearType"],
                    "head" : ["id","name","gender","school"],
                    "data" : []
                }
                print()
                print(f"[!] proccessing {item['yearType']}")
                for subitem in item["sourceDataLink"]:
                    try:
                        print(f"\n ➤ [!] Fetching {subitem['vocType']}")
                        req = requests.get(subitem["api"],timeout=3)
                        jsoned = req.json()
                        eachDataBucket = self.eachDataHandler([item[3] for item in jsoned["data"]],item["yearType"],subitem["vocType"])
                        afterAlleachBucket["data"].append(eachDataBucket)
                    except Exception as e:
                        afterAlleachBucket["data"].append({
                            "vocType" : subitem["vocType"],
                            "error" : True
                        })
                        self.logError["errorVoc"].append({
                            "yearType" : item["yearType"],
                            "vocType" : subitem["vocType"]
                        })
                        print(f"  ➥ [x] Failed to fetch {subitem['vocType']}\n")
                requestBucket.append(afterAlleachBucket)
            return requestBucket
        else:
            return False


    def make(self,arg):
        try:
            tobeReturned = self.makeReqToApi(arg)
            print()
            self.logger()
            print()
            if tobeReturned != False:
                counterFailed = 0
                for item in tobeReturned:
                    for subitem in item["data"]:
                        if subitem["error"] == True:
                            counterFailed += 1
                if counterFailed == sum([len(item["data"]) for item in tobeReturned]):
                    print("➥[x] can't create dataset. All of connections went failed")
                    return False
                makeFolderMain = str(input("[?] begin to make dataset (y/n) : "))
                if makeFolderMain.lower() == "y":
                    fdName = self.makeFolderMain("outputDataSet",0)
                    self.makeEachDataSet(tobeReturned,fdName)
                    # if self.fileType == "json":
                    #     print()
                    #     # self.makeEachDataSet(tobeReturned,fdName) if self.fileType == "json" else self.makeEachDataSetcsv(tobeReturned,fdName)
                    #     self.makeEachDataSet(tobeReturned,fdName)
                    # else:
                    #     [print(tobeReturned)]
                return False
            return False
        except KeyboardInterrupt:
            print("[x] Adios")

    # getter
    def logger(self):
        if self.logError["errorVoc"] or self.logError["errorId"] or self.logError["errReport"]:
            print("\n\n\n")
            print("[x] Error Data log")
            if self.logError["errorVoc"]:
                for item in self.logError["errorVoc"]:
                    print(f"  ➥ [~] Can't Fetch {item['vocType']} in {item['yearType']} Data")
            elif self.logError["errorId"]:
                for itemid in self.logError["errorId"]:
                    print(f"  ➥ [~] Cant Fetch {itemid['vocType']}'s {itemid['id']} in {itemid['yearType']} Data")
            elif self.logError["errReport"]:
                for itemid in self.logError["errReport"]:
                    print(f"  ➥ [~] {itemid['id']}'s self-report status : False")
            print("\n\n\n")
        else:
            print("[✓] No Log To Be Displayed,All Data Successfully Fetched")