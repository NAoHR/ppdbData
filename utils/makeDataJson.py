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
            "linkSchool" :[
                {
                    "name" : "current",
                    "link" : "https://ppdb.jakarta.go.id/seleksi/prestasi/",
                },
                {
                    "name" : "current",
                    "link" : "https://arsip.siap-ppdb.com/2020/jakarta/seleksi/prestasi/"
                }
            ],
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
            self.credFromCurrent["eachId"].append(data["sekolah_id"])
            self.credFromCurrent["eachDataId"].append(jsonedAfterR[data["sekolah_id"]])
        except:
            return False
    # def __beginIfCredIsDone(self):

    def make(self):
        try:
            if self.__askSchoolType():
                for item in self.data["school"][self.credFromCurrent["schoolType"]]:
                    self.__requestFromChosenSchool(item)
                print(json.dumps(self.credFromCurrent,indent=3))
        except KeyboardInterrupt:
            print("adios")

a = MakeDataJson()
a.make()