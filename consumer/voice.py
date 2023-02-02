import requests
import json
from datetime import datetime, timedelta
from collections import OrderedDict
import json
import os
import copy
import urllib.parse
import time
from csv import DictReader
from datetime import datetime
from logging import exception
from helpers.constant import *


print(temp)
from helpers.TataAuth import Auth
tata_auth_token = Auth()

def checkPrintLog(data):
    print("he he he he eh he orewa dankihote Doflamingo!")
    return "he he he he eh he orewa dankihote Doflamingo!"

def validate_res(res):
    if 'message' in res:
        if (res['message'] == 'Missing required request parameters: [Authorization]'):
            tata_auth_token.set_token(generateTataTeleAuthToken())
            return {"status":False,"message":"retry again token got missing"}
        elif 'success' in res and 'message' in res:
            if(res['success'] == False or res['message'] == 'Deleted or blacklisted token provided'):
                tata_auth_token.set_token(generateTataTeleAuthToken())
                return {"status":False,"message":"retry again token got blacklisted"}
        elif(res['message'] == 'Token has expired'):
            tata_auth_token.set_token(generateTataTeleAuthToken())
            return {"status":False,"message":"retry again token got expired"}
    return {"status": True,"message":res}
# auth token for authentication for all API's
def generateTataTeleAuthToken():
    global MTALKZ_SMARTFLOW_AUTH_TOKEN
    try:
        global MTALKZ_SMARTFLOW_AUTH_TOKEN
        print('generateTataTeleAuthToken')
        payload = {
                "email": "Shelly@mtalkz.com",
                "password": "1wEcD#HyG2Ern_gr"
            }
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        response = requests.post(
            MTALKZ_SMARTFLOW_PANEL_LOGIN_FOR_TOKEN, json=payload, headers=headers)
        # print(type(response))
        res = response.json()
        # print(res)
        # MTALKZ_SMARTFLOW_AUTH_TOKEN['Authorization'] = str(res.get('access_token', ''))
        # tata_auth_token.token = res.get('access_token', None)
        # print("MTALKZ_SMARTFLOW_AUTH_TOKEN :: " + MTALKZ_SMARTFLOW_AUTH_TOKEN['Authorization'])
        tata_auth_token.token = copy.deepcopy(res.get('access_token', None))
        if tata_auth_token.token:
            print("tata_auth_token :: >> " + tata_auth_token.token)
        else:
            print("tata_auth_token.token API response ::: " + str(res))
        # return MTALKZ_SMARTFLOW_AUTH_TOKEN['Authorization']
        return tata_auth_token.token


    except Exception as e:
        global MTALKZ_SMARTFLOW_AUTH_TOKEN
        print("error is =>", e)
        tata_auth_token.token = None
        return tata_auth_token.token

    finally:
        # tata_auth_token.token = None
        return tata_auth_token.token

# call patch tatatele
def callpatch(data):
    try:
        payload = {
            "agent_number": None,"destination_number": None,"get_call_id": 1,"caller_id": None,"call_timeout": 120
            } 
        headers = {
            "accept": "application/json","Authorization": "","content-type": "application/json"
            }
        if data is None:
            return {"status": False,"message":"data is required but not provided"}
        token = tata_auth_token.get_token(time.time())
        if token is None:
            tata_auth_token.set_token(generateTataTeleAuthToken())
        headers['Authorization'] = tata_auth_token.get_token(time.time())
        if 'from' in data:
            payload['agent_number'] = data['from']
        else:
            return {"status": False,"message":"agent_number is required but not provided"}
        if 'to' in data:
            payload['destination_number'] = data['to']
        else:
            return {"status": False,"message":"destination_number is required but not provided"}
        if 'caller_id' in data:
            payload['caller_id'] = data['caller_id']
        else:
            return {"status": False,"message":"caller_id is required but not provided"}
        if 'call_timeout' in data:
            payload['call_timeout'] = data['call_timeout']
        
        response = requests.post(MTALKZ_SMARTFLOW_CALLPATCH_URL, json=payload, headers=headers)
        res = response.json()
        print(res)
        result = validate_res(res)
        return result
    except Exception as e:
        print("error :::callpatch tatatele ::::::::::: ",e)

