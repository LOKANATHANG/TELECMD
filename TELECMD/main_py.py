
import json, requests, time
from boltiot import Bolt
import conf

URL = "https://api.telegram.org/" + conf.telegram_bot_id

mybolt = Bolt(conf.api_key, conf.device_id)

light_pin = "1"
fan_pin = "2"
tv_pin = "3"
last_message_id = None
last_text = None

def check_device_status():
    try:
        response = mybolt.isOnline()
        response = json.loads(response)
        if response["value"] == "online":
            print("Device is Online")
            return True
        else:
            print("Device is offline")
            send_telegram_message("Device is offline")
            return False
    except Exception as e:
        print("An error occurred in Checking device status.")
        print(e)
        return False 

def send_telegram_message(message):
    """Sends message via Telegram"""
    print("Sending telegram message .....")
    url = URL + "/sendMessage?text=" + message + "&chat_id=" + conf.telegram_chat_id
    try: 
        response = requests.get(url)
        content = response.content.decode("utf8")
        js = json.loads(content)
        if js["ok"] == True:
            print("Messgae sent successfully.")
            return True
        else:
            print("Message on sent. Response: " + str(js["ok"]))
            print(js)
            return False
    except Exception as e:
        print("An error occurred in sending message via Telegram")
        print(e)
        return False
    
def get_last_message():
    """Gets last message from Telegram"""
    print("Getting last message .....")
    url = URL + "/getUpdates"
    try:
        response = requests.get(url)
        content = response.content.decode("utf8")
        js = json.loads(content)
        num_updates = len(js["result"])
        last_update = num_updates - 1
        message_id = js["result"][last_update]["channel_post"]["message_id"]
        text = js["result"][last_update]["channel_post"]["text"]
        print("This is the last message : " + text)
        return (text, message_id)
    except Exception as e:
        print("An error occurred in getting message from Telegram")
        print(e)
        
while True:
    # Step 1 : Check Device Status
    print("Checking device Status .....")
    response = check_device_status()
    if response != True:
        time.sleep(10)
        continue
    # Step 2 : Sending Welcome message with options.
    message = "Welcome to Telecmd Your all time companion\n" + "-" * 55 + "\nSelect Option -\n1. Light on\n2. Light off\n3. Fan on\n4. Fan off\n5. TV on\n6. TV off"
    response = send_telegram_message(message)
    if response != True:
        continue
    time.sleep(10)
    # Step 3 : Getting last message from telegram
    text, message_id = get_last_message()
    # Step 4 : Checking with previous message & message_id
    if (text !=last_text) or (message_id != last_message_id):
        if (text == "1") or (text == "Light on") or (text == "light on"):
            mybolt.digitalWrite(light_pin,"HIGH")
            message = "Light turned on"
            print(message)
            send_telegram_message(message)
        elif (text == "2") or (text == "Light off") or (text == "Light off"):
            mybolt.digitalWrite(light_pin,"LOW")
            message = "Light turned off"
            print(message)
            send_telegram_message(message)
        elif (text == "3") or (text == "Fan on") or (text == "fan on"):
            mybolt.digitalWrite(fan_pin,"HIGH")
            message = "Fan turned on"
            print(message)
            send_telegram_message(message)
        elif (text == "4") or (text == "Fan off") or (text == "fan off"):
            mybolt.digitalWrite(fan_pin,"LOW")
            message = "Fan turned off"
            print(message)
            send_telegram_message(message)
        elif (text == "5") or (text == "TV on") or (text == "tv on"):
            mybolt.digitalWrite(tv_pin,"HIGH")
            message = "TV turned on"
            print(message)
            send_telegram_message(message)
        elif (text == "6") or (text == "TV off") or (text == "tv off"):
            mybolt.digitalWrite(tv_pin,"LOW")
            message = "TV turned off"
            print(message)
            send_telegram_message(message)
        last_text = text
        last_message_id = message_id
    # Step 5 : Wait for 10 second
    time.sleep(10)