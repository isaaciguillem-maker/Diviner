#include <Servo.h>

// Configuració
const int STEP_ANGLE = 5;      // Pas angular (en graus)
const int MIN_SERVO = 30;      // Angle mínim servo (30 graus -> -60 lògic)
const int MAX_SERVO = 150;     // Angle màxim servo (150 graus -> +60 lògic)
const int SCAN_DELAY = 30;     // Temps d'espera per mesura (ms)

// Definició de pins
const int trigPin = 9;
const int echoPin = 10;
const int servoPin = 11;

// Variables globals
long duration;
int distance;
Servo myServo;

// Prototips
void performScan(int angle);
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
  // Evitem repetir els extrems (MAX_SERVO i MIN_SERVO)
  for (int angle = MAX_SERVO - STEP_ANGLE; angle > MIN_SERVO; angle -= STEP_ANGLE) {
    performScan(angle);
  }
}

void performScan(int servoAngle) {
  myServo.write(servoAngle);
  delay(SCAN_DELAY); // Espera optimitzada a 30ms

  int currentDistance = calculateDistance();

  // Convertim l'angle del servo a angle lògic (-60 a +60)
  // 90 graus del servo és 0 graus lògic (frontal)
  int logicalAngle = servoAngle - 90;

  Serial.print(logicalAngle);
  Serial.print(",");
  Serial.println(currentDistance);
}

int calculateDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Timeout ajustat per no bloquejar si no hi ha eco (aprox 5m)
  long pulseDuration = pulseIn(echoPin, HIGH, 30000);

  if (pulseDuration == 0) {
    return 400; // Fora de rang
  }

  // Càlcul simplificat: velocitat del so ~340m/s -> 1cm / 29us -> anada i tornada / 58
  return pulseDuration / 58;
}
