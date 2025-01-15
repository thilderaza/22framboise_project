#!/bin/bash

# Variables
SERVICE_NAME="websocket-client.service"
SCRIPT_PATH="/home/pi/websocket_client.py"  # Path to your Python script
PYTHON_PATH="/usr/bin/python3"              # Path to Python executable
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME"
RUN_AS_USER="pi"                            # The user to run the service as

# Vérification des privilèges
if [ "$(id -u)" -ne 0 ]; then
    echo "Ce script doit être exécuté avec les droits root (sudo)." >&2
    exit 1
fi

# Étape 1 : Création du fichier de service systemd
echo "Création du fichier de service systemd : $SERVICE_FILE"

cat <<EOL > $SERVICE_FILE
[Unit]
Description=Client WebSocket Python
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=$PYTHON_PATH $SCRIPT_PATH
Restart=always
RestartSec=10
Environment=PYTHONUNBUFFERED=1
StandardOutput=journal
StandardError=journal
User=$RUN_AS_USER
Group=$RUN_AS_USER

[Install]
WantedBy=multi-user.target
EOL

echo "Fichier de service créé."

# Étape 2 : Recharger systemd pour prendre en compte le nouveau service
echo "Rechargement de systemd..."
systemctl daemon-reload

# Étape 3 : Activer le service pour qu'il démarre au démarrage
echo "Activation du service au démarrage..."
systemctl enable $SERVICE_NAME

# Étape 4 : Démarrer le service
echo "Démarrage du service..."
systemctl start $SERVICE_NAME

# Étape 5 : Vérification du statut du service
echo "Statut du service :"
systemctl status $SERVICE_NAME --no-pager

# Instructions finales
echo "Configuration terminée. Les journaux du service peuvent être consultés avec :"
echo "sudo journalctl -u $SERVICE_NAME -f"