# Enter lead object in lead list
def enter_lead(data):
    try:
        leadListId = None
        leadObj = {"field_0": None}
        listOfNumbers = []
        listOfLeadObject = []
        payload = {"data": []}
        headers = {
            "accept": "application/json","Authorization": "token","content-type": "application/json"
        }
        if data is None:
            return {"status": False,"message":"data is required but not provided"}

        token = tata_auth_token.get_token(time.time())
        if token is None:
            tata_auth_token.set_token(generateTataTeleAuthToken())
        headers['Authorization'] = tata_auth_token.get_token(time.time())
        # if (data['field_0'] is None):
        #     return jsonify({"status", "Phone Number field is empty"})
        if 'campaign' in data:
            leadListId = data['campaign']
        else:
            return {"status": False,"message":"campaign is required but not provided"}
        if 'to' in data:
            listOfNumbers = data['to']
        else:
            return {"status": False,"message":"to is required but not provided"}

        for number in listOfNumbers:
            leadObj = {"field_0": None}
            leadObj['field_0'] = str(number)
            listOfLeadObject.append(leadObj)

        payload['data'] = listOfLeadObject
        print(payload)
        response = requests.post(MTALKZ_SMARTFLOW_ENTER_LEAD_IN_LEAD_LIST_URL+str(leadListId), json=payload, headers=headers)
        res = response.json()
        print(res)
        result = validate_res(res)
        return result
    except Exception as e:
        print("error :::enter_lead ::::::::::: ",e)

# Create Broadcast
def create_broadcast(data):
    try:
        print("###########::::::::create_broadcast:::::::::##########")
        payload = {"name": None,"description": None,"phone_number_list": None,"destination": None,
            "timeout": None,"concurrent_limit": None,"retry_after_minutes": None,"caller_id_number": None,
            "number_of_retry": None,"start_date_time": None,"end_date_time": None
        }
        headers = {
            "accept": "application/json","Authorization": "token","content-type": "application/json"
        }
        if data is None:
            return {"status": False,"message":"data is required but not provided"}

        if 'name' in data:
            payload['name'] = data['name']
        else:
            return {"status": False,"message":"name is required but not provided"}
        if 'description' in data:
            payload['description'] = data['description']
        else:
            return {"status": False,"message":"description is required but not provided"}
        if 'phone_number_list' in data:
            payload['phone_number_list'] = data['phone_number_list']
        else:
            return {"status": False,"message":"phone_number_list is required but not provided"}
        if 'destination' in data:
            payload['destination'] = data['destination']
        else:
            return {"status": False,"message":"destination is required but not provided"}
        if 'timeout' in data:
            payload['timeout'] = data['timeout']
        else:
            return {"status": False,"message":"timeout is required but not provided"}
        if 'concurrent_limit' in data:
            payload['concurrent_limit'] = data['concurrent_limit']
        else:
            return {"status": False,"message":"concurrent_limit is required but not provided"}
        if 'retry_after_minutes' in data:
            payload['retry_after_minutes'] = data['retry_after_minutes']
        else:
            return {"status": False,"message":"retry_after_minutes is required but not provided"}
        if 'caller_id_number' in data:
            payload['caller_id_number'] = data['caller_id_number']
        else:
            return {"status": False,"message":"caller_id_number is required but not provided"}
        if 'number_of_retry' in data:
            payload['number_of_retry'] = data['number_of_retry']
        else:
            return {"status": False,"message":"number_of_retry is required but not provided"}
        if 'start_date_time' in data:   
            payload['start_date_time'] = data['start_date_time']
        else:
            return {"status": False,"message":"start_date_time is required but not provided"}
        if 'end_date_time' in data:
            payload['end_date_time'] = data['end_date_time']
        else:
            return {"status": False,"message":"end_date_time is required but not provided"}

        token = tata_auth_token.get_token(time.time())
        if token is None:
            tata_auth_token.set_token(generateTataTeleAuthToken())
        headers['Authorization'] = tata_auth_token.get_token(time.time())
        response = requests.post(MTALKZ_SMARTFLOW_CREATE_BROADCAST_URL, json=payload, headers=headers)
        # print(type(response))
        res = response.json()
        # print(res)
        result = validate_res(res)
        return result
    except Exception as e:
        print("error :::create_broadcast:::::::: ",e)

