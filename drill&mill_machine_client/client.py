import paho.mqtt.client as mqtt
import time
import random
import json

broker = "localhost"
port = 1883
topic =  "LENZDRGB611"
msg_string = '{"temp": 20, "location": "LENZDRGB611", "type": "temperature", "units":  {"temp": "° C"}}'
msg_json = json.loads(msg_string)

client = mqtt.Client()
client.connect(broker, port, 60)

def publish(client):
     while True:
         time.sleep(random.randint(1, 10))
         msg_json["temp"] = round(random.uniform(20, 30), 2)
         result = client.publish(topic, json.dumps(msg_json))
         # result: [0, 1]
         status = result[0]
         if status == 0:
             print(f"Send `{msg_json}` to topic `{topic}`")
         else:
             print(f"Failed to send message to topic {topic}")
         
publish(client)
client.loop_forever()