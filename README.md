# Pseudo-LIDAR Frontal amb Arduino i Python

Aquest projecte implementa un sistema de radar/pseudo-LIDAR frontal utilitzant un sensor ultrasònic HC-SR04 muntat sobre un servo estàndard, controlat per un Arduino Mega. Les dades es visualitzen en temps real en un PC mitjançant un script de Python optimitzat per a una visualització clara i neta.

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

## Configuració i Ajustos Visuals

El radar està configurat per defecte per ser molt visual i net, ideal per interiors:

- **Rang:** Mostra objectes fins a **200 cm**.
- **Filtratge:** Ignora objectes a menys de **15 cm** (soroll) o a més de **200 cm**.
- **Zona Òptima:** Ressalta una franja verda entre **50 cm i 120 cm** per identificar ràpidament objectes a distància de treball.
- **Visualització:** Utilitza punts grans i vermells sense línies ni farcits per evitar confusions.

### Personalització

Pots editar `pc/radar.py` per canviar aquests paràmetres:

```python
MAX_DISTANCE = 200    # Distància màxima visual (cm)
MIN_VALID_DISTANCE = 15 # Filtratge de soroll proper
ZONE_START = 50       # Inici zona verda
ZONE_END = 120        # Final zona verda
```

### Sentit de Gir
Si el radar a la pantalla es mou al revés del moviment físic del servo:
- A `pc/radar.py`, canvia `ax.set_theta_direction(-1)` a `1` (o viceversa).

## Funcionament Tècnic

1. **Escaneig:** L'Arduino mou el servo de 30° a 150° (sector frontal de -60° a +60°).
2. **Mesura:** Es calcula la distància amb la fórmula `distància = durada / 58` (cm).
3. **Comunicació:** L'Arduino envia `angle,distància` via Sèrie a 115200 baudis.
4. **Visualització:** Python filtra i dibuixa només els punts vàlids sobre un gràfic polar net.
