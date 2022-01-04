# still on development, dont use this
import json
import requests


class MakeDataJson:    
    def __init__(self):
        self.credFromCurrent = {}
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
                            },
                            {
                                "yearType" : "2020",
                                "link" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/2-smp-prestasi.json",
                                "linkVoc" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/kompetensi/2-smp-prestasi.json"
                            }
                ],
                "sma" : [
                            {
                                "yearType" : "current",
                                "link" : "https://ppdb.jakarta.go.id/sekolah/1-sma-prestasi.json",
                                "linkVoc" : "https://ppdb.jakarta.go.id/sekolah/kompetensi/1-sma-prestasi.json",
                            },
                            {
                                "yearType" : "2020",
                                "link" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/1-sma-prestasi.json",
                                "linkVoc" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/kompetensi/1-sma-prestasi.json"
                            }
                ],
                "smk" : [
                            {
                                "yearType" : "current",
                                "link" : "https://ppdb.jakarta.go.id/sekolah/1-smk-prestasi.json",
                                "linkVoc" : "https://ppdb.jakarta.go.id/sekolah/kompetensi/1-smk-prestasi.json",
                            },
                            {
                                "yearType" : "2020",
                                "link" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/2-smk-prestasi.json",
                                "linkVoc" : "https://arsip.siap-ppdb.com/2020/jakarta/sekolah/kompetensi/2-smk-prestasi.json"
                            }                    
                ]
            }
        }