# ESP32 IoT Sensor Platform

A complete IoT solution for real-time environmental monitoring using ESP32 microcontroller with MQTT messaging, time-series data storage, and live dashboard visualization.

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![ESP-IDF](https://img.shields.io/badge/ESP--IDF-v5.5.2-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Hardware Requirements](#hardware-requirements)
- [Software Stack](#software-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Usage](#usage)
- [Dashboard](#dashboard)
- [Future Enhancements](#future-enhancements)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project implements a complete IoT sensor monitoring system that collects environmental data (temperature and humidity) from DHT22 sensors connected to ESP32 microcontrollers, transmits the data via MQTT protocol, stores it in a time-series database, and visualizes it in real-time through Grafana dashboards.

**Key Highlights:**
- Real-time sensor data collection
- MQTT-based message broker architecture
- Docker-containerized infrastructure
- Time-series data storage with InfluxDB
- Live monitoring dashboards with Grafana
- Persistent data storage across restarts

##  Features

### Hardware Layer
-  ESP32-based sensor nodes
-  DHT22 temperature and humidity sensor integration
-  WiFi connectivity
-  MQTT client implementation
-  Configurable sampling intervals

### Communication Layer
-  MQTT protocol (QoS 0)
-  Eclipse Mosquitto broker
-  Topic-based message routing
-  Automatic reconnection handling

### Data Processing
-  Python-based MQTT subscriber
-  Real-time data validation
-  Multi-database architecture (InfluxDB for time-series)
-  Error handling and logging

### Visualization
-  Grafana dashboards
-  Real-time data plotting
-  Historical data analysis
-  Customizable time ranges

### Infrastructure
-  Docker containerization
-  Docker Compose orchestration
-  Persistent data volumes
-  Easy deployment and scaling

##  System Architecture

```
┌─────────────────┐
│   ESP32 + DHT22 │
│   Sensor Node   │
└────────┬────────┘
         │ WiFi
         │ MQTT Publish
         ▼
┌─────────────────┐
│    Mosquitto    │
│   MQTT Broker   │
│   Port: 1883    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ MQTT Processor  │
│  (Python Script)│
│  - Validation   │
│  - Routing      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    InfluxDB     │
│  Time-Series DB │
│   Port: 8086    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Grafana     │
│   Dashboards    │
│   Port: 3000    │
└─────────────────┘
```

### Data Flow

1. **ESP32** reads sensor data from DHT22 every 5 seconds
2. **WiFi** connection established to local network
3. **MQTT Client** publishes data to topics:
   - `esp32/dht/temperature`
   - `esp32/dht/humidity`
4. **Mosquitto Broker** receives and routes messages
5. **Python Processor** subscribes to topics and validates data
6. **InfluxDB** stores time-series sensor readings
7. **Grafana** queries and visualizes data in real-time

##  Hardware Requirements

### ESP32 Development Board
- **Microcontroller**: ESP32-WROOM-32
- **Cores**: Dual-core Xtensa LX6
- **Clock Speed**: 240 MHz
- **Flash**: 4MB
- **RAM**: 520KB SRAM
- **WiFi**: 802.11 b/g/n
- **Operating Voltage**: 3.3V

### DHT22 Sensor
- **Type**: Digital temperature and humidity sensor
- **Temperature Range**: -40°C to 80°C (±0.5°C accuracy)
- **Humidity Range**: 0-100% RH (±2-5% accuracy)
- **Interface**: Single-wire digital
- **Operating Voltage**: 3.3V - 5V
- **Sampling Rate**: 0.5 Hz (once every 2 seconds)

### Wiring Diagram

```
DHT22          ESP32
─────          ─────
VCC   ────────  3.3V
DATA  ────────  GPIO 27 (configurable)
GND   ────────  GND

Note: 4.7kΩ - 10kΩ pull-up resistor between DATA and VCC
```

### Additional Components
- USB cable for programming
- Breadboard and jumper wires
- 4.7kΩ resistor (pull-up for DHT22 data line)

##  Software Stack

### Firmware Development
- **Framework**: ESP-IDF v5.5.2
- **Language**: C
- **RTOS**: FreeRTOS
- **Build System**: CMake
- **Development Environment**: VSCode with ESP-IDF extension

### Backend Services
- **MQTT Broker**: Eclipse Mosquitto 2.0
- **Database**: InfluxDB 2.7 (time-series)
- **Processing**: Python 3.11
- **Libraries**: 
  - `paho-mqtt` (MQTT client)
  - `influxdb-client` (InfluxDB Python client)

### Visualization
- **Dashboard**: Grafana (latest)
- **Query Language**: Flux

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **OS**: Linux (Debian-based)

## Project Structure

```
esp32_mqtt_dht22/
│
├── main/
│   ├── main.c                 # Main application logic
│   └── CMakeLists.txt         # Component build config
│
├── components/
│   └── DHT22/
│       ├── include/
│       │   └── DHT22.h        # DHT22 library header
│       ├── DHT22.c            # DHT22 implementation
│       └── CMakeLists.txt     # Component build config
│
├── dashboard/
│   ├── docker-compose.yml     # Container orchestration
│   ├── mqtt_influx_bridge.py  # MQTT to InfluxDB processor
│   └── venv/                  # Python virtual environment
│
├── build/                     # ESP-IDF build output (gitignored)
├── CMakeLists.txt             # Project build configuration
├── sdkconfig                  # ESP-IDF configuration (gitignored)
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## Getting Started

### Prerequisites

#### For ESP32 Development
```bash
# Install ESP-IDF v5.5.2
# Follow: https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/

# Verify installation
idf.py --version
```

#### For Dashboard Setup
```bash
# Install Docker
sudo apt update
sudo apt install docker.io docker-compose -y

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker compose version
```

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/esp32_mqtt_dht22.git
cd esp32_mqtt_dht22
```

#### 2. Configure ESP32 Firmware

Edit `main/main.c` and update:

```c
#define EXAMPLE_ESP_WIFI_SSID "YOUR_WIFI_SSID"
#define EXAMPLE_ESP_WIFI_PASS "YOUR_WIFI_PASSWORD"

// In mqtt_app_start() function:
.broker.address.uri = "mqtt://YOUR_MQTT_BROKER_IP:1883"
```

Update GPIO pin if needed:
```c
// In DHT_Publisher_task() function:
setDHTgpio(GPIO_NUM_27);  // Change to your connected GPIO
```

#### 3. Build and Flash ESP32

```bash
# Configure project (optional - for advanced settings)
idf.py menuconfig

# Build firmware
idf.py build

# Flash to ESP32 (replace /dev/ttyUSB0 with your port)
idf.py -p /dev/ttyUSB0 flash

# Monitor serial output
idf.py -p /dev/ttyUSB0 monitor
```

#### 4. Setup Dashboard Infrastructure

```bash
cd dashboard

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install paho-mqtt influxdb-client

# Start Docker services
docker compose up -d

# Check services status
docker compose ps
```

#### 5. Configure MQTT Bridge

Edit `dashboard/mqtt_influx_bridge.py`:

```python
# Update with your machine's IP address
INFLUX_URL = "http://YOUR_MACHINE_IP:8086"
INFLUX_TOKEN = "my-super-secret-auth-token"  # From docker-compose.yml
```

#### 6. Run MQTT Bridge

```bash
cd dashboard
source venv/bin/activate
python mqtt_influx_bridge.py
```

You should see:
```
Connected to MQTT broker with result code 0
Subscribed to topics
Received: esp32/dht/temperature = 25.30
✓ Written to InfluxDB: temperature = 25.30
```

##  Configuration

### ESP32 Configuration

| Parameter | Location | Description |
|-----------|----------|-------------|
| WiFi SSID | `main/main.c` | Your WiFi network name |
| WiFi Password | `main/main.c` | Your WiFi password |
| MQTT Broker IP | `main/main.c` | IP address of MQTT broker |
| DHT22 GPIO | `main/main.c` | GPIO pin for DHT22 data |
| Sampling Interval | `main/main.c` | Data reading interval (default: 5s) |

### MQTT Topics

| Topic | Data Type | Description |
|-------|-----------|-------------|
| `esp32/dht/temperature` | Float | Temperature in Celsius |
| `esp32/dht/humidity` | Float | Relative humidity percentage |

### InfluxDB Configuration

Access InfluxDB UI: `http://localhost:8086`

- **Organization**: esp32
- **Bucket**: sensors
- **Token**: my-super-secret-auth-token (change in production)

### Grafana Configuration

Access Grafana: `http://localhost:3000`

- **Username**: admin
- **Password**: admin (change on first login)

## Dashboard

### Accessing Grafana

1. Open browser: `http://localhost:3000`
2. Login with admin/admin
3. Add InfluxDB data source:
   - URL: `http://influxdb:8086`
   - Organization: `esp32`
   - Token: `my-super-secret-auth-token`
   - Bucket: `sensors`

### Creating Visualizations

**Temperature Panel:**
```flux
from(bucket: "sensors")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "temperature")
  |> filter(fn: (r) => r._field == "value")
```

**Humidity Panel:**
```flux
from(bucket: "sensors")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "humidity")
  |> filter(fn: (r) => r._field == "value")
```

### Sample Dashboard
- Real-time line charts for temperature and humidity
- Stat panels showing current values
- Time-range selector (15m, 1h, 6h, 24h, 7d)
- Auto-refresh every 5 seconds

## Future Enhancements

### Short Term
- [ ] Add more sensor types (BMP280 for pressure, MQ-135 for air quality)
- [ ] Implement OTA (Over-The-Air) firmware updates
- [ ] Add TLS/SSL for MQTT communication
- [ ] Create alert rules for threshold violations
- [ ] Add data export functionality

### Medium Term
- [ ] Multiple ESP32 nodes support
- [ ] REST API for data access
- [ ] React-based custom dashboard
- [ ] Mobile app for monitoring
- [ ] Historical data analytics

### Long Term
- [ ] Machine learning for anomaly detection
- [ ] Predictive maintenance
- [ ] Energy optimization algorithms
- [ ] Multi-tenant support
- [ ] Cloud deployment (AWS/GCP/Azure)

##  Troubleshooting

### ESP32 Issues

**Problem**: DHT22 sensor timeout
```
E (564) DHT: Sensor Timeout
```
**Solution**: 
- Check wiring connections
- Verify GPIO pin number in code
- Ensure 4.7kΩ pull-up resistor is present
- Try different GPIO pin

**Problem**: WiFi connection failed
```
E (xxxx) wifi: disconnected: Retrying Wi-Fi
```
**Solution**:
- Verify SSID and password are correct
- Check WiFi signal strength
- Ensure 2.4GHz network (ESP32 doesn't support 5GHz)

**Problem**: MQTT connection timeout
```
E (xxxx) esp-tls: select() timeout
```
**Solution**:
- Verify MQTT broker IP address is correct
- Ensure ESP32 and broker are on same network
- Check firewall rules allow port 1883

### Dashboard Issues

**Problem**: Docker services won't start
```bash
# Check logs
docker compose logs
```
**Solution**:
- Ensure ports 1883, 3000, 8086 are not in use
- Check Docker daemon is running
- Verify docker-compose.yml syntax

**Problem**: MQTT bridge not receiving messages
**Solution**:
- Verify MQTT broker is running: `docker compose ps`
- Check ESP32 is publishing: `idf.py monitor`
- Test with mosquitto_sub: `mosquitto_sub -h localhost -t "esp32/dht/#" -v`


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Mahmoud Esameldin Osman- engmahmoudosman@outlook.com

Project Link: [https://github.com/YOUR_USERNAME/esp32_mqtt_dht22](https://github.com/YOUR_USERNAME/esp32_mqtt_dht22)

## References 

- [ESP-IDF](https://docs.espressif.com/projects/esp-idf/) - Espressif IoT Development Framework
- [Eclipse Mosquitto](https://mosquitto.org/) - Open source MQTT broker
- [InfluxDB](https://www.influxdata.com/) - Time series database
- [Grafana](https://grafana.com/) - Analytics and monitoring platform
- DHT22 sensor library contributors

---
