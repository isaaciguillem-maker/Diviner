# Pseudo-LIDAR Frontal amb Arduino i Python

Aquest projecte implementa un sistema de radar/pseudo-LIDAR frontal utilitzant un sensor ultrasònic HC-SR04 muntat sobre un servo estàndard, controlat per un Arduino Mega. Les dades es visualitzen en temps real en un PC mitjançant un script de Python.

## Estructura del Projecte

- `arduino/lidar/lidar.ino`: Codi font per a l'Arduino.
- `pc/radar.py`: Script de visualització en Python.
- `pc/requirements.txt`: Llibreries Python necessàries.

## Requisits de Hardware

- **Arduino Mega** (o compatible, ajustant els pins si cal).
- **Sensor Ultrasònic HC-SR04**.
- **Servo Motor** estàndard (0-180 graus).
- Cables de connexió.

### Connexions

| Component | Pin Arduino | Descripció |
|-----------|-------------|------------|
| HC-SR04 Trig | 9 | Trigger del sensor |
| HC-SR04 Echo | 10 | Echo del sensor |
| Servo Senyal | 11 | Control del servo |
| VCC | 5V | Alimentació |
| GND | GND | Massa |

*Nota: Assegura't d'alimentar el servo amb una font externa si el corrent de l'USB no és suficient, connectant els GND comuns.*

## Instal·lació i Ús

### 1. Arduino

1. Obre `arduino/lidar/lidar.ino` amb l'Arduino IDE.
2. Selecciona la placa **Arduino Mega** i el port COM corresponent.
3. Puja el codi a la placa.
4. El servo començarà a escombrar automàticament.

### 2. Python (PC)

1. Instal·la Python (si no el tens).
2. Instal·la les dependències necessàries:
   ```bash
   pip install -r pc/requirements.txt
   ```
3. Edita l'arxiu `pc/radar.py` i modifica la variable `SERIAL_PORT` amb el teu port COM (ex: `COM3` a Windows o `/dev/ttyUSB0` a Linux).
4. Executa l'script:
   ```bash
   python pc/radar.py
   ```

## Funcionament

1. **Escaneig:** L'Arduino mou el servo de 30° a 150° (corresponent a un angle frontal de -60° a +60°).
2. **Mesura:** A cada pas de 5°, el sensor mesura la distància.
3. **Comunicació:** L'Arduino envia les dades en format `angle,distància` pel port sèrie.
4. **Visualització:** El PC rep les dades i actualitza un gràfic polar en temps real, mostrant els objectes detectats davant del sensor.

## Personalització

- **Angle d'escaneig:** Pots modificar els límits del bucle `for` a `lidar.ino`.
- **Velocitat:** Pots canviar el `delay(50)` a `lidar.ino` per fer l'escaneig més ràpid o més lent (tingues en compte la velocitat del so).
- **Visualització:** Pots ajustar `MAX_DISTANCE` a `radar.py` segons el rang que vulguis visualitzar.
