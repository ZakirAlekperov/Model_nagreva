import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Параметры модели
initial_temperature = 20  # начальная температура в °C
target_temperature = 200   # целевая температура в °C
time_steps = 240          # время моделирования в минутах (4 часа)
dt = 1                    # шаг времени в минутах

# Параметры передаточной функции
K = 0.5                   # коэффициент усиления
tau = 5                   # постоянная времени

# Параметры ПИД-регулятора
Kp = 1.0                  # Пропорциональный коэффициент
Ki = 0.1                  # Интегральный коэффициент
Kd = 0.01                 # Дифференциальный коэффициент

# Создание передаточной функции G(s) = K / (tau * s + 1)
num = [K]                 # числитель
den = [tau, 1]           # знаменатель
system = signal.TransferFunction(num, den)

# Временные точки
t = np.arange(0, time_steps + dt, dt)

# Массив для хранения температур и управляющего сигнала
temperatures = np.zeros(len(t))
temperatures[0] = initial_temperature

# Массив для хранения управляющего сигнала (мощности нагрева)
control_signal = np.zeros(len(t))

# Переменные для ПИД-регулятора
integral_error = 0
last_error = 0

# Внешние возмущения (например, изменение температуры)
external_influence_time = [60, 120, 180]  # моменты времени внешнего возмущения в минутах
external_influence_value = -15              # изменение температуры при возмущении

# Модель нагрева с использованием передаточной функции и ПИД-регулятора
for i in range(1, len(t)):
    # Применение внешнего возмущения
    if i in external_influence_time:
        temperatures[i - 1] += external_influence_value
    
    # Вычисление ошибки (разница между целевой и текущей температурой)
    error = target_temperature - temperatures[i - 1]
    
    # ПИД-вычисления
    integral_error += error * dt  # Интегральная часть
    derivative_error = (error - last_error) / dt if i > 1 else 0  # Дифференциальная часть
    
    # Управляющий сигнал от ПИД-регулятора
    control_signal[i] = Kp * error + Ki * integral_error + Kd * derivative_error
    
    # Применение передаточной функции к управляющему сигналу
    _, y, _ = signal.lsim(system, control_signal[:i+1], t[:i+1])
    
    # Обновление температуры на основе выходного сигнала системы
    temperatures[i] = initial_temperature + y[-1]
    
    last_error = error  # Обновление ошибки

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