import asyncio
import websockets
import json

SERVER_IP = "0.0.0.0"
SERVER_PORT = 8765

# Intervalle pour envoyer un ping (en secondes)
PING_INTERVAL = 20
PING_TIMEOUT = 10
cloud = None
# Liste des connexions actives
connected_clients = set()


async def update_mesures(websocket):
    """
    Envoie un message à tous les clients un par un, en attendant leur réponse.

    Args:
        message (str): Le message à envoyer.
    """
    for client in [c for c in connected_clients if c != websocket]:  # Convertir en liste pour éviter les erreurs lors des modifications du set
        try:
            print(f"Envoi au client {client.remote_address}: maj")
            await client.send(json.dumps({"id":"tour","message":"maj"}))  # Envoi du message au client
        except websockets.ConnectionClosed:
            print(f"Connexion fermée pour le client {client.remote_address}")
            connected_clients.remove(client)  # Supprime les connexions fermées


async def handler(websocket, path):
    """
    Gestionnaire pour chaque client connecté.
    """
    global cloud
    print(f"Client connecté : {websocket.remote_address}")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Message reçu du client {websocket.remote_address}: {message}")
            try:
                message = json.loads(message)
            except:
                await websocket.send("mauvais format de message")

            if message.get("id") == "cloud":
                cloud = websocket
                if message.get("message") == "maj":
                    await update_mesures(websocket)
                else:
                    await websocket.send(json.dumps({"id":"tour", "message":"requête non reconnue"}))
            elif message.get("id") == "boitier":
                if message["message"]["value1"] < 500:
                    await websocket.send(json.dumps({"id":"tour", "message": "led_on"}))
                else:
                    await websocket.send(json.dumps({"id":"tour", "message": "led_off"}))
                await cloud.send(json.dumps({"id":"tour", "message":message["message"]}))
            else:
                await websocket.send(f"Message bien reçu : {message}")

    except websockets.ConnectionClosed:
        print(f"Client déconnecté : {websocket.remote_address}")
    finally:
        connected_clients.remove(websocket)


async def main():
    async with websockets.serve(handler, SERVER_IP, SERVER_PORT, ping_interval=None):
        print(f"Serveur WebSocket démarré sur {SERVER_IP}:{SERVER_PORT}")
        await asyncio.Future()  # Maintient le serveur actif


if __name__ == "__main__":
    asyncio.run(main())
