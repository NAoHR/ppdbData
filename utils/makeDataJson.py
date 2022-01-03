class MakeDataJson:
    data = {
        "smp" : {
            "current" : {
                "link" : "https://ppdb.jakarta.go.id/sekolah/1-smp-prestasi.json"
            }
        },
        "sma" : {
            "current" : {
                "link" : "https://ppdb.jakarta.go.id/sekolah/1-sma-prestasi.json",
            },
        },
        "smk" : {
            "current" : {
                "link" : "https://ppdb.jakarta.go.id/sekolah/1-smk-prestasi.json"
            },
            "ayearBefore" : {
                "link" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/2-smk-prestasi.json"
            }
        }
    }    
    def __init__(self):
        return 