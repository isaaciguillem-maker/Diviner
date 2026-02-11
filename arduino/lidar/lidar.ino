#include <Servo.h>

// Configuració
const int STEP_ANGLE = 5;      // Pas angular (en graus)
const int MIN_SERVO = 30;      // Angle mínim servo (30 graus -> -60 lògic)
const int MAX_SERVO = 150;     // Angle màxim servo (150 graus -> +60 lògic)
const int SERVO_DELAY = 60;    // Temps d'espera perquè el servo s'estabilitzi abans de mesurar (ms)
const int READINGS_COUNT = 5;  // Nombre de lectures per fer la mediana
const int MAX_DIST = 400;      // Distància màxima vàlida

// Definició de pins
const int trigPin = 9;
const int echoPin = 10;
const int servoPin = 11;

// Variables globals
Servo myServo;

// Prototips
void performScan(int angle);
int getMedianDistance();
int calculateDistance();

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(115200);
  myServo.attach(servoPin);
}

void loop() {
  // Escombrat d'esquerra a dreta
  for (int angle = MIN_SERVO; angle <= MAX_SERVO; angle += STEP_ANGLE) {
    performScan(angle);
  }

  // Escombrat de tornada
  for (int angle = MAX_SERVO - STEP_ANGLE; angle > MIN_SERVO; angle -= STEP_ANGLE) {
    performScan(angle);
  }
}

void performScan(int servoAngle) {
  myServo.write(servoAngle);

  // 1. Estabilització mecànica: donar temps al servo
  delay(SERVO_DELAY);

  // 2. Múltiples lectures: obtenir mediana per filtrar soroll
  int currentDistance = getMedianDistance();

  // Convertim l'angle del servo a angle lògic (-60 a +60)
  int logicalAngle = servoAngle - 90;

  Serial.print(logicalAngle);
  Serial.print(",");
  Serial.println(currentDistance);
}

int getMedianDistance() {
  int readings[READINGS_COUNT];

  // Prenem N lectures amb petit interval
  for (int i = 0; i < READINGS_COUNT; i++) {
    readings[i] = calculateDistance();
    delay(15); // Petit retard entre pings per evitar ecos residuals
  }

  // Ordenem l'array (Bubble sort simple)
  for (int i = 0; i < READINGS_COUNT - 1; i++) {
    for (int j = 0; j < READINGS_COUNT - i - 1; j++) {
      if (readings[j] > readings[j + 1]) {
        int temp = readings[j];
        readings[j] = readings[j + 1];
        readings[j + 1] = temp;
      }
    }
  }

  // Retornem la mediana (element central)
  int median = readings[READINGS_COUNT / 2];

  // Filtratge final de valors absurds
  if (median <= 0 || median > MAX_DIST) {
    return MAX_DIST;
  }

  return median;
}

int calculateDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Timeout ajustat per no bloquejar (aprox 4m)
  long pulseDuration = pulseIn(echoPin, HIGH, 25000);

  if (pulseDuration == 0) {
    return MAX_DIST; // Timeout o sense eco
  }

  return (int)(pulseDuration / 58);
}
