
import requests
import os
from flask import Flask, request,jsonify
from slackclient import SlackClient
import ast
import collections
import json
from twilio.rest import Client 
#import nexmo
# import requests.packages.urllib3
# requests.packages.urllib3.disable_warnings()
app = Flask(__name__)
 
def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

@app.route("/",methods=['POST'])
def hello():
    sc = SlackClient('xoxb-338765440979-ausIKKuR2QncQHfzYx2mNs7T')
    print("check")
    d = convert(request.get_json())
    json_string = json.dumps(d)
    print(json_string)
    data=json.loads(json_string)
    keys=data.keys()
    print(keys)
    if keys[0]=='comment':
        post_string=data['comment']['user']['username']+ ' has commented \"'+data['comment']['content']['raw']+ '\" on '+data['comment']['created_on']+' in '+data['repository']['name']+' repository.'
    # elif key[0]=='push':
    #     post_string=data['push']['user']['username']+ ' has commented \"'+data['comment']['content']['raw']+ '\" on '+data['comment']['created_on']
    else :
        #   print(data)
        post_string=data[keys[1]]['username']+' has pushed into '+data[keys[2]]['name']+' and '+data[keys[0]]['changes'][0]['new']['name']+' branch with message '+data[keys[0]]['changes'][0]['new']['target']['message']+' at '+data[keys[0]]['changes'][0]['new']['target']['date']
        # print(data[keys[1]]['username'])
        # print()
        # print()
        # print()
        # print()
        # print(data[keys[0]]['changes'][0]['commits'][0]['date'])
        # print(data[keys[0]]['changes'][0]['commits'][0]['message'])
    sc.api_call(
      "chat.postMessage",
      channel="#general",
      text=post_string
    ) 
    account_sid = "AC665d42ce2ff5f7661ffab421a9c19651"
# Your Auth Token from twilio.com/console
    auth_token  = "7ded7b05377015b90bc539e0f5af10fa"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+918248861568", 
        from_="+19163827100",
        body=post_string)

    print(message.sid)
    # client.messages.create("919688509952","917904035546","hello world")
    # print(data["push"])
    #print(request.get_json())
    return "fff"

@app.route("/message",methods=['POST'])
def channelMessage():
    print(request.form["text"])
    print(request.form["user_id"])
    post_string="Message from "+request.form["user_id"]+" : \""+request.form["text"]+"\""
    account_sid = "AC665d42ce2ff5f7661ffab421a9c19651"
# Your Auth Token from twilio.com/console
    auth_token  = "7ded7b05377015b90bc539e0f5af10fa"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+918438565306", 
        from_="+19163827100",
        body=post_string)

    print(message.sid)
    if request.form["user_id"]<>'USLACKBOT' :
        return "{\"text\":\"Thanks for the message\"}"


@app.route("/boss",methods=['POST'])
def bossMessage():   
    print(request.form["text"])
    print(request.form["user_id"])
    if request.form["user_id"]<>'USLACKBOT':
        return "{\"text\":\"Welcome to Slack integration. You can view the notifications done to your git. All push and commit comment updates are posted here.\"}"    
if __name__ == "__main__":
    app.run()