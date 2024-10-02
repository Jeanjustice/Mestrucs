import streamlit as st
import pandas as pd

def clean_column_names(df):
    """Nettoie les noms des colonnes en supprimant les espaces et les accents."""
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.normalize('NFD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    return df

def process_contact_list(csv_file):
    # Lire le fichier CSV et nettoyer les noms des colonnes
    df = pd.read_csv(csv_file)
    df = clean_column_names(df)

    # Vérifier que les colonnes nécessaires existent
    required_columns = ['Type_de_donnees', 'Appelant', 'Appele', 'IMSI', 'IMEI']
    if not all(col in df.columns for col in required_columns):
        st.error("Le fichier CSV ne contient pas les colonnes requises.")
        return

    # Extraire le numéro suivi
    tracked_number = df['Appelant'].iloc[0] if df['Appelant'].iloc[0].startswith('33') else df['Appele'].iloc[0]

    # Extraire l'IMSI et l'IMEI du numéro suivi
    imsi = df.loc[df['Appelant'] == tracked_number, 'IMSI'].dropna().unique()
    imei = df.loc[df['Appelant'] == tracked_number, 'IMEI'].dropna().unique()
    
    imsi = imsi[0] if len(imsi) > 0 else "IMSI non disponible"
    imei = imei[0] if len(imei) > 0 else "IMEI non disponible"

    # Remplir la section "Total des échanges"
    total_exchanges = df[(df['Appelant'] == tracked_number) | (df['Appele'] == tracked_number)]
    total_count = len(total_exchanges)
    
    total_sms = len(total_exchanges[total_exchanges['Type_de_donnees'] == 'SMS'])
    total_call = len(total_exchanges[total_exchanges['Type_de_donnees'] == 'CALL'])
    total_mms = len(total_exchanges[total_exchanges['Type_de_donnees'] == 'MMS'])

    # Création du dictionnaire de contacts
    contacts = {}
    for index, row in df.iterrows():
        if row['Appelant'] == tracked_number:
            contact_number = row['Appele']
        elif row['Appele'] == tracked_number:
            contact_number = row['Appelant']
        else:
            continue

        if contact_number not in contacts:
            contacts[contact_number] = {'count': 0, 'SMS': 0, 'CALL': 0, 'MMS': 0}

        contacts[contact_number]['count'] += 1
        contacts[contact_number][row['Type_de_donnees']] += 1

    # Générer la sortie textuelle
    result = f"Liste de contacts pour le numéro suivi : {tracked_number}\n\n"
    result += f"IMSI : {int(imsi)}\nIMEI : {int(imei)}\n\n"
    result += f"Total des échanges : {total_count} ( {total_sms} SMS, {total_call} CALL, {total_mms} MMS )\n\n"
    result += "Contacts :\n"

    for contact, details in contacts.items():
        result += f"{contact} ({details['count']} fois : {details['SMS']} SMS, {details['CALL']} CALL, {details['MMS']} MMS)\n"

    return result

# Application Streamlit
st.title("Analyseur de liste de contacts")

uploaded_file = st.file_uploader("Choisir un fichier CSV", type="csv")

if uploaded_file is not None:
    contact_list_text = process_contact_list(uploaded_file)

    # Afficher la liste des contacts analysée
    st.text_area("Résultats de l'analyse", value=contact_list_text, height=300)

    # Option de téléchargement du fichier texte
    st.download_button(
        label="Télécharger la liste de contacts",
        data=contact_list_text,
        file_name='contact_list.txt',
        mime='text/plain'
    )
