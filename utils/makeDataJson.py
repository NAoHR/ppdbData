# still on development, dont use this
import json
import requests
from requests.exceptions import ReadTimeout


class MakeDataJson:    
    def __init__(self):
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
                                "pref" : "1"
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
[?] Choose school type : {err}
 ➥ [!] choose by number
   ➥ [~] 1. smp
   ➥ [~] 2. sma
   ➥ [~] 3. smk
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
            jsoned = r.json()
            for key,value in enumerate(jsoned):
                print(f"  ➥ [~] {key+1}. {value['nama']}")
            chosen = loopQ(len(jsoned))
            data = jsoned[chosen]
            afterR = requests.get(schoolData["linkVoc"],timeout=3)

            jsonedAfterR = afterR.json()
            self.credFromCurrent["eachDataId"].append({
                "schoolName" : data["nama"],
                "id" : data["sekolah_id"],
                "yearType" : schoolData["yearType"],
                "pref" : schoolData["pref"],
                "data" : jsonedAfterR[data["sekolah_id"]]
            })
        except:
            return False

    def __createEachJsonData(self):
        tobereturned = []
        for item in self.credFromCurrent["eachDataId"]:
            jsonBucket = []
            for subitem in item["data"]:
                merged = f"{self.data['linkSchool'][item['yearType']]}/{self.credFromCurrent['schoolType']}/{item['pref']}-{item['id']}-{subitem[0]}.json"
                r = requests.get(merged)
                if r.status_code == 200:
                    jsonBucket.append({
                        "api" : merged,
                        "vocType" : f"{subitem[1].replace(' ','-')}_{item['schoolName'].replace(' ','-')}"
                    })
            tobereturned.append({
                "yearType" : item['yearType'],
                "sourceDataLink" :  jsonBucket
            })
        return tobereturned

    def __createJsonFile(self,data,fileName="data_1"):
        with open(f"{fileName}.json","w") as f:
            newdata = {
                "data" : data
            }
            f.write(json.dumps(newdata,indent=3))
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
            print("zamn")
            return self.__createEachJsonData()
        

    def make(self):
        try:
            if self.__askSchoolType():
                for item in self.data["school"][self.credFromCurrent["schoolType"]]:
                    self.__requestFromChosenSchool(item)
                bucket = self.__beginIfCredIsDone()
                if bucket:
                    ask = str(input("[?] fileName (default: data1) : "))
                    return self.__createJsonFile(bucket,fileName=ask)
        except KeyboardInterrupt:
            print("adios")

a = MakeDataJson()
a.make()