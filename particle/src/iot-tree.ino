/*
 * Project iot-tree
 * Description: Turn tree on and off with Siri.
 * Author: Adam Walsh
 * Date: 2019-11-28
 */
int relayPin = D2;
int treeStatus = 0;

void setup()
{
  pinMode(relayPin, OUTPUT);
  Particle.variable("treeStatus", &treeStatus, INT);
  Particle.function("toggleTree", toggleTree);
}

void loop() {}

/**
 * Turn the tree on. 
 */
void turnOn()
{
  if (treeStatus == 0)
  {
    digitalWrite(relayPin, HIGH);
    treeStatus = 1;
  }
}
/**
 * Turn the tree off. 
 */
void turnOff()
{
  if (treeStatus == 1)
  {
    digitalWrite(relayPin, LOW);
    treeStatus = 0;
  }
}
/**
 * This function is exposed to the Particle cloud 
 * so that we can toggle the tree's lights on and off.
 * 
 * @param mode Wether to turn the tree on or off. "1" for on, "0" for off.
 */
int toggleTree(String mode)
{
  if (mode == "1")
  {
    digitalWrite(relayPin, HIGH);
    treeStatus = 1;
  }
  else if (mode == "0")
  {
    digitalWrite(relayPin, LOW);
    treeStatus = 0;
  }
  return treeStatus;
}