import requests
import json
import datetime
import subprocess
channelList = "https://slack.com/api/channels.list"
channelHistory = "https://slack.com/api/channels.history"
token = "YOUR_TOKEN"

def getChannelID():
    payload = {
        "token": token
    }
    response = requests.get(channelList, params=payload)
    json_data = response.json()
    channels = json_data["channels"]
    channels_list=[]
    for channel in channels:
        channels_list.append(channel['id'])
    return channels_list

datelist=[]
def makedatelist():
    channels_list=getChannelID()
    for channel_id in channels_list:
        payload = {
            "token": token,
            "channel": channel_id
        }
        response = requests.get(channelHistory, params=payload)
        json_data = response.json()
        messages = json_data["messages"]
        for message in messages:
            dt = datetime.datetime.fromtimestamp(float(message['ts']))
            month = str(dt.month)
            day=str(dt.day)
            if len(month) == 1:
                month = '0' + month
            if len(day) == 1:
                day = '0' + day
            YMD = str(dt.year) + month + day

            D = [d['date'] == YMD for d in datelist]
            if True in D:
                num = int(datelist[D.index(True)]['quantity'])
                num += 1
                datelist[D.index(True)]['quantity'] = str(num)
            else:
                num=str(1)
                datelist.append({"date": YMD, "quantity": num})
    return datelist
                
def main():
    datelists = makedatelist()
    for date in datelists:
        date = json.dumps(date)
        cmd = "curl -X POST YOUR_PIXELA_GRAPH_URL -H 'X-USER-TOKEN:xxxxxxxxxx' -d "
        cmd = cmd + "'" + date + "'"
        print(cmd)
    

if __name__ == '__main__':
    main()