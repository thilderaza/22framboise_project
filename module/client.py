import asyncio
import websockets
import json
from grove.adc import ADC
from network_tools import get_ip_from_mac
import RPi.GPIO as GPIO

adc = ADC()

mac = "b8:27:eb:54:0d:5c"  # Adresse MAC tour
SERVER_IP = get_ip_from_mac(mac)
SERVER_PORT = 8765

async def send_value(websocket):
    channel = 0
    value = adc.read(channel)
    voltage = value * 5.0 / 1023
    await websocket.send(json.dumps({"id":"boitier", "message":{"id_boitier":2, "value1":value}}))

def set_led(value):
    print(value)
    LED_PIN = 5
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    if value == "on":
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("ok on")
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
        print("ok off")
    GPIO.cleanup()

async def communicate():
    uri = f"ws://{SERVER_IP}:{SERVER_PORT}"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connecté au serveur WebSocket")
            async def receive_messages():
                while True:
                    try:
                        response = await websocket.recv()
                        response = json.loads(response)
                        print(f"Message reçu du serveur : {response}")
                        # Répondre automatiquement si nécessaire
                        if response["id"] == "tour" and response["message"] == "maj":
                            await send_value(websocket)
                        elif response["id"] == "tour" and "led" in response["message"]:
                            if "on" in response["message"]:
                                set_led("on")
                            else:
                                set_led("off")
                    except websockets.ConnectionClosed:
                        print("Connexion au serveur perdue.")
                        break

            # Lancer en parallèle l'envoi et la réception de messages
            await receive_messages()

    except Exception as e:
        print(f"Erreur de connexion : {e}")


if __name__ == "__main__":
    asyncio.run(communicate())
