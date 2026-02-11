import serial
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import time
import sys

# Configuració
SERIAL_PORT = 'COM3'  # Canvia-ho pel teu port (ex: 'COM3' a Windows, '/dev/ttyUSB0' a Linux)
BAUD_RATE = 115200
MAX_DISTANCE = 400    # Distància màxima del sensor en cm

# Inicialització de dades
# Angles d'escaneig: de -60 a +60 graus, cada 5 graus.
angles_deg = np.arange(-60, 61, 5) # array([-60, -55, ..., 60])
angles_rad = np.radians(angles_deg) # Convertim a radiants per matplotlib
distances = np.full_like(angles_deg, MAX_DISTANCE, dtype=float) # Inicialitzem amb distància màxima

# Intentem connectar al port sèrie
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    print(f"Connectat al port {SERIAL_PORT}")
except serial.SerialException:
    print(f"Error: No s'ha pogut obrir el port {SERIAL_PORT}.")
    print("Comprova que l'Arduino està connectat i el port és correcte.")
    # Per proves sense Arduino, podem comentar la línia següent:
    sys.exit(1)

# Funció per llegir dades del port sèrie
def update_data():
    global distances
    # Llegim totes les línies disponibles al buffer
    while ser and ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8').strip()
            if not line: continue

            parts = line.split(',')
            if len(parts) == 2:
                angle = int(parts[0])
                dist = int(parts[1])

                # Filtre de distància
                if dist > MAX_DISTANCE or dist <= 0:
                    dist = MAX_DISTANCE

                # Busquem l'índex corresponent a l'angle rebut
                # L'angle ve de -60 a 60 en passos de 5.
                # L'array angles_deg té valors [-60, -55, ..., 60]
                idx = np.where(angles_deg == angle)[0]

                if len(idx) > 0:
                    distances[idx[0]] = dist

        except ValueError:
            pass # Ignorem línies malformades
        except Exception as e:
            print(f"Error llegint: {e}")

# Funció d'animació
def animate(i):
    update_data()

    ax.clear()

    # Configuració del gràfic polar
    ax.set_theta_zero_location("N") # 0 graus al Nord (Frontal)
    ax.set_theta_direction(-1)      # Sentit horari (opcional, ajusta segons el teu servo)
    # Nota: Si el teu servo esquerra és positiu, posa sentit anti-horari (per defecte o 1)
    # Si el teu servo dreta és positiu, posa sentit horari (-1)

    ax.set_rlabel_position(0)
    ax.set_ylim(0, MAX_DISTANCE)
    ax.set_title("Radar Frontal", va='bottom')

    # Dibuixem l'àrea detectada (com un radar sòlid)
    # Afegim el punt (0,0) al polígon per tancar-lo correctament cap a l'origen si volem
    # Però fill() ja ho fa bé en polar.

    ax.fill(angles_rad, distances, 'b', alpha=0.3) # Omplert blau translúcid
    ax.plot(angles_rad, distances, 'b-')           # Línia de contorn
    ax.plot(angles_rad, distances, 'ro', markersize=3) # Punts vermells per les mesures

    # Limitem la vista als angles d'interès (-90 a 90 per tenir context frontal)
    ax.set_thetamin(-90)
    ax.set_thetamax(90)

# Configuració de la finestra
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='polar')

# Iniciem l'animació
ani = FuncAnimation(fig, animate, interval=50) # Actualitza cada 50ms

plt.show()

# Tanquem el port en sortir
if ser:
    ser.close()
