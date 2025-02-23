import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import matplotlib.pyplot as plt
import numpy as np
import time

# Configura o autorefresh a cada 3000 ms (3 segundos)
st_autorefresh(interval=3000, limit=1000, key="autorefresh")

# URL do Gateway para obter dados dos sensores e enviar comandos para atuadores
GATEWAY_URL = "http://localhost:8080"

@st.cache_data(ttl=2)
def get_sensor_data():
    """
    Busca os dados dos sensores na API do gateway e os organiza em um dicionário.
    Retorna:
        dict: Um dicionário com os dados dos sensores, agrupados por tipo.
              Se o sensor nunca foi ligado, a lista estará vazia.
    """
    try:
        response = requests.get(f"{GATEWAY_URL}/api/sensors")
        sensors = response.json()  # resposta é uma lista de objetos SensorDTO
        sensor_data = {
            'temperature_sensor': [],
            'light_sensor': [],
            'humidity_sensor': []
        }
        for sensor in sensors:
            name = sensor.get("name", "").lower()
            if "temperature" in name:
                sensor_data['temperature_sensor'].append(sensor)
            elif "light" in name:
                sensor_data['light_sensor'].append(sensor)
            elif "humidity" in name:
                sensor_data['humidity_sensor'].append(sensor)
        return sensor_data
    except requests.exceptions.RequestException as e:
        st.error("Erro ao conectar com o gateway.")
        print(f"Erro ao conectar com o gateway: {e}")
        return {}

def plot_sensor_history(history, sensor_name, unit=""):
    """
    Plota o histórico dos valores do sensor usando Matplotlib.
    Parâmetros:
        history (list): Lista de valores históricos (float) do sensor.
        sensor_name (str): Nome do sensor (ex.: "Temperatura").
        unit (str): Unidade de medida para exibição.
    """
    if not history:
        st.warning(f"{sensor_name} indisponível.")
        return

    times = np.arange(len(history))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(times, history, marker='o', linestyle='-', color='b')
    ax.set_ylabel(f"{sensor_name} ({unit})", fontsize=15)
    ax.grid(True, axis='y')
    ax.set_xlim(0, max(20, len(history)-1))
    ax.set_xticks([])
    ax.tick_params(axis='y', labelsize=12)
    st.pyplot(fig)

def send_actuator_command(actuator_name, value):
    """
    Envia um comando para um atuador via API do gateway.
    Parâmetros:
        actuator_name (str): Nome do atuador (ex.: "actuator_temperature").
        value (float): Valor a ser enviado para o atuador.
    """
    try:
        response = requests.post(f"{GATEWAY_URL}/api/actuators/{actuator_name}/{value}")
        if response.status_code == 200:
            st.success(f"Comando enviado para {actuator_name} com valor {value}")
        else:
            error_detail = response.json().get("detail", "Dispositivo Indisponivel")
            st.error(f"Falha ao enviar comando para {actuator_name}. Erro: {error_detail}")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao conectar com o gateway: {e}")

# Configuração do app Streamlit
st.title("🌱 Estufa Inteligente Dashboard")

# Inicializa os históricos e flags de erro para cada sensor, se ainda não existirem
if "temperature_history" not in st.session_state:
    st.session_state.temperature_history = []
if "light_history" not in st.session_state:
    st.session_state.light_history = []
if "humidity_history" not in st.session_state:
    st.session_state.humidity_history = []
if "temperature_error" not in st.session_state:
    st.session_state.temperature_error = False
if "light_error" not in st.session_state:
    st.session_state.light_error = False
if "humidity_error" not in st.session_state:
    st.session_state.humidity_error = False

