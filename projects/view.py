import json
import pymongo 
from flask import request, jsonify,make_response
from flask_restful import Resource
from project_monitor.resources.errors import mongo_error,sql_server, server_down,status_sucess
from project_monitor.projects.methods import check_mongo, check_api,check_mongo360, docnms_api,ftcr_dashboard,ftcr_missmatch,flte_dashboard,flte_missmatch

class PortalMonitoring(Resource):
    def get(self):
        project_status = []
        projects = ["ftcr","docnms","eprobes"]
        ftcr,docnms= {},{}
        for project in projects:
            url = "http://10.106.22.170:3002/epTestList"
            #url = http://217.165.211.39:5045/rcDashboard
                #params usecase_id=10&startdate=2023-10-03&team_id=1%20
            if project == "ftcr": 
                check_mongo_server = check_mongo()
                check_api_server = check_api(url)
                if check_mongo_server is not True:
                    ftcr['project'] = 'ftcr'
                    ftcr['status']= "Down"
                    ftcr['reason'] = "Mongo server is down"
                    project_status.append(ftcr)
                elif check_api_server is not True:
                    ftcr['project'] = 'ftcr'
                    ftcr['status']= "Down"
                    ftcr['reason'] = "Api server is down"
                    project_status.append(ftcr)
                elif (check_mongo_server is  True) and (check_api_server is True):
                    ftcr['project'] = 'ftcr'
                    ftcr['status']= "Up"
                    ftcr['reason'] = "Working fine"
                    project_status.append(ftcr)

            if project == "docnms":
                url = "http://10.106.22.169:8400/docnmsFilterValues"
                check_mongo_server = check_mongo360()
                #params 
                check_api_server = check_api(url)
                if check_mongo_server is not True:
                    docnms['project'] = 'docnms'
                    docnms['status']= "Down"
                    docnms['reason'] = "Mongo server is down"
                    project_status.append(docnms)
                elif check_api_server is not True:
                    docnms['project'] = 'docnms'
                    docnms['status']= "Down"
                    docnms['reason'] = "Api server is down"
                    project_status.append(docnms)
                elif (check_mongo_server is  True) and (check_api_server is True):
                    docnms['project'] = 'docnms'
                    docnms['status']= "Up"
                    docnms['reason'] = "Working fine"
                    project_status.append(docnms)

            if project == "eprobes": 
                eprobes = {}
                url = "http://10.106.22.170:3002/epFilterValues"
                check_mongo_server = check_mongo()
                check_api_server = check_api(url)
                if check_mongo_server is not True:
                    eprobes['project'] = 'eprobes'
                    eprobes['status']= "Down"
                    eprobes['reason'] = "Mongo server is down"
                    project_status.append(eprobes)
                elif check_api_server is not True:
                    eprobes['project'] = 'eprobes'
                    eprobes['status']= "Down"
                    eprobes['reason'] = "Api server is down"
                    project_status.append(eprobes)
                elif (check_mongo_server is  True) and (check_api_server is True):
                    eprobes['project'] = 'eprobes'
                    eprobes['status']= "Up"
                    eprobes['reason'] = "Working fine"
                    project_status.append(eprobes)

        return jsonify(project_status)




