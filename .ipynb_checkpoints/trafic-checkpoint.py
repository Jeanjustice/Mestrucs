import streamlit as st
import random
import pandas as pd
from datetime import datetime, timedelta

def generate_phone_number():
    """Génère un numéro de téléphone aléatoire."""
    prefix = random.choice(['06', '07', '01', '02', '03', '04'])
    number = ''.join(random.choices('0123456789', k=8))
    return f"{prefix}{number}"

def generate_event_type():
    """Génère un type d'événement avec des probabilités spécifiées."""
    return random.choices(
        ['SMS', 'CALL', 'MMS'],
        weights=[60, 30, 10],
        k=1
    )[0]

def generate_imsi():
    """Génère un numéro IMSI français aléatoire."""
    return f"208{''.join(random.choices('0123456789', k=10))}"

def generate_imei():
    """Génère un numéro IMEI aléatoire."""
    return ''.join(random.choices('0123456789', k=15))

def convert_to_international_format(phone_number):
    """Convertit un numéro de téléphone en format international avec l'indicatif français."""
    return f"33{phone_number[1:]}"  # Retire le premier 0

def generate_traffic_data(tracked_number, num_interlocutors=6, num_events=100):
    """Génère des données de trafic téléphonique."""
    interlocutors = [generate_phone_number() for _ in range(num_interlocutors)]
    data = []

    # Définir le début de l'intervalle de temps
    start_time = datetime.now()

    # Générer l'IMSI et l'IMEI correspondant au numéro suivi
    imsi = generate_imsi()
    imei = generate_imei()

    for i in range(num_events):
        # Créer un horodatage pour chaque événement
        event_time = start_time + timedelta(minutes=i)
        event_time_str = event_time.strftime("%d/%m/%Y-%H:%M:%S")
        
        # Générer le type d'événement
        event_type = generate_event_type()

        # Déterminer si le numéro suivi est appelant ou appelé
        if random.choice([True, False]):
            caller = convert_to_international_format(tracked_number)
            receiver = convert_to_international_format(random.choice(interlocutors))
        else:
            caller = convert_to_international_format(random.choice(interlocutors))
            receiver = convert_to_international_format(tracked_number)

        # 10% de chance d'avoir un IMSI et un IMEI
        if random.random() < 0.1:
            imsi_to_use = imsi
            imei_to_use = imei
        else:
            imsi_to_use = ''
            imei_to_use = ''

        # Ajouter les données au tableau
        data.append([event_type, event_time_str, caller, receiver, imsi_to_use, imei_to_use])

    return data

def create_csv(tracked_number, data):
    """Crée un fichier CSV à partir des données."""
    # Créer un DataFrame avec les en-têtes corrects
    df = pd.DataFrame(data, columns=["Type de données", "Date", "Appelant", "Appelé", "IMSI", "IMEI"])

    # Générer le nom du fichier avec le numéro suivi
    file_name = f"Suivi_du_numero_{convert_to_international_format(tracked_number)}.csv"
    
    # Créer le CSV dans un buffer
    csv_buffer = df.to_csv(index=False)
    
    return file_name, csv_buffer

# Configuration de l'application Streamlit
st.title("Générateur de Trafic Télécom")

if st.button("Générer un trafic télécom"):
    tracked_number = generate_phone_number()
    traffic_data = generate_traffic_data(tracked_number)

    # Créer le CSV avec un nom de fichier dynamique
    file_name, csv_buffer = create_csv(tracked_number, traffic_data)

    # Afficher le numéro suivi en gras
    st.markdown(f"### Suivi de : **{convert_to_international_format(tracked_number)}**")

    # Afficher les données dans un tableau
    st.write(pd.DataFrame(traffic_data, columns=["Type de données", "Date", "Appelant", "Appelé", "IMSI", "IMEI"]))

    # Télécharger le CSV
    st.download_button(
        label="Télécharger le fichier CSV",
        data=csv_buffer,
        file_name=file_name,
        mime='text/csv'
    )
