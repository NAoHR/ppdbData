# still on development, dont use this
import json
import requests
from requests.exceptions import ReadTimeout


class MakeDataJson:    
    def __init__(self):
        self.errorLog = {
            "mainError" : [],
            "subMainError" : []
        }
        self.credFromCurrent = {
            "eachId" : [],
            "eachDataId" : []
        }
        self.data = {
            "accepted" : {
                "sctype" : {
                    "1" : "smp",
                    "2" : "sma",
                    "3" : "smk"
                },
                "scYear" : {
                    "1" : "current",
                    "2" : "2020",
                    "3" : "both"
                }
            },
            "linkSchool" :  {
                "current" : "https://ppdb.jakarta.go.id/seleksi/prestasi/",
                "2020" : "https://arsip.siap-ppdb.com/2020/jakarta/seleksi/prestasi/"
            },

            "school" : {
                "smp" : [
                            {
                                "yearType" : "current",
                                "link" : "https://ppdb.jakarta.go.id/sekolah/1-smp-prestasi.json",
                                "linkVoc" : "https://ppdb.jakarta.go.id/sekolah/kompetensi/1-smp-prestasi.json",
                                "pref" : "1"
                            },
                            {
                                "yearType" : "2020",
                                "link" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/2-smp-prestasi.json",
                                "linkVoc" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/kompetensi/2-smp-prestasi.json",
                                "pref" : "2"
                            }
                ],
                "sma" : [
                            {
                                "yearType" : "current",
                                "link" : "https://ppdb.jakarta.go.id/sekolah/1-sma-prestasi.json",
                                "linkVoc" : "https://ppdb.jakarta.go.id/sekolah/kompetensi/1-sma-prestasi.json",
                                "pref" : "1"
                            },
                            {
                                "yearType" : "2020",
                                "link" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/1-sma-prestasi.json",
                                "linkVoc" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/kompetensi/1-sma-prestasi.json",
                                "pref" : "2"
                            }
                ],
                "smk" : [
                            {
                                "yearType" : "current",
                                "link" : "https://ppdb.jakarta.go.id/sekolah/1-smk-prestasi.json",
                                "linkVoc" : "https://ppdb.jakarta.go.id/sekolah/kompetensi/1-smk-prestasi.json",
                                "pref" : "1"
                            },
                            {
                                "yearType" : "2020",
                                "link" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/2-smk-prestasi.json",
                                "linkVoc" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/kompetensi/2-smk-prestasi.json",
                                "pref" : "2"
                            }                    
                ]
            }
        }
    def __askSchoolType(self,err=""):
        print(f"""
[!] Jakarta Only [!]
[?] Choose school type : {err}
 ➥ [!] choose by number
   ➥ [1] . smp
   ➥ [2] . sma
   ➥ [3] . smk
        """)
        try:
            inputer = int(input("[?] : "))
            if inputer in range(1,4):
                getSchoolType = self.data["accepted"]["sctype"].get(str(inputer))
                if getSchoolType != None:
                    self.credFromCurrent["schoolType"] = getSchoolType
                    return True
            else:
                return self.__askSchoolType(err="max length 3")
        except ValueError:
            return self.__askSchoolType(err="invalid Type")
    
    def __requestFromChosenSchool(self,schoolData):
        try:
            def loopQ(ldata):
                try:
                    num = int(input(f"[?] choose (for {schoolData['yearType']}): "))
                    num = num -1
                    if num < 0 or num > (ldata -1):
                        return loopQ(ldata)
                    else:
                        return num
                except ValueError:
                    print("invalid type")
                    return loopQ(ldata)
            
            print(f"\n[O] {schoolData['yearType']}'s Section")
            r = requests.get(schoolData["link"],timeout=3)
            if r.status_code == 200:
                jsoned = r.json()
                for key,value in enumerate(jsoned):
                    print(f"  ➥ [{key+1}] . {value['nama']}")
                chosen = loopQ(len(jsoned))
                data = jsoned[chosen]
                afterR = requests.get(schoolData["linkVoc"],timeout=3)
                jsonedAfterR = afterR.json()
                self.credFromCurrent["eachDataId"].append({
                    "schoolName" : data["nama"],
                    "err" : False,
                    "id" : data["sekolah_id"],
                    "yearType" : schoolData["yearType"],
                    "pref" : schoolData["pref"],
                    "data" : jsonedAfterR[data["sekolah_id"]]
                })
            else:
                self.credFromCurrent["eachDataId"].append({
                    "schoolName" : data["nama"],
                    "err" : True,
                    "id" : data["sekolah_id"],
                    "yearType" : schoolData["yearType"],
                    "pref" : schoolData["pref"],
                    "data" : jsonedAfterR[data["sekolah_id"]]
                })
                self.errorLog["MainError"].append({
                    "cred" : f"{schoolData['yearType']}"
                })
        except:
            print("")
    def __createEachJsonData(self):
        tobereturned = []
        for item in self.credFromCurrent["eachDataId"]:
            if item["err"] == False:
                print(f"[~] Begin to request {item['schoolName']}-{item['yearType']}")
                jsonBucket = []
                for subitem in item["data"]:
                    try:
                        merged = f"{self.data['linkSchool'][item['yearType']]}{self.credFromCurrent['schoolType']}/{item['pref']}-{item['id']}-{subitem[0]}.json"
                        r = requests.get(merged,timeout=3)
                        if r.status_code == 200:
                            print(f"  ➥ [✓] success to request {item['schoolName']} - {subitem[1]}")
                            jsonBucket.append({
                                "api" : merged,
                                "vocType" : f"{subitem[1].replace(' ','-')}_{item['schoolName'].replace(' ','-')}"
                            })
                        else:
                            self.errorLog["subMainError"].append({
                                "cred" : f"{item['schoolName']} - {subitem[1]} - {item['yearType']}"
                            })
                    except Exception as E:
                        print(f"  ➥ [x] failed to request {item['schoolName']} : Connection Err")
                tobereturned.append({
                    "yearType" : item['yearType'],
                    "sourceDataLink" :  jsonBucket
                })
        return tobereturned

    def __createJsonFile(self,data,fileName="data_1"):
        fileName = f"{fileName}.json"
        with open(f"{fileName}","w") as f:
            newdata = {
                "data" : data
            }
            f.write(json.dumps(newdata,indent=3))
            print(f"[✓] Successfully create {fileName}")
            return True

    def __beginIfCredIsDone(self):
        print()
        if len(set([item["id"] for item in self.credFromCurrent["eachDataId"]])) == 1:
            return self.__createEachJsonData()
        else:
            print("[!] Both data are not the same [!]")
            yesOrNo = str(input("[?] Do yo really want to procceed this data (yes/no)? "))
            if yesOrNo.lower() == "no":
                print("Abort")
                return False
            return self.__createEachJsonData()
        
    def __logError(self):
        pre = "Cant Retrify"
        def loop(data):
            for item in data:
                print(f"  ➥ [x] {pre} {item['cred']}")
        print("\n[!] Error Log")
        logNum = 0
        if self.errorLog["mainError"]:
            loop(self.errorLog["mainError"])
            logNum += 1
        elif self.errorLog["subMainError"]:
            loop(self.errorLog["subMainError"])
            logNum += 1
        else:
            print("  ➥ [✓] All Connection went Succes")
        return logNum

    def make(self):
        try:
            if self.__askSchoolType():
                for item in self.data["school"][self.credFromCurrent["schoolType"]]:
                    self.__requestFromChosenSchool(item)
                bucket = self.__beginIfCredIsDone()
                if bucket:
                    err = self.__logError()
                    if err > 0:
                        def askE():
                            askEr = str(input("\nError(s) occured, Do you really want to proccess (y/n) : "))
                            if askEr == "y" or askEr == "n":
                                return askEr
                            else:
                                print("[x] invalid Input")
                                return askE()
                        answer = askE()
                        if answer == "n":
                            return False
                        else:
                            ask = str(input("\n[?] fileName (default: data1) : "))
                            return self.__createJsonFile(bucket,fileName=ask)        
                    ask = str(input("\n[?] fileName (default: data1) : "))
                    return self.__createJsonFile(bucket,fileName=ask)
        except KeyboardInterrupt:
            print("\nadios")