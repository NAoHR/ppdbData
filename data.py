# HOW TO CREATE YOUR OWN DATA
# yearType -> to classify what kind of data you want to execute (current yoear or below it)
# sourceDataLink -> to store all of the api you are going to use
    # api -> fill this with a valid ppdb api link,go to ppdb website find your school,go to network and find the api that the website has requested to
    # vocType -> vocational type or wha kind of major this data filled with,either ipa,ips,kgsp,etc...
allData = [
    {
        "yearType" : "current",
        "sourceDataLink" : [
            {
                "api" : "https://ppdb.jakarta.go.id/seleksi/prestasi/smk/1-42010088-4.json",
                "vocType" : "kgsp"
            },
            {
                "api" : "https://ppdb.jakarta.go.id/seleksi/prestasi/smk/1-42010088-8.json",
                "vocType" : "ttl"
            },
            {
                "api" : "https://ppdb.jakarta.go.id/seleksi/prestasi/smk/1-42010088-14.json",
                "vocType" : "tflm"
            },
            {
                "api" : "https://ppdb.jakarta.go.id/seleksi/prestasi/smk/1-42010088-20.json",
                "vocType" : "tmpo"
            },
            {
                "api" : "https://ppdb.jakarta.go.id/seleksi/prestasi/smk/1-42010088-71.json",
                "vocType" : "sija"
            },
            {
                "api" : "https://ppdb.jakarta.go.id/seleksi/prestasi/smk/1-42010088-202.json",
                "vocType" : "tedk"
            }
        ]
    },
    {
        "yearType" : "2020",
        "sourceDataLink" : [
            {
                "api" : "https://arsip.siap-ppdb.com/2020/jakarta/seleksi/prestasi/smk/2-42010088-4.json",
                "vocType" : "kgsp"
            },
            {
                "api" : "https://arsip.siap-ppdb.com/2020/jakarta/seleksi/prestasi/smk/2-42010088-8.json",
                "vocType" : "ttl"
            },
            {
                "api" : "https://arsip.siap-ppdb.com/2020/jakarta/seleksi/prestasi/smk/2-42010088-14.json",
                "vocType" : "tflm"
            },
            {
                "api" : "https://arsip.siap-ppdb.com/2020/jakarta/seleksi/prestasi/smk/2-42010088-20.json",
                "vocType" : "tmpo"
            },
            {
                "api" : "https://arsip.siap-ppdb.com/2020/jakarta/seleksi/prestasi/smk/2-42010088-71.json",
                "vocType" : "sija"
            },
            {
                "api" : "https://arsip.siap-ppdb.com/2020/jakarta/seleksi/prestasi/smk/2-42010088-202.json",
                "vocType" : "tedk"
            }
        ]
    }
]