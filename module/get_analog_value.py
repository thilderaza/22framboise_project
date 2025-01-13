from grove.adc import ADC

# Initialisation du module ADC (lectures analogiques)
adc = ADC()

# Canal analogique où le potentiomètre est connecté (A0 dans cet exemple)
channel = 0

while True:
        # Lecture de la valeur brute (entre 0 et 1023 pour un ADC 10 bits)
        value = adc.read(channel)
        # Calcul de la tension (si VCC est 5V)
        voltage = value * 5.0 / 1023

        print(f"Valeur brute : {value}, Tension : {voltage:.2f} V")
