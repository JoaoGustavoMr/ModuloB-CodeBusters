import serial
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# -------------------
# Configuração Serial
# -------------------
porta = 'COM9'  # Porta do Arduino
baud = 9600
arduino = serial.Serial(porta, baud, timeout=1)

# -------------------
# Arquivos
# -------------------
arquivo_csv = 'dados_sensores.csv'
arquivo_log = 'anomalias.log'

# Criar CSV com cabeçalho
with open(arquivo_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'node', 'temperatura', 'umidade'])

# -------------------
# Limites de anomalia
# -------------------
limite_temp = 30           # °C
limite_umidade_min = 40    # %
limite_umidade_max = 70    # %
node_id = "Node1"

# -------------------
# Configuração do gráfico
# -------------------
fig, ax = plt.subplots(2, 1, figsize=(10,8))
plt.tight_layout(pad=3)

def atualizar(i):
    try:
        df = pd.read_csv(arquivo_csv)
        ax[0].cla()
        ax[1].cla()
        
        # Temperatura
        ax[0].plot(pd.to_datetime(df['timestamp']), df['temperatura'], color='r')
        ax[0].set_title("Temperatura")
        ax[0].set_ylabel("°C")
        
        # Umidade
        ax[1].plot(pd.to_datetime(df['timestamp']), df['umidade'], color='b')
        ax[1].set_title("Umidade")
        ax[1].set_ylabel("%")
        ax[1].set_xlabel("Tempo")
    except:
        pass

ani = FuncAnimation(fig, atualizar, interval=5000)
plt.ion()
plt.show()

# -------------------
# Loop principal
# -------------------
while True:
    try:
        linha = arduino.readline().decode('utf-8').strip()
        if linha:
            # Espera dados no formato "25.4,60.1"
            temp, hum = map(float, linha.split(','))
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Salvar no CSV
            with open(arquivo_csv, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, node_id, temp, hum])

            # Checar anomalias
            if temp > limite_temp:
                with open(arquivo_log, 'a') as log:
                    log.write(f"{timestamp},{node_id},Temperatura alta,{temp}\n")
                print(f"ALERTA: Temperatura alta! {temp}°C")

            if hum < limite_umidade_min or hum > limite_umidade_max:
                with open(arquivo_log, 'a') as log:
                    log.write(f"{timestamp},{node_id},Umidade fora do limite,{hum}\n")
                print(f"ALERTA: Umidade fora do limite! {hum}%")

            # Mostrar no console
            print(f"{timestamp} | {node_id} | Temp: {temp}°C | Hum: {hum}%")
        
        plt.pause(0.01)
    except KeyboardInterrupt:
        print("Finalizando...")
        break
    except Exception as e:
        print("Erro:", e)