# Start Broadcast
def start_broadcast(data):
    try:
        print("######## ::::start_broadcast:::: ######## ")
        broadcastId = None
        headers = {
            "accept": "application/json",
            "Authorization": "token"
        }
        if data is None:
            return {"status": False,"message":"data is required but not provided"}
        if 'id' in data:
            broadcastId = data['id']
        token = tata_auth_token.get_token(time.time())
        if token is None:
            tata_auth_token.set_token(generateTataTeleAuthToken())
        headers['Authorization'] = tata_auth_token.get_token(time.time())
        response = requests.get(MTALKZ_SMARTFLOW_START_BROADCAST_URL+str(broadcastId), headers=headers)
        res = response.json()
        print(res)
        result = validate_res(res)
        return result
    except Exception as e:
        print("error ::::start_broadcast::::::::: ",e)

# Pause Broadcast
def pause_broadcast(data):
    try:
        print("######## ::::pause_broadcast:::: ######## ")
        broadcastId = None
        headers = {
            "accept": "application/json",
            "Authorization": "token"
        }
        if data is None:
            return {"status": False,"message":"data is required but not provided"}
        if 'id' in data:
            broadcastId = data['id']
        token = tata_auth_token.get_token(time.time())
        if token is None:
            tata_auth_token.set_token(generateTataTeleAuthToken())
        headers['Authorization'] = tata_auth_token.get_token(time.time())
        response = requests.get(MTALKZ_SMARTFLOW_PAUSE_BROADCAST_URL+str(broadcastId), headers=headers)
        res = response.json()
        print(res)
        result = validate_res(res)
        return result
    except Exception as e:
        print("error pause_broadcast ::::::::::: ",e)

# Resume broadcast
def resume_broadcast(data):
    try:
        print("######## ::::resume_broadcast:::: ######## ")
        broadcastId = None
        headers = {
            "accept": "application/json",
            "Authorization": "token"
        }
        if data is None:
            return {"status": False,"message":"data is required but not provided"}
        if 'id' in data:
            broadcastId = data['id']
        token = tata_auth_token.get_token(time.time())
        if token is None:
            tata_auth_token.set_token(generateTataTeleAuthToken())
        headers['Authorization'] = tata_auth_token.get_token(time.time())
        response = requests.get(MTALKZ_SMARTFLOW_RESUME_BROADCAST_URL+str(broadcastId), headers=headers)
        res = response.json()
        print(res)
        result = validate_res(res)
        return result
    except Exception as e:
        print("error :::resume_broadcast ::::::::::: ",e)

# End broadcast
def end_broadcast(data):
    try:
        print("######## ::::end_broadcast:::: ######## ")
        broadcastId = None
        headers = {
            "accept": "application/json",
            "Authorization": "token"
        }
        if data is None:
            return {"status": False,"message":"data is required but not provided"}
        if 'id' in data:
            broadcastId = data['id']
        token = tata_auth_token.get_token(time.time())
        if token is None:
            tata_auth_token.set_token(generateTataTeleAuthToken())
        headers['Authorization'] = tata_auth_token.get_token(time.time())
        response = requests.get(MTALKZ_SMARTFLOW_END_BROADCAST_URL+str(broadcastId), headers=headers)
        res = response.json()
        print(res)
        result = validate_res(res)
        return result
    except Exception as e:
        print("error :::end_broadcast ::::::::::: ",e)


# Create Lead list
def create_leads_list(data):
    try:
        payload = {
            "field": [],
            "name": None,
            "description": None
        }
        headers = {
            "accept": "application/json",
            "Authorization": "token",
            "content-type": "application/json"
        }
        if data is None:
            return {"status": False,"message":"data is required but not provided"}

        payload['name'] = data['name']
        payload['description'] = data['description']
        payload['field'] = data['field']
        token = tata_auth_token.get_token(time.time())
        if token is None:
            tata_auth_token.set_token(generateTataTeleAuthToken())
        headers['Authorization'] = tata_auth_token.get_token(time.time())
        if payload['name'] is None:
            return {"status": "Enter Name of lead list"}
        if payload['description'] is None:
            return {"status": "Enter description of lead list"}
        if len(payload['field']) == 0:
            return {"status": "No entry of field specified"}
        response = requests.post(MTALKZ_SMARTFLOW_CREATE_LEAD_LIST_URL, json=payload, headers=headers)
        res = response.json()
        print(res)
        result = validate_res(res)
        return result
    except Exception as e:
        print("error :::create_lead_list ::::::::::: ",e)

