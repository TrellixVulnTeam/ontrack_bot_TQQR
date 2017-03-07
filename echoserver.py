from flask import Flask, request
import json
import requests
import urllib.request

app = Flask(__name__)

# This needs to be filled with the Page Access Token that will be provided
# by the Facebook App that will be created.
PAT = 'EAAYwSluZA0n8BAMcl44gpxJftYGVodv5uUBvZBeoAt0a8ztqhsrZATEyG6U3b5Fk1xKibZAP6b3JVnNk6M9EdwYz12RzdZBn72l3IKV9VHQbJ0T31sWWZBpvvRoxm7M5G1W1cAos7GDk6EWCAs6Ngcl5q4NZAwjsvfuoc53Qf3sCwZDZD'

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
  #print(payload)
  payload=payload.decode('utf-8')
  #payload=json.loads(payload)
  #print(payload)
  for sender, message in messaging_events(payload):
    print("Incoming from %s: %s" % (sender, message))
    name=get_name(sender)
    send_message(PAT, sender, name)
  return "ok"
def get_name(sender):
  url=("https://graph.facebook.com/%s" %sender)
  data=requests.get(url, params={'access_token': PAT})
  payload=json.loads(data.text)
  return payload['first_name']
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
      "message": {"text": text}
      #"message": {"text": text.decode('unicode_escape')}
    }),
    headers={'Content-type': 'application/json'})
  if r.status_code != requests.codes.ok:
    print(r.text)

if __name__ == '__main__':
  app.run()