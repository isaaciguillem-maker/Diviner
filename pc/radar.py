import serial
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import sys

# Configuració
SERIAL_PORT = 'COM3'  # Windows: COM3, Linux: /dev/ttyUSB0
BAUD_RATE = 115200
MAX_DISTANCE = 200    # Distància màxima visual (cm)
MIN_VALID_DISTANCE = 15 # Ignorem lectures massa properes (soroll)
STEP_ANGLE = 5        # Pas angular (ha de coincidir amb l'Arduino)
MIN_ANGLE = -60       # Angle lògic mínim
MAX_ANGLE = 60        # Angle lògic màxim

# Zona d'interès destacada (fons verd)
ZONE_START = 50
ZONE_END = 120

# Inicialització de dades
angles_deg = np.arange(MIN_ANGLE, MAX_ANGLE + 1, STEP_ANGLE)
angles_rad = np.radians(angles_deg)
# Inicialitzem amb valors fora de rang per no dibuixar res al principi
distances = np.full_like(angles_deg, MAX_DISTANCE + 50, dtype=float)

ser = None
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    print(f"Connectat al port {SERIAL_PORT}")
except serial.SerialException:
    print(f"Error: No s'ha pogut obrir el port {SERIAL_PORT}.")
    print("Comprova que l'Arduino està connectat i el port és correcte.")
    # Si volem provar sense Arduino, comentem la línia de sortida
    sys.exit(1)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='polar')

ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_rlabel_position(45)
ax.set_ylim(0, MAX_DISTANCE)
ax.set_thetamin(MIN_ANGLE - 10)
ax.set_thetamax(MAX_ANGLE + 10)
ax.set_title("Radar Frontal Pseudo-LIDAR", va='bottom', fontsize=14, fontweight='bold')

# Dibuixem la zona d'interès estàtica
theta_zone = np.linspace(np.radians(MIN_ANGLE - 10), np.radians(MAX_ANGLE + 10), 100)
# En polar, fill_between necessita una matriu de theta i el radi (o dos)
# Per crear una franja constant, passem valors escalars o arrays de la mateixa mida
ax.fill_between(theta_zone, ZONE_START, ZONE_END, color='green', alpha=0.15, label='Zona Òptima (50-120cm)')

# Afegim elements dummy a la llegenda per controlar-la manualment
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', label='Objecte Detectat',
               markerfacecolor='red', markersize=10, markeredgecolor='black'),
    plt.Rectangle((0,0), 1, 1, color='green', alpha=0.15, label='Zona Òptima')
]
ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.1, 1.1))

scatter = ax.scatter([], [], c='red', s=60, alpha=0.8, edgecolors='maroon', linewidth=0.5)

def update_data():
    if ser and ser.is_open:
        while ser.in_waiting > 0:
            try:
                line_str = ser.readline().decode('utf-8').strip()
                if not line_str: continue

                parts = line_str.split(',')
                if len(parts) == 2:
                    angle = int(parts[0])
                    dist = int(parts[1])

                    idx = np.where(angles_deg == angle)[0]
                    if len(idx) > 0:
                        if dist < MIN_VALID_DISTANCE or dist > MAX_DISTANCE:
                             distances[idx[0]] = MAX_DISTANCE + 50
                        else:
                             distances[idx[0]] = dist
            except:
                pass

def animate(i):
    global scatter
    update_data()

    # Eliminem l'scatter anterior
    try:
        scatter.remove()
    except ValueError:
        pass # Per si ja s'ha esborrat

    mask = (distances >= MIN_VALID_DISTANCE) & (distances <= MAX_DISTANCE)
    valid_angles = angles_rad[mask]
    valid_distances = distances[mask]

    scatter = ax.scatter(valid_angles, valid_distances, c='red', s=70, alpha=0.9, edgecolors='black', linewidth=0.8)

    return scatter,

ani = FuncAnimation(fig, animate, interval=30, blit=False)

plt.tight_layout()
plt.show()

if ser and ser.is_open:
    ser.close()
