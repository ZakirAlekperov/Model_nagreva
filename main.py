import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Параметры модели
initial_temperature = 20  # начальная температура в °C
target_temperature = 200   # целевая температура в °C
time_steps = 240          # время моделирования в минутах (4 часа)
dt = 1                    # шаг времени в минутах



# Визуализация результатов
plt.figure(figsize=(10, 5))
plt.plot(t, temperatures, label='Температура в печи', color='orange')
plt.axhline(y=target_temperature, color='red', linestyle='--', label='Целевая температура')
plt.title('Модель нагревания в хлебопекарной печи с ПИД-регулятором и внешними возмущениями (4 часа)')
plt.xlabel('Время (минуты)')
plt.ylabel('Температура (°C)')
plt.legend()
plt.grid()
plt.show()