class PortalDetails(Resource):
    def post(self):
        project = request.json.get("project_name")
        project_detail = []
        if project == "ftcr":
            modules = ["corevoice","ont","ontnew","router","iptv","flte"]
            for module in modules:
            if module == "corevoice":
                corevoice = {}
                corevoice1 = {}
                ucs1 = []
                ucs = []
                usecase_ids = ["2010","2011","2013","2014","2015","2016","2017",
                "2018","2019","2050","2051","2052","2080","2090","2910","2920","2930","2940","2950","2960","2970"]
                for usecase_id in usecase_ids:
                    api_response = ftcr_dashboard(int(usecase_id))
                    details_resp = ftcr_missmatch(str(usecase_id))
                    if len(details_resp) == 1:
                        ucs1.append(usecase_id)
                    if len(api_response) == 1:
                        ucs.append(usecase_id)
                if ucs == []:
                    corevoice["project"] = "ftcr(corevoice(dashboard))"
                    corevoice["status"] = "Up"
                    corevoice["reason"] = "Working fine"
                    project_detail.append(corevoice)
                elif ucs != []:
                    corevoice["project"] = "ftcr(corevoice(dashboard))"
                    corevoice["status"] = "Down"
                    corevoice["reason"] = f'{ucs} no data from bigdata server'
                    project_detail.append(corevoice)

                if ucs1 == []:
                    corevoice1["project"] = "ftcr(corevoice(mismatch))"
                    corevoice1["status"] = "Up"
                    corevoice1["reason"] = "Working fine"
                    project_detail.append(corevoice1)
                elif ucs1 != []:
                    corevoice1["project"] = "ftcr(corevoice(mismatch))"
                    corevoice1["status"] = "Down"
                    corevoice1["reason"] = f'{ucs} no data from bigdata server'
                    project_detail.append(corevoice1)

            if module == "router":
                router = {}
                router1 = {}
                ucs1 = []
                ucs = []
                usecase_ids = ["3030","3040","3170","3210","3220","3240","3250","3260","3270","3280","3291","3451"]
                for usecase_id in usecase_ids:
                    details_resp = ftcr_missmatch(str(usecase_id))
                    if len(details_resp) == 1:
                        ucs1.append(usecase_id)
                    api_response = ftcr_dashboard(int(usecase_id))
                    if len(api_response) == 1:
                        ucs.append(usecase_id)
                if ucs == []:
                    router["project"] = "ftcr(router(dashboard))"
                    router["status"] = "Up"
                    router["reason"] = "Working fine"
                    project_detail.append(router)
                elif ucs != []:
                    router["project"] = "ftcr(router(dashboard))"
                    router["status"] = "Down"
                    router["reason"] = f'{ucs} no data from bigdata server'
                    project_detail.append(router)

                if ucs1 == []:
                    router1["project"] = "ftcr(router(mismatch))"
                    router1["status"] = "Up"
                    router1["reason"] = "Working fine"
                    project_detail.append(router1)
                elif ucs != []:
                    router1["project"] = "ftcr(router(mismatch))"
                    router1["status"] = "Down"
                    router1["reason"] = f'{ucs} no data from bigdata server'
                    project_detail.append(router1)

            if module == "ont":
                ont = {}
                ont1 = {}
                ucs1 = []
                ucs = []
                usecase_ids = ["6010","6020","6030","6040","6050","6060","6070",
                "6080","6100","6110","6120","6130","6140","6150","6160","6170","6180"]
                for usecase_id in usecase_ids:
                    api_response = ftcr_dashboard(int(usecase_id))
                    details_resp = ftcr_missmatch(str(usecase_id))
                    if len(details_resp) == 1:
                        ucs1.append(usecase_id)
                    if len(api_response) == 1:
                        ucs.append(usecase_id)
                if ucs == []:
                    ont["project"] = "ftcr(ont(missmatch))"
                    ont["status"] = "Up"
                    ont["reason"] = "Working fine"
                    project_detail.append(ont)
                elif ucs != []:
                    ont["project"] = "ftcr(ont(mismatch))"
                    ont["status"] = "Down"
                    ont["reason"] = f'{ucs} no data from bigdata server'
                    project_detail.append(ont)
                
                if ucs1 == []:
                    ont1["project"] = "ftcr(ont(missmatch))"
                    ont1["status"] = "Up"
                    ont1["reason"] = "Working fine"
                    project_detail.append(ont1)
                elif ucs1 != []:
                    ont1["project"] = "ftcr(ont(missmatch))"
                    ont1["status"] = "Down"
                    ont1["reason"] = f'{ucs} no data from bigdata server'
                    project_detail.append(ont1)

            if module == "ontnew":
                ontnew = {}
                ontnew1 = {}
                ucs1 = []
                ucs = []
                usecase_ids = ["7010","7020","7030","7040","7050","7060","7070","7080","7100","7110","7120","7130","7140","7150","7160","7170","7180","7190","7200"]
                for usecase_id in usecase_ids:
                    api_response = ftcr_dashboard(int(usecase_id))
                    if len(details_resp) == 1:
                        ucs.append(usecase_id)
                if ucs == []:
                    ontnew["project"] = "ftcr(ontnew(dashboard))"
                    ontnew["status"] = "Up"
                    ontnew["reason"] = "Working fine"
                    project_detail.append(ontnew)
                elif ucs != []:
                    ontnew["project"] = "ftcr(ontnew(dashboard))"
                    ontnew["status"] = "Down"
                    ontnew["reason"] = f'{ucs} no data from bigdata server'
                    project_detail.append(ontnew)

                if ucs1 == []:
                    ontnew1["project"] = "ftcr(ontnew(mismatch))"
                    ontnew1["status"] = "Up"
                    ontnew1["reason"] = "Working fine"
                    project_detail.append(ontnew1)
                elif ucs1 != []:
                    ontnew1["project"] = "ftcr(ontnew(mismatch))"
                    ontnew1["status"] = "Down"
                    ontnew1["reason"] = f'{ucs} no data from bigdata server'
                    project_detail.append(ontnew1)
            
            if module == "flte":
                flte = {}
                ucs = []
                usecase_ids = ["1","3","5","6","7","8","10",
                "12","13","14"]
                for usecase_id in usecase_ids:
                    api_response = flte_dashboard(int(usecase_id))
                    if len(api_response) == 0:
                        ucs.append(usecase_id)
                if ucs == []:
                    flte["project"] = "ftcr(flte(dashboard))"
                    flte["status"] = "Up"
                    flte["reason"] = "Working fine"
                    project_detail.append(flte)
                elif ucs != []:
                    flte["project"] = "ftcr(flte(dashboard))"
                    flte["status"] = "Down"
                    flte["reason"] = f'{ucs} no data from bigdata server'
                    project_detail.append(flte)

            if module == "iptv":
                iptv = {}
                ucs = []
                usecase_ids = ["1","2","3","5","6","7","8","10",
                "12","13","14","15","16","18","19","20"]
                for usecase_id in usecase_ids:
                    api_response = ftcr_dashboard(int(usecase_id))
                    if len(api_response) == 1:
                        ucs.append(usecase_id)
                if ucs == []:
                    iptv["project"] = "ftcr(iptv(dashboard))"
                    iptv["status"] = "Up"
                    iptv["reason"] = "Working fine"
                    project_detail.append(iptv)
                elif ucs != []:
                    iptv["project"] = "ftcr(iptv(dashboard))"
                    iptv["status"] = "Down"
                    iptv["reason"] = f'{ucs} no data from bigdata server'
                    project_detail.append(iptv)


        if project == "docnms":
            docnms = {}
            api_resp = docnms_api()
            if api_resp is not False:
                if len(api_resp) == 0:
                    docnms["project"]  = "docnms"
                    docnms["status"] = "Up"
                    docnms["reason"] = "Working Fine"
                    project_detail.append(docnms)
                else:
                    docnmsms["project"]  = "docnms"
                    docnms["status"] = "Down"
                    docnms["reason"] = f" no  data avilable for regions {api_resp}"
                    project_detail.append(docnms)
            else:
                docnmsms["project"]  = "docnms"
                docnms["status"] = "Down"
                docnms["reason"] = f" not able to connect to the bigdtata server"
                project_detail.append(docnms)
        return jsonify(project_detail)