# fetch all lead lists
def fetch_lead_lists():
    try:
        headers = {
            "accept": "application/json",
            "Authorization": "token",
        }
        token = tata_auth_token.get_token(time.time())
        if token is None:
            tata_auth_token.set_token(generateTataTeleAuthToken())
        headers['Authorization'] = tata_auth_token.get_token(time.time())
        response = requests.get(MTALKZ_SMARTFLOW_FETCH_LEAD_LIST_URL, headers=headers)
        res = response.json()
        print(res)
        result = validate_res(res)
        return result
    except Exception as e:
        print("error :::fetch_lead_list ::::::::::: ",e)

# update lead lists
def update_lead_least(data):
    try:
        payload = {
            "name": None,
            "description": None
        }
        headers = {
            "accept": "application/json",
            "Authorization": "token",
            "content-type": "application/json"
        }
        
        if data is None:
            return {'status': 'json data is none'}
        payload['name'] = data['name']
        payload['description'] = data['description']

        token = tata_auth_token.get_token(time.time())
        if token is None:
            tata_auth_token.set_token(generateTataTeleAuthToken())
        headers['Authorization'] = tata_auth_token.get_token(time.time())

        if payload['name'] is None:
            return {"status": "upto 25 char only is None"}
        if payload['description'] is None:
            return {"status": "description of lead list is None"}

        response = requests.put(MTALKZ_SMARTFLOW_UPDATE_LEAD_LIST_URL+str(data['id']), json=payload, headers=headers)
        res = response.json()
        print(res)
        result = validate_res(res)
        return result
    except Exception as e:
        print("error :::update_lead_list ::::::::::: ",e)


# delete lead list
def delete_lead_list(data):
    try:
        payload = {
            "id": None,
        }
        headers = {
            "accept": "application/json",
            "Authorization": "token",
        }
        if data is None:
            return {'status': 'json data is none'}

        token = tata_auth_token.get_token(time.time())
        if token is None:
            tata_auth_token.set_token(generateTataTeleAuthToken())
        headers['Authorization'] = tata_auth_token.get_token(time.time())

        if data['id'] is None:
            return {"status": "Enter ID of lead list to be deleted"}

        response = requests.delete(MTALKZ_SMARTFLOW_DELETE_LEAD_LIST_URL+str(data['id']), headers=headers)
        res = response.json()
        print(res)
        result = validate_res(res)
        return result
    except Exception as e:
        print("error :::delete_lead_list ::::::::::: ",e)


# GET leads ID of lead list with given id
def get_lead_id(data):
    try:
        headers = {
            "accept": "application/json",
            "Authorization": "token",
        }
        if data is None:
            return {'status': 'json data is none'}
        token = tata_auth_token.get_token(time.time())
        if token is None:
            tata_auth_token.set_token(generateTataTeleAuthToken())
        headers['Authorization'] = tata_auth_token.get_token(time.time())
        response = requests.get(MTALKZ_SMARTFLOW_GET_LEAD_ID+str(data['id']), headers=headers)
        res = response.json()
        print(res)
        result = validate_res(res)
        return result
    except Exception as e:
        print("error :::get_lead_id ::::::::::: ",e)


# # Update a lead
def update_lead(data):
    try:
        payload = {
            "field_0": "",
            "field_1": "",
            "field_5": "",
        }
        headers = {
            "accept": "application/json",
            "Authorization": "token",
            "content-type": "application/json"
        }
        if data is None:
            return {'status': 'json data is none'}
        token = tata_auth_token.get_token(time.time())
        if token is None:
            tata_auth_token.set_token(generateTataTeleAuthToken())
        headers['Authorization'] = tata_auth_token.get_token(time.time())
        if (data['contact'] is None):
            return {'status': 'there is no contact number provided'}
        payload['field_0'] = data['contact']
        payload['field_1'] = data['name']
        payload['field_5'] = data['otp']

        response = requests.put(MTALKZ_SMARTFLOW_UPDATE_LEAD+data['id'], json=payload, headers=headers)
        res = response.json()
        print(res)
        result = validate_res(res)
        return result
    except Exception as e:
        print("error :::update_lead ::::::::::: ",e)