def update_sensor_history():
    """
    Atualiza os históricos dos sensores, adicionando o valor atual a cada lista,
    mantendo no máximo 20 valores. Verifica se o sensor está presente (não vazio)
    e ativo (active == true). Caso contrário, define a flag de erro.
    """
    sensor_data = get_sensor_data()

    # Atualiza histórico do sensor de Temperatura
    if sensor_data.get("temperature_sensor") and len(sensor_data["temperature_sensor"]) > 0:
        sensor_temp = sensor_data["temperature_sensor"][0]
        if sensor_temp.get("active", True):
            try:
                new_value = float(sensor_temp.get("valueField"))
                st.session_state.temperature_history.append(new_value)
                if len(st.session_state.temperature_history) > 20:
                    st.session_state.temperature_history = st.session_state.temperature_history[-20:]
                st.session_state.temperature_error = False
            except (ValueError, TypeError):
                st.session_state.temperature_error = True
        else:
            st.session_state.temperature_error = True
    else:
        st.session_state.temperature_error = True

    # Atualiza histórico do sensor de Luz
    if sensor_data.get("light_sensor") and len(sensor_data["light_sensor"]) > 0:
        sensor_light = sensor_data["light_sensor"][0]
        if sensor_light.get("active", True):
            try:
                new_value = float(sensor_light.get("valueField"))
                st.session_state.light_history.append(new_value)
                if len(st.session_state.light_history) > 20:
                    st.session_state.light_history = st.session_state.light_history[-20:]
                st.session_state.light_error = False
            except (ValueError, TypeError):
                st.session_state.light_error = True
        else:
            st.session_state.light_error = True
    else:
        st.session_state.light_error = True

    # Atualiza histórico do sensor de Umidade
    if sensor_data.get("humidity_sensor") and len(sensor_data["humidity_sensor"]) > 0:
        sensor_humidity = sensor_data["humidity_sensor"][0]
        if sensor_humidity.get("active", True):
            try:
                new_value = float(sensor_humidity.get("valueField"))
                st.session_state.humidity_history.append(new_value)
                if len(st.session_state.humidity_history) > 20:
                    st.session_state.humidity_history = st.session_state.humidity_history[-20:]
                st.session_state.humidity_error = False
            except (ValueError, TypeError):
                st.session_state.humidity_error = True
        else:
            st.session_state.humidity_error = True
    else:
        st.session_state.humidity_error = True

# Atualiza os históricos dos sensores (a função get_sensor_data já tem TTL de 2 segundos)
update_sensor_history()

# Seção do Sensor de Temperatura
with st.container():
    st.subheader("🌡️ Sensor de Temperatura")
    if st.session_state.temperature_error:
        st.error("Sensor de Temperatura desligado.")
    else:
        plot_sensor_history(st.session_state.temperature_history, "Temperatura", unit="°C")
    temperature_value = st.slider("Ajuste a Temperatura", min_value=0, max_value=50, value=25, key="temp_slider")
    if st.button("Enviar comando de Temperatura", key="temp_button"):
        send_actuator_command("actuator_temperature", temperature_value)

# Seção do Sensor de Luz
with st.container():
    st.subheader("💡 Sensor de Luz")
    if st.session_state.light_error:
        st.error("Sensor de Luz desligado.")
    else:
        plot_sensor_history(st.session_state.light_history, "Luz", unit="lux")
    light_value = st.slider("Ajuste a Luz", min_value=0, max_value=100, value=50, key="light_slider")
    if st.button("Enviar comando de Luz", key="light_button"):
        send_actuator_command("actuator_light", light_value)

# Seção do Sensor de Umidade
with st.container():
    st.subheader("💧 Sensor de Umidade")
    if st.session_state.humidity_error:
        st.error("Sensor de Umidade desligado.")
    else:
        plot_sensor_history(st.session_state.humidity_history, "Umidade", unit="%")
    humidity_value = st.slider("Ajuste a Umidade", min_value=0, max_value=100, value=50, key="humidity_slider")
    if st.button("Enviar comando de Umidade", key="humidity_button"):
        send_actuator_command("actuator_humidity", humidity_value)
