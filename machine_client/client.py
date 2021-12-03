import paho.mqtt.client as mqtt
import time
import json
from random import seed
from random import random
seed(1)

# default message
msg_string = '{"temperature": 20, "xcoordinate": 0.08, "ycoordindate": 2.9", "machine": "LENZDRGB611", "type": "drill_mill_machine", "units":  {"temp": "° C"}}'
msg_json = json.loads(msg_string)

# mqtt broker host and port and establish connection
broker = "localhost"
port = 1883
client = mqtt.Client()
client.connect(broker, port, 60)

def publish(client):
     while True:
         time.sleep(random.randint(1, 10))
         msg_json["temp"] = round(random.uniform(20, 30), 2)
         msg_json["xcoordinate"] = random()
         msg_json["ycoordindate"] = random()
         result = client.publish(msg_json["location"], json.dumps(msg_json))
         # result: [0, 1]
         status = result[0]
         if status == 0:
             print(f"Send `{msg_json}` to topic `{topic}`")
         else:
             print(f"Failed to send message to topic {topic}")

publish(client)
client.loop_forever()
