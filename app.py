from flask import Flask, request
from pymessenger import Bot
from utils import *
import requests,json

app = Flask("My news bot")

FB_ACCESS_TOKEN = "EAAfkm1agk7YBAOttZC0ANtIcgHZAu2pATVbJfb4TUpUwxgtFl9x4NPqZCVqGJN98Iewj9mCQtICl6GKZBGG4hxvBPzsCGOpC0Ym4ZCC4T6rcnFUC23zfVXXmgZCT8SqXoqJZCwXp5K40TyNktmSI2pzVAmO2q2PVyZAy0n4tAGZBekz0le2zOJRvf"
bot = Bot(FB_ACCESS_TOKEN)

VERIFICATION_TOKEN = "hello"


@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    print(request.data)
    data = request.get_json()
    
    if data['object'] == "page":
        entries = data['entry']
        for entry in entries:
            if 'messaging' in entry:
                print("--------here----")
                messaging = entry['messaging']
                for messaging_event in messaging:
                    
                    sender_id = messaging_event['sender']['id']
                    recipient_id = messaging_event['recipient']['id']
                    if messaging_event.get('postback'):
                        if messaging_event['postback'].get('payload'):
                        # HANDLE PAYLOAD HERE
                            payload=messaging_event['postback']['payload']
                            elements=pay_load_adapter(payload)
                            bot.send_text_message(sender_id, "可以让我知道你的就餐位置吗？")
                            
                            bot.send_generic_message(sender_id,elements)
                
                    
                    if messaging_event.get('message'):
                    
                    
                        # HANDLE NORMAL MESSAGES HERE
                        
                        if messaging_event['message'].get('text'):
                            # HANDLE TEXT MESSAGES
                            
                            query = messaging_event['message']['text']
                            
                            reply = fetch_reply(query, sender_id)
                            #bot.send_text_message(sender_id, reply)
                            elements = get_welcome_elements()
                            bot.send_generic_message(sender_id, elements)
                            '''buttons = [{"type":"web_url",
                                       "url": "https://youtube.com/IndianPythonista",
                                       "title":"My channel"}]
                            bot.send_button_message(sender_id, "Check out this link!", buttons)'''

#else:
#               print("--------here else----")
#                sender_id = entry['standby'][0]['sender']['id']
#                reply=entry['standby'][0]['postback']['title']
                            #ANDLE TEXT MESSAGESbot.send_text_message(sender_id, reply)

    return "ok", 200

def set_greeting_text():
    headers = {
        'Content-Type':'application/json'
        }
    data = {
        "setting_type":"greeting",
        "greeting":{
            "text":"Hi {{user_first_name}}! I am your food assistant."
            }
        }
    ENDPOINT = "https://graph.facebook.com/v2.8/me/thread_settings?access_token=%s"%(FB_ACCESS_TOKEN)
    r = requests.post(ENDPOINT, headers = headers, data = json.dumps(data))
    print(r.content)

def set_persistent_menu():
    headers = {
        'Content-Type':'application/json'
        }
    data = {
        "setting_type":"call_to_actions",
            "thread_state" : "existing_thread",
            "call_to_actions":[
                               {
                               "type":"web_url",
                               "title":"Meet the developer",
                               "url":"https://fb.me/nikhilksingh97"
                               },
                               {
                               "type":"postback",
                               "title":"Help",
                               "payload":"SHOW_HELP"
                               }]
        }
    ENDPOINT = "https://graph.facebook.com/v2.8/me/thread_settings?access_token=%s"%(FB_ACCESS_TOKEN)
    r = requests.post(ENDPOINT, headers = headers, data = json.dumps(data))
    print(r.content)

def log(message):
    print(message)
    sys.stdout.flush()



if __name__ == "__main__":
    app.run(port=8000, use_reloader = True)
