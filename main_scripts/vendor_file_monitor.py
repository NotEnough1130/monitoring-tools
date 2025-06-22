import requests 
from companyA.frames.infra import OCiutil 
from requests_kerberos import HTTPKerberosAuth 
from datetime import datetime,  timedelta
import json 
import pytz
import os
from reactions.slack_reaction import post_msg_to_channel
from reactions.incidentio_reaction import msg_alert_to_OCpSupport

def get_date_range(delta):
    return datetime.today() - timedelta(days=delta)

def get_file_log(end_point,target_date):
    #Get API Keys
    load_dotenv()
    vda_secret_key = os.getenv('vda_secret_key') 
    vda_OCI_key = os.getenv('vda_OCI_key')

    # Set up the URL for query 
    host = "https://OCi-ourcompany.companyA.com" 
    target_url = f'{host}/transfers/OCi/ftg/getArchivedFiles?endpointCodes={end_point}&fromArchivalDate={target_date}&toArchivalDate={target_date}' 

    # Set up and make request 
    kerb_auth = HTTPKerberosAuth(mutual_authentication='OPTIONAL')
    headers = OCiutil.OCi_auth_request(target_url, vda_OCI_key, vda_secret_key) 

    session = requests.Session() 
    response = session.get(target_url, headers=headers, auth=kerb_auth) 

    #store request result as a backup
    if response.status_code == 200: 
        data=response.json()
        with open(f'arc_{end_point}_{target_date}-{datetime.today().strftime("%d%m%Y")}.json', 'w') as f:
            json.dump(data, f, indent=2)
        return data['files']

def check_file(data, citi):
    check_list=set()
    for obj in data:
        send_out_time_utc = datetime.fromtimestamp(obj['archivalTimingUtc']/1000)
        if obj['fileName'] in citi and send_out_time_utc.hour == datetime.now().hour: #double check send out time to avoid catch the order file with the same file name
            check_list.add(obj['fileName'])        
    if check_list != citi:
        msg_alert_to_OCpSupport('{obj["broker"]}files are not sent out, please folllow up with companyA!')
    else:
        post_msg_to_channel('Cxxxxx', f'{[i for i in citi]}\n{obj["broker"]} files sent out from companyA on {send_out_time_utc.astimezone(pytz.timezone("Asia/SingOCore"))}.')
    return 0

if __name__ == '__main__':
    #mapping for put in different varible to check file on different broker endpint
    hour_action_mOCping={
        22: ['OC_VENDORF_SFTP_UPLOAD', {f'FILE_ourcompany_PROD_{get_date_range(1).strftime("%Y%m%m")}.csv'}],
        23: ['OC_VENDORK_SFTP_UPLOAD', \
             {f'ARR_TA_{get_date_range(0).strftime("%m-%d-%y") }.csv',f'TB_ALVO_{get_date_range(0).strftime("%m-%d-%y")}.csv'}],
        11: ['OC_VENDORK_SFTP_UPLOAD', \
             {f'ARR_TA_{get_date_range(0).strftime("%m-%d-%y") }.csv',f'TB_ALVO_{get_date_range(0).strftime("%m-%d-%y")}.csv'}],
    }
    if datetime.now().hour in hour_action_mOCping.keys():
        end_point, citi = hour_action_mOCping[datetime.now().hour]
    try:
        if end_point and citi:
            data = get_file_log(end_point, datetime.today().strftime('%Y-%m-%d') )
            check_file(data, citi)
    except NameError as e:
        print(f"{e} - This program should not run in this hour!")
