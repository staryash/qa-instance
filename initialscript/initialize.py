import requests
import base64
import json 

# https://qa-instance.koiawaazsuno.in/api/clips produrl via nginx
# http://10.92.210.70:8081/api/clips direct prod url

qa_endpoint = "http://10.92.210.70:8081/api/clips"
base_log_dir = "/tts_data/call_center_audio_logs/transcripts/"
logfile_arr = ["62534252-b6cb-421a-9842-3504f237a32c.txt","852599af-1377-4fb6-bf2f-ba4d696e1571.txt","c310a7dc-d62e-463a-b6cb-12135402d1a2.txt","4a2c67b9-07d2-4614-bc6c-06053cea1228.txt","204e84dd-cfe3-4d2a-a6be-86f2ed338f0a.txt","e1ac7b31-fe06-4e37-a2cb-e1f0c13effd6.txt","59b22ecb-272e-4213-b7e7-445a328d92d4.txt","18a612b4-4324-45da-8a89-52510490d5db.txt","75dc138e-9974-4fd3-8d63-d2e6aec22371.txt"]

 
def read_audio_data(logfile):
    with open(logfile, "r") as lf:
        text = lf.readline()
 
    call_info = text.split("|")
    audio_path = call_info[0].strip()
    transcript_hi = call_info[1].strip()
    transcript_en = call_info[2].strip()
    intent = call_info[3].strip()
    ph_number = "na"
    if(len(call_info)>4):
        ph_number = call_info[4].strip()
        
    
 
    return {'audio_path': audio_path,
            'predicted_text': transcript_en,
            'predicted_intent': intent,
            'ph_number': ph_number }

def post_to_qa_portal(calldata):
 
    curr_call_attrs = {}
    curr_call_data = {}
    data = {}
    audio = {}

 
    audio_name = calldata["audio_path"]
    with open(audio_name, "rb") as af:
        audio_b64 = base64.b64encode(af.read())

    audio_file_name = audio_name.split('/')[len(audio_name.split('/')) - 1]
    curr_call_attrs["clip_path"] = audio_file_name
    curr_call_attrs["clip_src"] = "avaya"
    curr_call_attrs["language"] = "english"
    curr_call_attrs["predicted_intent"] = calldata["predicted_intent"]
    curr_call_attrs["predicted_text"] = calldata["predicted_text"]
    curr_call_attrs["meta_info"] = json.dumps({"phone": calldata["ph_number"]})

    audio_arr = []
    audio["name"] = audio_file_name
    audio["type"] = "audio/wav"
    audio["file"] = "data:audio/wav;base64,"+audio_b64.decode('utf-8')
    audio_arr.append(audio)

    curr_call_attrs["audio"] = audio_arr
 
    curr_call_data["type"] = "clips"
    curr_call_data["attributes"] = curr_call_attrs
    data["data"] = curr_call_data
    data["meta"] = {}

    payload = json.dumps(data)
    print(payload)
 
    response = requests.post( qa_endpoint, data=payload)
    return response
    # return data

for file in logfile_arr:
    calldata = read_audio_data(base_log_dir+file)
    response = post_to_qa_portal(calldata)
    print(response)
