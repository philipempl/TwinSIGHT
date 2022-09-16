import paho.mqtt.client as mqtt
import time
import json
from random import seed
import random
seed(1)

# default message
msg_string = '{"thingId": "twin.sight:LENZDRGB610", "temperature": 20, "xcoordinate": 0.08, "ycoordinate": 2.9, "bit_length": 5}'
msg_json = json.loads(msg_string)

# mqtt broker host and port and establish connection
broker = "localhost"
port = 1883
client = mqtt.Client()
client.connect(broker, port)

def publish(client):
     while True:
         time.sleep(random.randint(1, 10))
         msg_json["temperature"] = round(random.uniform(20, 30), 2)
         msg_json["xcoordinate"] = round(random.uniform(0, 1), 4)
         msg_json["ycoordindate"] = round(random.uniform(0, 1), 4)
         msg_json["bit_length"] = round(random.uniform(0, 1), 4)

         topic = msg_json["thingId"]
         result = client.publish(topic, json.dumps(msg_json))
         # result: [0, 1]
         status = result[0]
         if status == 0:
             print(f"Send `{msg_json}` to topic `{topic}`")
         else:
             print(f"Failed to send message to topic {topic}")

publish(client)
client.loop_forever()
