# Pseudo-LIDAR Frontal amb Arduino i Python

Aquest projecte implementa un sistema de radar/pseudo-LIDAR frontal utilitzant un sensor ultrasònic HC-SR04 muntat sobre un servo estàndard, controlat per un Arduino Mega. Les dades es visualitzen en temps real en un PC mitjançant un script de Python optimitzat.

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

## Configuració i Ajustos

### Resolució Angular
Per defecte, l'escaneig es fa cada **5 graus**.
Si vols canviar-ho (per exemple a 2 graus per més precisió o 10 per més velocitat):
1. A `arduino/lidar/lidar.ino`: Canvia `const int STEP_ANGLE = 5;` pel valor desitjat.
2. A `pc/radar.py`: Canvia `STEP_ANGLE = 5` pel mateix valor.

### Sentit de Gir
Si el radar a la pantalla es mou al revés del moviment físic del servo:
- A `pc/radar.py`, canvia `ax.set_theta_direction(-1)` a `1` (o viceversa).

### Velocitat
- El sistema està configurat amb un `delay` de 30ms per posició. Pots ajustar `SCAN_DELAY` a l'Arduino, però valors inferiors a 25ms poden causar lectures inestables del sensor ultrasònic.

## Funcionament Tècnic

1. **Escaneig:** L'Arduino mou el servo de 30° a 150° (sector frontal de -60° a +60°).
2. **Mesura:** Es calcula la distància amb la fórmula `distància = durada / 58` (cm).
3. **Comunicació:** L'Arduino envia `angle,distància` via Sèrie a 115200 baudis.
4. **Visualització:** Python actualitza només els punts necessaris del gràfic polar per garantir un rendiment fluid sense parpelleig.