# Delete a lead
def delete_lead(data):
    try:
        headers = {
            "accept": "application/json",
            "Authorization": "token",
        }
  
        if data is None:
            return {'status': 'json data is none'}
        token = tata_auth_token.get_token(time.time())
        if token is None:
            tata_auth_token.set_token(generateTataTeleAuthToken())
        headers['Authorization'] = tata_auth_token.get_token(time.time())
        response = requests.get(MTALKZ_SMARTFLOW_DELETE_LEAD_URL+str(data['id']), headers=headers)
        res = response.json()
        print(res)
        result = validate_res(res)
        return result
    except Exception as e:
        print("error :::delete_lead ::::::::::: ",e)


# fetch all ivr details
def fetch_ivr():
    try:
        headers = {
            "accept": "application/json",
            "Authorization": "token",
        }
        token = tata_auth_token.get_token(time.time())
        if token is None:
            tata_auth_token.set_token(generateTataTeleAuthToken())
        headers['Authorization'] = tata_auth_token.get_token(time.time())
        response = requests.get(MTALKZ_SMARTFLOW_FETCH_ALL_IVR, headers=headers)
        res = response.json()
        print(res)
        result = validate_res(res)
        return result
    except Exception as e:
        print("error :::fetch_ivr ::::::::::: ",e)

# Create IVR
def create_ivr(data):
    try:
        payload = {
            "name": "Test IVR Name",
            "description": "Test IVR Description",
            "recording": "recording||102410",
            "timeout": 30,
            "destination": [
                "extension||0503150060003"
            ],
            "incorrect_count": "1",
            "invalid_recording": "recording||102410",
            "invalid_destination": "extension||0503150060003",
            "timeout_retry_recording": "recording||102410",
            "timeout_recording": "recording||102410",
            "timeout_destination": "extension||0503150060003",
            "timeout_retries": 1,
            "recording_invalid": "recording||102410",
            "timeout_tries": 1,
            "option": [
                1
            ]
        }
        headers = {
            "accept": "application/json",
            "Authorization": "token",
            "content-type": "application/json"
        }
        if data is None:
            return {'status': 'json data is none'}
        payload['name'] = data['name']
        payload['description'] = data['description']
        payload['recording'] = data['recording']
        payload['timeout'] = data['timeout']
        payload['destination'] = data['destination']
        payload['incorrect_count'] = data['incorrect_count']
        payload['invalid_recording'] = data['invalid_recording']
        payload['invalid_destination'] = data['invalid_destination']
        payload['timeout_retry_recording'] = data['timeout_retry_recording']
        payload['timeout_recording'] = data['timeout_recording']
        payload['timeout_destination'] = data['timeout_destination']
        payload['timeout_retries'] = data['timeout_retries']
        payload['recording_invalid'] = data['recording_invalid']
        payload['timeout_retries'] = data['timeout_retries']
        payload['option'] = data['option']
        token = tata_auth_token.get_token(time.time())
        if token is None:
            tata_auth_token.set_token(generateTataTeleAuthToken())
        headers['Authorization'] = tata_auth_token.get_token(time.time())
        response = requests.post(MTALKZ_SMARTFLOW_CREATE_IVR, json=payload, headers=headers)
        res = response.json()
        print(res)
        result = validate_res(res)
        return result
    except Exception as e:
        print("error :::create_ivr ::::::::::: ",e)

# fetch recording
def fetch_Recording():
    try:
        headers = {
            "accept": "application/json",
            "Authorization": "token",
        }
        token = tata_auth_token.get_token(time.time())
        if token is None:
            tata_auth_token.set_token(generateTataTeleAuthToken())
        headers['Authorization'] = tata_auth_token.get_token(time.time())
        response = requests.get(MTALKZ_SMARTFLOW_FETCH_ALL_RECORDING, headers=headers)
        res = response.json()
        print(res)
        result = validate_res(res)
        return result
    except Exception as e:
        print("error :::fetch_Recording ::::::::::: ",e)

