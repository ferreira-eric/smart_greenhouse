# Greenhouse Monitoring System 🌱

Welcome to the **Greenhouse Monitoring System**! This project simulates an intelligent greenhouse system where sensors send real-time data to a central gateway via RabbitMQ. Below, you’ll find an overview of the components and instructions to set up and run the system.

---

## 📦 Project Components

- **`greenhouse.py`**: Simulates greenhouse devices (sensors and actuators). 🔄
- **`smart-gateway`**: Receives and processes messages from sensors.  
  **Note:** To run this, you need to set up another project!
- **`dashboard.py`**: A Streamlit-based web interface for monitoring sensor data and controlling actuators. 📊

> **Important:** The functionality of `smart-gateway` depends on the [Smart Gateway](https://github.com/ferreira-eric/smart-gateway) project. Make sure to clone, install, and run the Smart Gateway project separately to ensure the system works correctly. ⚠️

---

## 🚀 Installation

### 🔧 Prerequisites

Before you begin, ensure that you have the following installed on your system:
- Python 3.x 🐍
- RabbitMQ 🐰
- Required Python libraries (install using the command below):

```sh
pip install -r requirements.txt
```
---

## 🐰 Running RabbitMQ 

Start RabbitMQ before running the system:

```sh
sudo systemctl start rabbitmq-server  # For Linux
rabbitmq-server  # For manual startup
```
---

## 🌡️ Running Sensors

The sensors simulate environmental data (such as temperature, light, and humidity) and send updates to the gateway. Each sensor should be run in a separate terminal:

```sh
python greenhouse.py Temperature 1 20 °C 50051
python greenhouse.py Light 2 60 lux 50052
python greenhouse.py Humidity 3 50 % 50053
```

Each sensor publishes data to its respective RabbitMQ queue, updating its value over time.

---

## 🔌 Running the Gateway

The gateway is responsible for receiving and processing sensor messages.
Important: This functionality is provided by a separate project, the [Smart Gateway](https://github.com/ferreira-eric/smart-gateway). Please refer to that repository for detailed installation and usage instructions. 🔗

---

## 📊 Running the Streamlit Dashboard Client

The Streamlit dashboard provides a web interface for monitoring sensor data and sending actuator commands.

```sh
streamlit run client.py #linux
python -m streamlit run client.py #windowns
```

---

### 🧮 Features:
- Real-time visualization of temperature, humidity, and light sensor data.
- Ability to send control commands to actuators.
- Automatic data refresh every few seconds.

## 🛠️ System Overview

### `greenhouse.py`
- Implements `Sensor` and `Actuator` classes.
- Sensors continuously update their values and publish status to RabbitMQ queues.
- Uses `protobuf` to serialize sensor data.

### `smart-gateway`
- Listens for messages from predefined sensor queues.
- Parses messages using `protobuf`.

### `client.py`
- Fetches sensor data from the gateway.
- Visualizes sensor readings using Matplotlib.
- Allows users to control actuators via an intuitive web interface.
  
---

## 📐 Architeture

![Distribuidos arquitetura-C8 Architecture (3)](https://github.com/user-attachments/assets/37df8cfb-dbdb-4786-8a93-4cbf3fd4d0d9)

