# Boitiers
## Lecture des valeurs analogues
pip install grove.py

sudo raspi-config
  → activer la communication I2C
sudo reboot

## Initialisation d'un nouveau boitier

### Étape 1 : Configuration du fichier de service systemd
Créez un fichier de service systemd pour votre script Python.

Ouvrez un éditeur pour créer un nouveau fichier de service :

```bash
sudo nano /etc/systemd/system/websocket-client.service
```
Ajoutez la configuration suivante au fichier :

```ini
[Unit]
Description=Client WebSocket Python
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/bin/python3 /chemin/vers/votre/script.py
Restart=always
RestartSec=10
Environment=PYTHONUNBUFFERED=1
StandardOutput=journal
StandardError=journal
User=pi
Group=pi

[Install]
WantedBy=multi-user.target
Explication des paramètres
After=network-online.target et Wants=network-online.target : Assurent que le service démarre uniquement une fois que le réseau (Wi-Fi inclus) est opérationnel.
ExecStart : Commande pour exécuter le script Python.
Restart=always : Relance automatiquement le service en cas d'arrêt (ex. : si le serveur WebSocket est indisponible).
RestartSec=10 : Attend 10 secondes avant de redémarrer le service après un échec.
Environment=PYTHONUNBUFFERED=1 : Désactive le buffering de Python pour que les journaux soient immédiatement visibles.
StandardOutput=journal et StandardError=journal : Envoie les sorties standard et d'erreur dans les journaux de systemd.
```

### Étape 2 : Activer et démarrer le service
Rechargez les fichiers de service systemd pour inclure votre nouveau service :

```bash
sudo systemctl daemon-reload
```

Activez le service pour qu'il démarre au démarrage :

```bash
sudo systemctl enable websocket-client.service
```

Démarrez le service immédiatement :

```bash
sudo systemctl start websocket-client.service
```

Vérifiez le statut du service pour voir s'il fonctionne correctement :

```bash
sudo systemctl status websocket-client.service
```

### Étape 3 : Gestion des journaux
Les journaux générés par votre script Python seront accessibles via journalctl. Pour les consulter :

```bash
sudo journalctl -u websocket-client.service -f
```

Tout est automatisé dans le script `init.sh` qui se trouve dans le dossier `Documents` du Raspberry Pi, il suffit de lancer la commande suivante :

```bash
sudo chmod +x Documents/init.sh
sudo bash Documents/init.sh
```