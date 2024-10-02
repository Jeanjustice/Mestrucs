import streamlit as st
import pandas as pd

def create_contact_list(df, tracked_number):
    """Crée une liste de contacts à partir du DataFrame."""
    imsi = df['IMSI'].dropna().unique()
    imei = df['IMEI'].dropna().unique()
    
    contact_counts = pd.concat([df['Appelant'], df['Appelé']]).value_counts()

    contact_list = []
    contact_list.append(f"Liste de contacts de {tracked_number}")
    
    if imsi.size > 0:
        contact_list.append(f"IMSI : {imsi[0]}")
    if imei.size > 0:
        contact_list.append(f"IMEI : {imei[0]}")

    contact_list.append("\nContacts :")
    for contact, count in contact_counts.items():
        contact_list.append(f"{contact} ({count})")

    return "\n".join(contact_list)

# Configuration de l'application Streamlit
st.title("Analyse de Trafic Télécom")

# Téléchargement du fichier CSV
uploaded_file = st.file_uploader("Téléchargez un fichier CSV", type=["csv"], label_visibility="collapsed")

if uploaded_file is not None:
    # Lire le fichier CSV
    df = pd.read_csv(uploaded_file)

    # Vérifier les colonnes nécessaires
    required_columns = {'Appelant', 'Appelé', 'IMSI', 'IMEI'}
    if required_columns.issubset(df.columns):
        # Extraire le numéro suivi (on suppose qu'il est toujours le même)
        tracked_number = df.iloc[0]['Appelant']  # On peut changer cette logique si nécessaire

        # Créer la liste de contacts
        contact_list = create_contact_list(df, tracked_number)

        # Afficher la liste de contacts dans l'application
        st.text_area("Liste des Contacts", value=contact_list, height=300)

        # Option pour télécharger la liste des contacts
        st.download_button(
            label="Télécharger la liste des contacts",
            data=contact_list,
            file_name='contacts_list.txt',
            mime='text/plain'
        )
    else:
        st.error("Le fichier CSV doit contenir les colonnes : Appelant, Appelé, IMSI, IMEI.")
else:
    st.info("Veuillez télécharger un fichier CSV pour commencer.")
