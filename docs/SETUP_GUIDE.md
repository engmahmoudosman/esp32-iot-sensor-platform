
# Setup Guide

## Quick Start

### 1. Hardware Setup

1. Connect DHT22 to ESP32:
   - VCC → 3.3V
   - DATA → GPIO 27
   - GND → GND
   - Add 4.7kΩ pull-up resistor between DATA and VCC

2. Connect ESP32 to computer via USB

### 2. Firmware Setup

```bash
# Configure WiFi and MQTT broker
nano main/main.c

# Update these lines:
#define EXAMPLE_ESP_WIFI_SSID "YOUR_SSID"
#define EXAMPLE_ESP_WIFI_PASS "YOUR_PASSWORD"

# In mqtt_app_start():
.broker.address.uri = "mqtt://192.168.x.x:1883"

# In DHT_Publisher_task():
setDHTgpio(GPIO_NUM_27);  # Change if using different GPIO
# Build and flash
idf.py build
idf.py -p /dev/ttyUSB0 flash monitor
```

### 3. Dashboard Setup

```
cd dashboard

# Install Docker (if not installed)
# See main README for Docker installation

# Start services
docker compose up -d

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate
pip install paho-mqtt influxdb-client

# Configure bridge
nano mqtt_influx_bridge.py
 Update INFLUX_URL with your machine's IP

# Run bridge
python mqtt_influx_bridge.py
```

### 4. Access Dashboard

- Grafana: http://localhost:3000 (admin/admin)
- InfluxDB: http://localhost:8086
- MQTT Broker: localhost:1883

### 5. Create Grafana Dashboard
1. Login to Grafana
2. Add InfluxDB data source
3. Create new dashboard
4. Add panels with Flux queries (see README)

### Troubleshooting
See main README.md for common issues and solutions.


