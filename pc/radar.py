import serial
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import sys
import time

# Configuració
SERIAL_PORT = 'COM3'  # Windows: COM3, Linux: /dev/ttyUSB0
BAUD_RATE = 115200
MAX_DISTANCE = 400    # Distància màxima del sensor en cm
STEP_ANGLE = 5        # Pas angular (ha de coincidir amb l'Arduino)
MIN_ANGLE = -60       # Angle lògic mínim
MAX_ANGLE = 60        # Angle lògic màxim

# Inicialització de dades
angles_deg = np.arange(MIN_ANGLE, MAX_ANGLE + 1, STEP_ANGLE)
angles_rad = np.radians(angles_deg)
distances = np.full_like(angles_deg, MAX_DISTANCE, dtype=float)

ser = None

# Intentem connectar al port sèrie
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    print(f"Connectat al port {SERIAL_PORT}")
except serial.SerialException:
    print(f"Error: No s'ha pogut obrir el port {SERIAL_PORT}.")
    print("Comprova que l'Arduino està connectat i el port és correcte.")
    # Si volem provar sense Arduino, comentem la línia de sortida
    sys.exit(1)

# Configuració inicial del gràfic
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='polar')

# Configuració dels eixos
ax.set_theta_zero_location("N") # 0 graus al Nord (Frontal)
ax.set_theta_direction(-1)      # -1 per sentit horari, 1 per anti-horari
ax.set_rlabel_position(0)
ax.set_ylim(0, MAX_DISTANCE)
# Ajustem la vista als angles d'interès amb marge
ax.set_thetamin(MIN_ANGLE - 10)
ax.set_thetamax(MAX_ANGLE + 10)
ax.set_title("Radar Frontal Pseudo-LIDAR", va='bottom')

# Inicialitzem els gràfics
# Guardem referències per actualitzar-los després
line, = ax.plot(angles_rad, distances, 'b-') # Línia de contorn
points, = ax.plot(angles_rad, distances, 'ro', markersize=3) # Punts de mesura

# Fill retorna una llista de polígons, agafem el primer
fill_poly_list = ax.fill(angles_rad, distances, 'b', alpha=0.3)
fill_poly = fill_poly_list[0]

def update_data():
    global distances
    # Llegim totes les línies disponibles al buffer
    if ser and ser.is_open:
        while ser.in_waiting > 0:
            try:
                line_str = ser.readline().decode('utf-8').strip()
                if not line_str: continue

                parts = line_str.split(',')
                if len(parts) == 2:
                    angle = int(parts[0])
                    dist = int(parts[1])

                    # Filtre de distància
                    if dist > MAX_DISTANCE or dist <= 0:
                        dist = MAX_DISTANCE

                    # Busquem l'índex corresponent a l'angle rebut
                    idx = np.where(angles_deg == angle)[0]

                    if len(idx) > 0:
                        distances[idx[0]] = dist

            except ValueError:
                pass # Ignorem línies malformades
            except Exception as e:
                print(f"Error llegint: {e}")

def animate(i):
    global fill_poly
    update_data()

    # Actualitzem les dades de la línia i els punts (eficient)
    line.set_ydata(distances)
    points.set_ydata(distances)

    # Per l'àrea ombrejada (fill), l'estratègia més robusta és esborrar i recrear
    try:
        fill_poly.remove()
    except ValueError:
        pass # Si ja s'ha eliminat

    # Creem el nou polígon omplert
    fill_poly_list = ax.fill(angles_rad, distances, 'b', alpha=0.3)
    fill_poly = fill_poly_list[0]

    return line, points, fill_poly

# Iniciem l'animació
# interval=30ms per una visualització fluida (~30fps)
ani = FuncAnimation(fig, animate, interval=30, blit=False)

plt.show()

# Tanquem el port en sortir
if ser and ser.is_open:
    ser.close()
