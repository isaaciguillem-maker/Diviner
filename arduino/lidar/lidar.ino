#include <Servo.h>

// Definició de pins
const int trigPin = 9;
const int echoPin = 10;
const int servoPin = 11;

// Variables globals
long duration;
int distance;
Servo myServo;

// Prototips de funcions
void performScan(int angle);
int calculateDistance();

void setup() {
  pinMode(trigPin, OUTPUT); // Configura el pin trig com a sortida
  pinMode(echoPin, INPUT);  // Configura el pin echo com a entrada
  Serial.begin(115200);     // Inicia comunicació sèrie a 115200 baudis
  myServo.attach(servoPin); // Connecta el servo al pin definit
}

void loop() {
  // Escombrat d'esquerra a dreta: de 30 a 150 graus del servo (-60 a +60 lògic)
  for (int angle = 30; angle <= 150; angle += 5) {
    performScan(angle);
  }

  // Escombrat de tornada: de 145 a 35 graus del servo (+55 a -55 lògic)
  // Evitem repetir els extrems (150 i 30) ja escanejats a l'anterior i següent bucle
  for (int angle = 145; angle >= 35; angle -= 5) {
    performScan(angle);
  }
}

// Funció auxiliar per moure el servo, mesurar i enviar dades
void performScan(int servoAngle) {
  myServo.write(servoAngle);
  delay(50); // Espera 50ms perquè el servo arribi i s'estabilitzi

  int currentDistance = calculateDistance();

  // Convertim l'angle del servo a angle lògic (-60 a +60)
  // 90 graus del servo és 0 graus lògic (frontal)
  int logicalAngle = servoAngle - 90;

  // Envia dades pel port sèrie: angle,distància
  Serial.print(logicalAngle);
  Serial.print(",");
  Serial.println(currentDistance);
}

// Funció per calcular la distància amb el sensor ultrasònic
int calculateDistance() {
  // Neteja el pin trig
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Envia un pols de 10 microsegons
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Llegeix el pin echo, retorna el temps de viatge de l'ona en microsegons
  // Timeout de 30ms (aprox 5m) per evitar bloqueig si no hi ha eco
  long pulseDuration = pulseIn(echoPin, HIGH, 30000);

  if (pulseDuration == 0) {
    return 400; // Si no hi ha eco (fora de rang), retornem una distància màxima (per exemple 400cm)
  }

  // Calcula la distància: velocitat del so = 0.034 cm/us
  // Distància = (Temps * Velocitat) / 2
  int dist = pulseDuration * 0.034 / 2;

  return dist;
}
