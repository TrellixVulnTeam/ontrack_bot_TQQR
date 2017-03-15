from flask import Flask, request
from fuzzywuzzy import process
import json
import requests
import urllib
from . import config


app = Flask(__name__)
  

try:
  PAT=os.environ['PAT']
  token=os.environ['token']
  print("Success")
except:
  PAT=config.PAT
  token=config.token

@app.route('/', methods=['GET'])
def handle_verification():
  print("Handling Verification.")
  if request.args.get('hub.verify_token', '') == token:
    print("Verification successful!")
    return request.args.get('hub.challenge', '')
  else:
    print("Verification failed!")
    return 'Error, wrong validation token'

@app.route('/', methods=['POST'])

def handle_messages():
  print("Handling Messages")
  payload = request.get_data()
  payload=payload.decode('utf-8')

  for sender, message in messaging_events(payload):
    print("Incoming from %s: %s" % (sender, message))
    message=message.decode("utf-8") 
    #name=get_name(sender)
    #response=("Hey there %s!" %name)
    find_message(PAT, sender, message)
  return "ok"
def find_message(PAT, sender, message):
  lists=[]
  lists.append({'greeting':['Hey', 'Hi', 'Hello', 'Hey there', "What's up?", 'watsup', 'Hiya', 'Aloha']})
  lists.append({'farewell':['Bye', 'Seeya', 'See you later', 'Peace out', 'Goodbye']})
  lists.append({'confirmation':['Yes', 'Yea', 'Please', 'Sure', 'Definitely', 'Of course', 'Mhmmm', 'Yes please']})
  lists.append({'denial':['No', 'Nope', 'Maybe later', 'Maybe', 'No thanks']})
  total=[]
  for dicts in lists:
    total+=(list(dicts.values())[0])

  answer=process.extract(message, total)
  for dicts in lists:
    for title, words in dicts.items():  
      if(answer[0][0] in words):
        command=("%s(PAT, sender)" %title)
        eval(command)

def greeting(PAT, sender):
  send_message(PAT, sender, "Hey %s, my name is Artemis, it's nice to meet you!" %get_name(sender))
  send_message(PAT, sender, "Did you want to set up some tasks today?")
def prompt():
  return ("Did you want to set up some tasks today?")
def farewell(PAT, sender):
  send_message(PAT, sender, "Bye %s!" %get_name(sender))
def confirmation(PAT, sender):
  send_message(PAT, sender, "Awesome! Sadly, since I am currently in development, that feature is not fully functional and has yet to be released.")
def denial(PAT, sender):
  send_message(PAT, sender, "Okay, maybe later!")


  

def get_name(sender):
  url=("https://graph.facebook.com/%s" %sender)
  data=requests.get(url, params={'access_token': PAT})
  payload=json.loads(data.text)
  return payload['first_name']

def messaging_events(payload):
  data = json.loads(payload)
  messaging_events = data["entry"][0]["messaging"]
  for event in messaging_events:
    if "message" in event and "text" in event["message"]:
      yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')

def send_message(token, recipient, text):
  r = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": token},
    data=json.dumps({
      "recipient": {"id": recipient},
      "message": {"text": text}
    }),
    headers={'Content-type': 'application/json'})
  if r.status_code != requests.codes.ok:
    print(r.text)

if __name__ == '__main__':
  app.run()