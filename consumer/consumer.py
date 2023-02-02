from kafka import KafkaConsumer
import json
import requests
import json
from voice import *
print("consume_message called successfully")
KAFKA_VERSION = (0, 10)
list = []

def returnProviderList(queueData):
    check = str(queueData['data']['integration']['provider'])
    checkProviderList = check.split('-')
    return checkProviderList

def master_functions(queueData):
    try:
        tataTeleApiFunDict = {"callpatch": callpatch,"obd":enter_lead,
                            "check":checkPrintLog,"createBroadcast":create_broadcast,
                            "startBroadcast":start_broadcast,"pauseBroadcast":pause_broadcast,
                            "resumeBroadcast":resume_broadcast,"endBroadcast":end_broadcast,
                            "createLeadList":create_leads_list,"fetchLeadList":fetch_lead_lists,
                            "fetchIvr":fetch_ivr,"createIvr":create_ivr,"fetchRecording":fetch_Recording,
                            "createAgent":create_agent,"fetchAutoAttendant":fetch_auto_attendant,
                            "createAutoAttendant":create_autoAttendant,"fetchLeadDetail":fetch_lead
                        }
        checkProvider = returnProviderList(queueData)
        print(checkProvider)
        # checking condition if provider is tatatele
        if checkProvider[0] == 'voice' and checkProvider[2] == 'tatatele':
            checkMidVal = str(checkProvider[1])
            # print("this is data in queue data",queueData['data'])
            res = tataTeleApiFunDict[checkMidVal](queueData['data'])
            # print("print in master function :::::::::: ",type(res))
            # print("print in master function :::::::::: ",res)
            return res
        # checking condition if provider is karix
        elif checkProvider[0] == '' and checkProvider[2] == 'karix':
            # Do nothing
            print("Do nothing")
            return {"status":False,"provider":"Karix"}
          
    except Exception as e:
        print(e)

consumer = KafkaConsumer('my_topic',
                bootstrap_servers=['kafka:9092'],
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),api_version=KAFKA_VERSION)


try:
    for message in consumer:
        print("Consumed message: ", message.value)
except Exception as e:
    print(e)
    print("inturuption from keyboard")
