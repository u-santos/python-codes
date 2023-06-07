import datetime
import time

# Obtenha a hora atual do servidor
current_time = datetime.datetime.now().time()
current_minute = current_time.minute

print(current_time)
if current_minute >= 15 and current_minute <= 25:
    print("Aguardando 10 minutos...")
    time.sleep(600)  # 10 minutos em segundos