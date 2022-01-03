class MakeDataJson:    
    def __init__(self,data,schoolType):
        self.data = {
            "smp" : {
                "current" : {
                    "link" : "https://ppdb.jakarta.go.id/sekolah/1-smp-prestasi.json"
                },
                "ayearBefore" : {
                    "link" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/1-smp-prestasi.json"
                },
                "eachVoc" : False
            },
            "sma" : {
                "yearType" : {
                    "current" : {
                        "link" : "https://ppdb.jakarta.go.id/sekolah/1-sma-prestasi.json",
                    },
                    "ayearBefore" : {
                        "link" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/1-sma-prestasi.json"
                    }
                },
                "eachVoc" : {
                    "current" : "https://ppdb.jakarta.go.id/sekolah/kompetensi/1-sma-prestasi.json",
                    "ayearBefore" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/kompetensi/1-sma-prestasi.json"
                }
            },
            "smk" : {
                "yearType" : {
                    "current" : {
                        "link" : "https://ppdb.jakarta.go.id/sekolah/1-smk-prestasi.json"
                    },
                    "ayearBefore" : {
                        "link" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/2-smk-prestasi.json"
                    }
                },
                "eachVoc" : {
                    "current" : "https://ppdb.jakarta.go.id/sekolah/kompetensi/1-smk-prestasi.json",
                    "ayearBefore" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/kompetensi/2-smk-prestasi.json"
                }
            }
        }
        self.schoolType = schoolType