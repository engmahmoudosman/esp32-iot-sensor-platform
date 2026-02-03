# System Architecture Documentation

## Overview

This document describes the technical architecture of the ESP32 IoT Sensor Platform.

## System Components

### 1. Edge Layer (ESP32)

**Hardware:**
- MCU: ESP32-WROOM-32 (Dual-core Xtensa LX7 @ 240MHz)
- Sensor: DHT22 (Temperature & Humidity)
- Connectivity: WiFi 802.11 b/g/n

**Software:**
- Framework: ESP-IDF v5.5.2
- RTOS: FreeRTOS
- MQTT Client: ESP-MQTT component


**Responsibilities:**
- Sensor data acquisition
- WiFi connection management
- MQTT client operation
- Error handling and recovery

### 2. Message Broker (Mosquitto)

**Technology:** Eclipse Mosquitto 2.0

**Configuration:**
- Port: 1883 (MQTT)
- Protocol: MQTT v3.1.1
- QoS: 0 (Fire and forget)
- Authentication: None (for local development)

**Topics Structure:**
```
esp32/
  └── dht/
      ├── temperature
      └── humidity
```

### 3. Data Processor (Python Bridge)

**Technology:** Python 3.11 with paho-mqtt

**Functions:**
- Subscribe to MQTT topics
- Validate incoming data
- Transform data format
- Write to InfluxDB

**Data Validation:**
- Temperature range: -50°C to 100°C
- Humidity range: 0% to 100%
- Data type validation (numeric)

### 4. Storage Layer

**Database:** InfluxDB 2.7

**Schema:**
```
Measurement: temperature
- Tags: sensor=DHT22, device_id=esp32, location=unknown
- Field: value (float)
- Timestamp: auto-generated

Measurement: humidity
- Tags: sensor=DHT22, device_id=esp32, location=unknown
- Field: value (float)
- Timestamp: auto-generated
```

**Retention Policy:**
- Default: Infinite
- Recommended: 90 days for production

### 5. Visualization Layer

**Technology:** Grafana (latest)

**Data Source:** InfluxDB (Flux query language)

**Dashboards:**
- Real-time sensor values
- Historical trends
- Statistical analysis (min, max, avg)

## Data Flow

1. **Sensor Reading** (ESP32)
   ```
   DHT22 → ESP32 → Validation → Format
   ```

2. **Data Transmission** (MQTT)
   ```
   ESP32 → WiFi → MQTT Broker → Python Subscriber
   ```

3. **Data Storage** (InfluxDB)
   ```
   Python Bridge → Validation → InfluxDB Write API → Database
   ```

4. **Data Visualization** (Grafana)
   ```
   Grafana → Flux Query → InfluxDB → Render Charts
   ```

## Network Architecture

```
┌─────────────────────────────────────────┐
│         Local Network (192.168.x.x)     │
│                                          │
│  ┌──────────┐         ┌──────────────┐ │
│  │  ESP32   │────────▶│  Linux Host  │ │
│  │192.168.x │  WiFi   │  192.168.x.9 │ │
│  └──────────┘         └──────┬───────┘ │
│                              │          │
│                       Docker Bridge     │
│                       (172.17.0.0/16)  │
│                              │          │
│              ┌───────────────┼───────┐ │
│              │               │       │ │
│         ┌────▼────┐    ┌────▼────┐  │ │
│         │Mosquitto│    │InfluxDB │  │ │
│         │Container│    │Container│  │ │
│         └────┬────┘    └────▲────┘  │ │
│              │              │       │ │
│         ┌────▼──────────────┴────┐  │ │
│         │  Python Bridge (Host) │  │ │
│         └────┬──────────────────┘  │ │
│              │                     │ │
│         ┌────▼────┐                │ │
│         │ Grafana │                │ │
│         │Container│                │ │
│         └─────────┘                │ │
│                                    │ │
└────────────────────────────────────┘ │
```

## Security Considerations

**Current Implementation (Development):**
- No authentication on MQTT
- No encryption (plain MQTT)
- HTTP for Grafana/InfluxDB

**Production Recommendations:**
- Enable MQTT authentication (username/password)
- Use MQTT over TLS (port 8883)
- Enable InfluxDB authentication
- Use HTTPS for web interfaces
- Implement device certificates
- Network segmentation (IoT VLAN)

## Performance Metrics

**Throughput:**
- MQTT messages: 1 message every 5 seconds per device
- Peak: ~12 messages/minute per device
- Scalability: Supports 50+ devices on current setup

**Latency:**
- Sensor to MQTT: <100ms
- MQTT to InfluxDB: <50ms
- Total end-to-end: <200ms
- Dashboard refresh: 5 seconds

**Resource Usage:**
- InfluxDB: ~200MB RAM, 1GB storage/month/device
- Mosquitto: ~50MB RAM
- Grafana: ~200MB RAM
- Python Bridge: ~50MB RAM

## Scalability

**Horizontal Scaling:**
- Multiple ESP32 devices: Just add more (unique device IDs)
- MQTT clustering: For high-availability
- InfluxDB clustering: For larger deployments

**Vertical Scaling:**
- Increase sampling rate
- Add more sensor types
- Implement data aggregation
- Use database sharding

## Deployment Models

### Development (Current)
- Single Linux machine
- Docker containers for services
- Local network access only

### Production
- VPS or cloud instance
- Reverse proxy (Nginx)
- SSL/TLS certificates
- Domain name
- Firewall rules
- Backup automation

### Enterprise
- Kubernetes cluster
- Load balancers
- Database replication
- Monitoring (Prometheus)
- Alerting (AlertManager)
- Service mesh

## Technology Choices Rationale

| Technology | Chosen | Rationale |
|------------|--------|-----------|
| MCU | ESP32 | WiFi built-in, powerful, cheap, good community |
| Framework | ESP-IDF | Official, robust, full control |
| Protocol | MQTT | Lightweight, pub/sub, IoT standard |
| Broker | Mosquitto | Open-source, stable, widely used |
| Database | InfluxDB | Purpose-built for time-series, fast queries |
| Visualization | Grafana | Powerful, flexible, industry standard |
| Containerization | Docker | Portable, easy deployment, isolation |

## Future Architecture Enhancements

1. **Add PostgreSQL** for device metadata and user management
2. **Add Redis** for caching and real-time updates
3. **Implement REST API** for programmatic access
4. **Add Nginx** as reverse proxy
5. **WebSocket** for real-time dashboard updates
6. **Message Queue** (RabbitMQ/Kafka) for buffering
7. **Authentication Service** (OAuth2/JWT)
8. **Alerting System** (email, SMS, webhooks)