# get all auto attendants
def fetch_auto_attendant():
    try:
        headers = {
            "accept": "application/json",
            "Authorization": "token"
        }
        token = tata_auth_token.get_token(time.time())
        if token is None:
            tata_auth_token.set_token(generateTataTeleAuthToken())
        headers['Authorization'] = tata_auth_token.get_token(time.time())
        response = requests.get(MTALKZ_SMARTFLOW_FETCH_ALL_AUTO_ATTENDANTS, headers=headers)
        res = response.json()
        print(res)
        result = validate_res(res)
        return result
    except Exception as e:
        print("error :::fetch_auto_attendant ::::::::::: ",e)

# create auto attendants
def create_autoAttendant(data):
    try:
        payload = {
            "name": "Prop","description": "Prop description","recording_id": "44924",
            # "recording_type": "outbouns_tts",
            "recording_type": "outbound_tts","destination_id": "1","destination_type": "hangup"
        }
        headers = {
            "accept": "application/json",
            "Authorization": "token",
            "content-type": "application/json"
        }
        if data is None:
            return {'status': 'json data is none'}
        payload['name'] = data['name']
        payload['description'] = data['description']
        payload['recording_id'] = data['recording_id']
        payload['recording_type'] = data['recording_type']
        payload['destination_id'] = data['destination_id']
        payload['destination_type'] = data['destination_type']

        token = tata_auth_token.get_token(time.time())
        if token is None:
            tata_auth_token.set_token(generateTataTeleAuthToken())
        headers['Authorization'] = tata_auth_token.get_token(time.time())
        response = requests.post(MTALKZ_SMARTFLOW_CREATE_AUTO_ATTENDANTS, json=payload, headers=headers)
        res = response.json()
        print(res)
        result = validate_res(res)
        return result
    except Exception as e:
        print("error :::create_auto_attendant ::::::::::: ",e)


# fetch auto attenant by given id
def get_auto_attendant_by_id(data):
    try:
        headers = {
            "accept": "application/json",
            "Authorization": "token",
        }
        if data is None:
            return {'status': 'json data is none'}
        token = tata_auth_token.get_token(time.time())
        if token is None:
            tata_auth_token.set_token(generateTataTeleAuthToken())
        headers['Authorization'] = tata_auth_token.get_token(time.time())
        response = requests.get(MTALKZ_SMARTFLOW_FETCH_AUTO_ATTENDANTS+str(data['id']), headers=headers)
        res = response.json()
        print(res)
        result = validate_res(res)
        return result
    except Exception as e:
        print("error :::get_auto_attendant_by_id ::::::::::: ",e)


# agent creation api
def create_agent(data):
    try:
        payload = {
            "name": None,
            "follow_me_number": None,
            "intercom": None,
            "allowed_did_numbers": None
        }
        headers = {
            "accept": "application/json","Authorization": "","content-type": "application/json"
        }
        print("working here 3p")
        if data is None:
            return {'status': 'json data is none'}
        print("data = ", data)
        print("headers = ", headers)

        payload['name'] = data['name']
        payload['follow_me_number'] = data['follow_me_number']
        payload['intercom'] = data['intercom']
        payload['allowed_did_numbers'] = data['allowed_did_numbers']

        token = tata_auth_token.get_token(time.time())
        if token is None:
            tata_auth_token.set_token(generateTataTeleAuthToken())
        headers['Authorization'] = tata_auth_token.get_token(time.time())

        response = requests.post(MTALKZ_SMARTFLOW_CREATE_AGENT_URL, json=payload, headers=headers)
        res = response.json()
        print(res)
        result = validate_res(res)
        return result
    except Exception as e:
        print("error :::create_agent ::::::::::: ",e)


# fetch detail of lead from lead list
def fetch_lead(data):
    try:
        headers = {
        "accept": "application/json",
        "Authorization": "token"
        }

        if data is None:
                return {'status': False, 'error':"No lead-list id provided"}
        if 'leadlistid' in data:
            leadlistid = data['leadlistid']
        else:
            return {'status': False, 'error':"No lead-list id provided"}
        token = tata_auth_token.get_token(time.time())
        if token is None:
            tata_auth_token.set_token(generateTataTeleAuthToken())
        headers['Authorization'] = tata_auth_token.get_token(time.time())
        response = requests.get(MTALKZ_FETCH_LEAD_FROM__LEAD_LIST+str(leadlistid), headers=headers)
        res = response.json()
        print(res)
        result = validate_res(res)
        return result
    except Exception as e:
        print("error :::fetch_lead ::::::::::: ",e)

