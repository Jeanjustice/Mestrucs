import streamlit as st
import requests
import pandas as pd

def check_tor_relay(ip_address):
    url = f"https://onionoo.torproject.org/summary?search={ip_address}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        if data['relays']:
            # Récupération des détails des relais
            relays_info = []
            for relay in data['relays']:
                relays_info.append({
                    'Nom': relay['n'],
                    'Fingerprint': relay['f'],
                    'Adresses': ', '.join(relay['a']),
                })
            return relays_info  # Retourne la liste des relais
        else:
            return None  # Indique qu'aucun relais n'a été trouvé
    else:
        return [{'Nom': 'Erreur', 'Fingerprint': 'Erreur', 'Adresses': f"Erreur lors de la requête: {response.status_code}"}]

# Interface Streamlit
st.title("Vérificateur de nœuds Tor")
st.write("Téléchargez un fichier texte contenant des adresses IP ou collez-les ci-dessous.")

# Champ de texte pour coller les adresses IP
ip_input = st.text_area("Adresses IP (une par ligne) :")

# Ou drag and drop pour un fichier
uploaded_file = st.file_uploader("Ou téléchargez un fichier contenant des adresses IP", type=["txt"])

if uploaded_file is not None:
    ip_input = uploaded_file.read().decode("utf-8")

# Vérification des IPs
if ip_input:
    ip_list = ip_input.strip().split('\n')
    results = []
    negative_results = []  # Liste pour stocker les résultats négatifs

    for ip in ip_list:
        ip = ip.strip()
        if ip:  # Vérifie que la ligne n'est pas vide
            result = check_tor_relay(ip)
            if result is None:
                negative_results.append(f"L'IP {ip} n'est pas un nœud Tor actuellement.")
            else:
                results.extend(result)  # Ajoute les résultats positifs

    # Convertit les résultats positifs en DataFrame pour affichage
    results_df = pd.DataFrame(results) if results else pd.DataFrame(columns=['Nom', 'Fingerprint', 'Adresses'])
    
    st.write("### Résultats positifs de vérification :")
    st.dataframe(results_df)  # Affiche le tableau avec les résultats positifs
    
    # Affichage des résultats négatifs
    if negative_results:
        st.write("### Résultats négatifs :")
        for neg_res in negative_results:
            st.write(neg_res)
