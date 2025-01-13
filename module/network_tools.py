import subprocess
import re
import socket

def get_ip_from_mac(mac_address):
    """
    Récupère l'adresse IP locale associée à une adresse MAC donnée.

    Args:
        mac_address (str): L'adresse MAC (par exemple, '00:1A:2B:3C:4D:5E').

    Returns:
        str: L'adresse IP locale correspondante, ou None si introuvable.
    """
    try:
        # Exécute la commande ARP pour afficher la table ARP
        output = subprocess.check_output("ip neigh", shell=True, text=True)

        # Recherche l'adresse MAC et l'adresse IP correspondante
        pattern = re.compile(rf"(\d+\.\d+\.\d+\.\d+)\s+dev\s+\S+\s+lladdr\s+{mac_address}\s+.*(REACHABLE|STALE)", re.IGNORECASE)
        match = pattern.search(output)

        if match:
            return match.group(1)  # Retourne l'adresse IP trouvée

        return None  # Adresse IP non trouvée
    except Exception as e:
        print(f"Erreur : {e}")
        return None


def get_local_ip():
    try:
        # Se connecter à un serveur arbitraire pour déterminer l'interface réseau active
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception as e:
        print(f"Erreur lors de la récupération de l'adresse IP : {e}")
        return "0.0.0.0"

# Exemple d'utilisation
if __name__ == "__main__":
    mac = "b8:27:eb:54:0d:5c"  # Adresse mac de la tour
    ip = get_ip_from_mac(mac)
    if ip:
        print(f"L'adresse IP pour {mac} est : {ip}")
    else:
        print(f"Aucune adresse IP trouvée pour {mac}.")

    print("local IP : " + get_local_ip())
