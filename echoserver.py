from flask import Flask, request
import json
import requests

app = Flask(__name__)

# This needs to be filled with the Page Access Token that will be provided
# by the Facebook App that will be created.
PAT = 'EAAYwSluZA0n8BAJFDoZCElipIzdZC78x8ugQse8TwUnTY76yZBN6SOPWtLA4ZCiYsaIo4qp7v2NxHwDjq4vGVAOZCYDYS56ZCYK8rpjYVKpqJNp7QudjZBTZAbIAC40u16qlnARa3omdorw9O5aUl2h2DuyvMwZAOYANZCnp22beYcogwZDZD'

@app.route('/', methods=['GET'])
def handle_verification():
  print("Handling Verification.")
  if request.args.get('hub.verify_token', '') == 'secret':
    print("Verification successful!")
    return request.args.get('hub.challenge', '')
  else:
    print("Verification failed!")
    return 'Error, wrong validation token'

@app.route('/', methods=['POST'])
def handle_messages():
  print("Handling Messages")
  payload = request.get_data()
  print(payload)
  for sender, message in messaging_events(payload):
    print("Incoming from %s: %s" % (sender, message))
    url=("https://graph.facebook.com/%i?&access_token=%i",sender_id, PAT)
    #data=requests.get(url)
    #console.log(data)
    #data=urllib.request.urlopen("https://graph.facebook.com/4?fields=name&access_token="+ACCESS_TOKEN).read()
    #data=urllib.request.urlopen("https://graph.facebook.com/"+sender+"?access_token="+ACCESS_TOKEN).read()
    #print(data)
    #name=data.decode('utf-8')
    #jdata=json.loads(name)
    #name=jdata['first_name']
    #reply(sender, jdata['name'])


    send_message(PAT, sender, "Simon")
  return "ok"

def messaging_events(payload):
  """Generate tuples of (sender_id, message_text) from the
  provided payload.
  """
  data = json.loads(payload)
  messaging_events = data["entry"][0]["messaging"]
  for event in messaging_events:
    if "message" in event and "text" in event["message"]:
      yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
    #else:
     #yield event["sender"]["id"], "I can't echo this"


def send_message(token, recipient, text):
  """Send the message text to recipient with id recipient.
  """

  r = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": token},
    data=json.dumps({
      "recipient": {"id": recipient},
      "message": {"text": text.decode('unicode_escape')}
    }),
    headers={'Content-type': 'application/json'})
  if r.status_code != requests.codes.ok:
    print(r.text)

if __name__ == '__main__':
  app.run()