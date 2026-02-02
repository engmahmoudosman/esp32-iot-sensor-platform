#!/usr/bin/env python3
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB Configuration (using the token from docker-compose.yml)
INFLUX_URL = "http://192.168.18.9:8086"  # Use your machine's IP
INFLUX_TOKEN = "my-super-secret-auth-token"  # From docker-compose.yml
INFLUX_ORG = "esp32"
INFLUX_BUCKET = "sensors"

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC_TEMP = "esp32/dht/temperature"
MQTT_TOPIC_HUM = "esp32/dht/humidity"

# Initialize InfluxDB client
influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(MQTT_TOPIC_TEMP)
    client.subscribe(MQTT_TOPIC_HUM)
    print(f"Subscribed to topics")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    
    print(f"Received: {topic} = {payload}")
    
    try:
        value = float(payload)
        
        if "temperature" in topic:
            measurement = "temperature"
        elif "humidity" in topic:
            measurement = "humidity"
        else:
            return
        
        point = Point(measurement) \
            .tag("sensor", "DHT22") \
            .tag("location", "esp32") \
            .field("value", value)
        
        write_api.write(bucket=INFLUX_BUCKET, record=point)
        print(f"✓ Written to InfluxDB: {measurement} = {value}")
        
    except Exception as e:
        print(f"Error: {e}")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

print("Starting MQTT to InfluxDB bridge...")
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_forever()
