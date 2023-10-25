import pymongo
import requests
from datetime import datetime,timedelta
import json
from flask import jsonify
import pymssql

# FTCR Mongo
def check_mongo():
    try:
        client = pymongo.MongoClient("mongodb://thedash:dash1234@10.237.238.172:27017/iptv_analytics?replicaSet=rs0")
        print("mongo connected successfully")
        # Close the connection
        client.close()
        # If you reached this point, the connection was successful
        return True
    except Exception as e:
        # Handle connection failure (e.g., log the error)
        print(f"MongoDB Connection Error: {e}")
        return False

# general api's
def check_api(url):
    try:
        response = requests.get(url)
        # Check if the status code is in the 2xx range, indicating success
        #response.raise_for_status()
        print(f"API is working. Status code: {response.status_code}")
        return True
    except Exception as e:
        print(f"API is not working. Error: {e}")
        return False

# docnms eprobes asoc switch_tv unoc access_request soc mongo
def check_mongo360():
    try:
        client = pymongo.MongoClient("mongodb://thedash:dash1234@10.106.22.172:27017/iptv_analytics?replicaSet=rs0")
        # Close the connection
        client.close()
        # If you reached this point, the connection was successful
        return True
    except Exception as e:
        # Handle connection failure (e.g., log the error)
        print(f"MongoDB Connection Error: {e}")
        return False

# docnms api check
def docnms_api():
    try:
        cnxn = pymssql.connect(server='10.237.91.212',user='ohm',password='ohm',database='IPTV_analytics')
        cursor = cnxn.cursor()
        tm = datetime.now()
        startdate = tm+timedelta(days=0)
        enddate = startdate+timedelta(days=0)
        start = startdate.replace(hour=0, minute=0, second=0, microsecond=0)
        end = enddate.replace(hour=23, minute=59, second=59, microsecond=0)
        start = start.strftime("%Y-%m-%d %H:%M:%S")
        end = end.strftime("%Y-%m-%d %H:%M:%S")
        region = ["AAN","AUH","DXB","EC","RAK","WC","WR"]
        reg = []
        for r in region:
            query = "select load_datetime, replace(olt, ' ', '') as olt, sum(count) as ct from ReportingDWH.dbo.vw_tx_alarms_cnt where doctype='LOSI' and load_datetime>= '{}' and load_datetime<= '{}' and region in ('{}')  group by load_datetime,olt order by load_datetime desc".format(start,end,r)
            res = cursor.execute(query)
            res1 =cursor.fetchall()
            if list(res1) == []:
                reg.append(r)
        return reg
    except Exception as e:
        print(f"API is not working. Error: {e}")
        return False


# ftcr api's check
def ftcr_missmatch(usecase_id):
    try:
        startdate = datetime.now()
        startdate = startdate+timedelta(days=-1)
        enddate = startdate+timedelta(days=-1)
        enddatebd = startdate.strftime('%Y%m%d')
        startdatebd = enddate.strftime('%Y%m%d')
        url = '''http://10.237.230.138:8083/home/ftcr_detail?usecase_id='''+str(usecase_id)+'''&current_date='''+startdatebd+'''&end_date='''+enddatebd
        res = requests.get(url)
        return list(res)
    except Exception as e:
        print(f"API is not working. Error: {e}")
        return False

def flte_mismatch():
    try:
        cnxn = pymssql.connect(server='10.237.91.212',user='ohm',password='ohm',database='FTCR')
        cursor = cnxn.cursor()
        ucs = []
        UC1 = "select * from [FTCR].[dbo].flte_new_uc where usecase_num='UC 1' and usecase_name='Voice APN Missing ODU - ZTE'"
        UC2 = "select * from [FTCR].[dbo].flte_new_uc where usecase_num='UC 2' and usecase_name='SIP Registration Failures'"
        UC3 = "select * from [FTCR].[dbo].flte_new_uc where usecase_num='UC 3' and usecase_name='Poor Signal Quality ODU – ZTE'"
        UC4 = "select * from [FTCR].[dbo].flte_new_uc where usecase_num='UC 4' and usecase_name='WiFi Status IDU - Huawei'"
        UC5 = "select * from [FTCR].[dbo].flte_new_uc where usecase_num='UC 5' and usecase_name='WiFi Status IDU – ZTE'"
        UC6 = "select * from [FTCR].[dbo].flte_new_uc where usecase_num='UC 6' and usecase_name='High CPU Utilization IDU - Huawei'"
        UC7 = "select * from [FTCR].[dbo].flte_new_uc where usecase_num='UC 7' and usecase_name='High CPU Utilization IDU – ZTE'"
        UC8 = "select * from [FTCR].[dbo].flte_new_uc where usecase_num='UC 8' and usecase_name='High CPU Utilization ODU – ZTE'"
        UC9 = "select * from [FTCR].[dbo].flte_new_uc where usecase_num='UC 9' and usecase_name='High Memory Utilization IDU - Huawei'"
        UC10 = "select * from [FTCR].[dbo].flte_new_uc where usecase_num='UC 10' and usecase_name='High Memory Utilization IDU - ZTE'"
        UC11 = "select * from [FTCR].[dbo].flte_new_uc where usecase_num='UC 11' and usecase_name='High Memory Utilization ODU - ZTE'"
        UC12 = "select * from [FTCR].[dbo].flte_new_uc where usecase_num='UC 12' and usecase_name='Prolonged Device IDU - Huawei'"
        UC13 = "select * from [FTCR].[dbo].flte_new_uc where usecase_num='UC 13' and usecase_name='Prolonged Device IDU – ZTE'"
        UC14 = "select * from [FTCR].[dbo].flte_new_uc where usecase_num='UC 14' and usecase_name='Prolonged Device ODU – ZTE'"
        queries = [UC1,UC2,UC3,UC4,UC5,UC6,UC7,UC8,UC9,UC10,UC11,UC12,UC13,UC14]
        for query in queries:
            res = cursor.execute(query)
            res1 =cursor.fetchall()
            if list(res1) == []:
                ucs.append(query)
        return ucs
    except Exception as e:
        print(f"API is not working. Error: {e}")
        return False

def ftcr_dashboard(usecase_id):
    tm = datetime.now()
    startdate = tm+timedelta(days=-1)
    enddate = startdate+timedelta(days=-2)
    start = startdate.replace(hour=0, minute=0, second=0, microsecond=0)
    end = enddate.replace(hour=0, minute=0, second=0, microsecond=0)
    client = pymongo.MongoClient("mongodb://thedash:dash1234@10.237.238.172:27017/iptv_analytics?replicaSet=rs0")
    db = client['iptv_analytics']
    res = db.rcDashboardDaily.find({"usecase_id":usecase_id,"datetime":{"$gte":end,"$lte":start}})
    return list(res)

def flte_dashboard(usecase_id):
    tm = datetime.now()
    startdate = tm+timedelta(days=-1)
    enddate = startdate+timedelta(days=-2)
    start = startdate.replace(hour=0, minute=0, second=0, microsecond=0)
    end = enddate.replace(hour=0, minute=0, second=0, microsecond=0)
    start = start.strftime("%Y-%m-%d")
    end = end.strftime("%Y-%m-%d")
    client = pymongo.MongoClient("mongodb://thedash:dash1234@10.237.238.172:27017/iptv_analytics?replicaSet=rs0")
    db = client['iptv_analytics']
    res = db.flte_UCs.find({"usecase_id":usecase_id,"datetime":{"$gte":end,"$lte":start}})
    return res