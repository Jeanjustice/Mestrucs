import streamlit as st
import pandas as pd

def analyze_contacts(file):
    # Lire le fichier CSV
    df = pd.read_csv(file)

    # Identification du numéro suivi (première entrée dans la colonne "Appelant")
    numero_suivi = df["Appelant"].iloc[0]

    # Extraire l'IMSI et l'IMEI du numéro suivi, suppression des NaN et conversion en string sans décimales
    imsi = df.loc[df["Appelant"] == numero_suivi, "IMSI"].dropna().unique()
    imei = df.loc[df["Appelant"] == numero_suivi, "IMEI"].dropna().unique()
    imsi = [str(int(imsi[0]))] if len(imsi) > 0 else ["Non disponible"]
    imei = [str(int(imei[0]))] if len(imei) > 0 else ["Non disponible"]

    # Compter les occurrences pour chaque contact et les types de données
    contact_count = df.groupby(["Appelant", "Type de données"]).size().unstack(fill_value=0) + \
                    df.groupby(["Appelé", "Type de données"]).size().unstack(fill_value=0)
    contact_count = contact_count.fillna(0).astype(int)

    # Construire la liste des contacts avec comptage par type de données
    contact_list = []
    for contact, row in contact_count.iterrows():
        sms_count = row.get('SMS', 0)
        call_count = row.get('CALL', 0)
        mms_count = row.get('MMS', 0)
        counts = []
        if sms_count > 0:
            counts.append(f"{sms_count} SMS")
        if call_count > 0:
            counts.append(f"{call_count} CALL")
        if mms_count > 0:
            counts.append(f"{mms_count} MMS")
        contact_list.append(f"{contact} ({', '.join(counts)})")

    # Afficher les résultats dans l'application Streamlit
    st.write(f"Liste de contacts pour le numéro suivi : {numero_suivi}")
    st.write(f"IMSI : {imsi[0]}")
    st.write(f"IMEI : {imei[0]}")
    st.write("Contacts :")
    for contact in contact_list:
        st.write(contact)

    # Télécharger la liste de contacts au format texte
    contacts_txt = f"Liste de contacts pour le numéro suivi : {numero_suivi}\n\n"
    contacts_txt += f"IMSI : {imsi[0]}\n"
    contacts_txt += f"IMEI : {imei[0]}\n\n"
    contacts_txt += "Contacts :\n" + "\n".join(contact_list)

    st.download_button(
        label="Télécharger la liste de contacts (.txt)",
        data=contacts_txt,
        file_name='contacts_list.txt',
        mime='text/plain'
    )

# Interface de l'application Streamlit
st.title("Analyseur de Liste de Contacts")

uploaded_file = st.file_uploader("Choisir un fichier CSV", type="csv")
if uploaded_file is not None:
    analyze_contacts(uploaded_file)
