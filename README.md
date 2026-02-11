# Pseudo-LIDAR Frontal amb Arduino i Python

Aquest projecte implementa un sistema de radar/pseudo-LIDAR frontal d'alta precisió utilitzant un sensor ultrasònic HC-SR04 muntat sobre un servo estàndard, controlat per un Arduino Mega. Les dades es visualitzen en temps real en un PC mitjançant un script de Python optimitzat.

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

**Nota sobre el rendiment:** El firmware està configurat per prioritzar la **precisió** sobre la velocitat. L'escombrat serà més lent que en versions anteriors perquè fa múltiples lectures per posició per eliminar soroll.

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

## Configuració i Visualització

El radar està configurat per defecte per ser molt visual i net:
- **Rang visual:** Fins a 200 cm.
- **Filtratge:** Ignora soroll (<15cm) i valors llunyans (>200cm).
- **Zona Òptima:** Ressalta la franja de 50-120 cm.
- **Gràfics:** Utilitza punts vermells clars sobre fons polar.

### Personalització Tècnica (Arduino)

A `arduino/lidar/lidar.ino` pots ajustar:
- `SERVO_DELAY`: Temps d'espera mecànica (per defecte 60ms).
- `READINGS_COUNT`: Nombre de lectures per fer la mediana (per defecte 5). Augmentar-ho millora la precisió però alenteix l'escombrat.

## Funcionament Tècnic

1. **Escaneig:** L'Arduino mou el servo de 30° a 150° (sector frontal de -60° a +60°).
2. **Estabilització:** S'espera 60ms perquè el servo deixi de vibrar.
3. **Multimostreig:** Es fan 5 lectures consecutives del sensor ultrasònic.
4. **Filtratge:** Es calcula la mediana de les lectures per descartar valors erronis (outliers).
5. **Comunicació:** S'envia `angle,distància_mediana` via Sèrie a 115200 baudis.
6. **Visualització:** Python mostra les dades filtrades en un radar polar.
