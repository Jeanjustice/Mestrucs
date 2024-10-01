import streamlit as st
import random

def generate_phone_numbers(num=50):
    phone_numbers = []
    for _ in range(num):
        prefix = random.choice(['06', '07'])
        number = ''.join(random.choices('0123456789', k=8))
        phone_number = f"{prefix}{number}"
        phone_numbers.append(phone_number)
    return phone_numbers

# Configuration de l'application Streamlit
st.title("Générateur de Numéros de Téléphone")

if st.button("Générer des Numéros de Téléphone"):
    generated_numbers = generate_phone_numbers()
    st.write("### Numéros générés :")
    
    # Créer une chaîne de caractères pour le text area avec colonnes
    num_columns = 5
    column_lines = []
    
    # Créer des lignes pour chaque numéro dans les colonnes
    for i in range(0, len(generated_numbers), num_columns):
        line = "\t".join(generated_numbers[i:i + num_columns])  # Utiliser tabulation pour séparer les colonnes
        column_lines.append(line)
    
    # Convertir la liste de lignes en une chaîne de caractères
    formatted_numbers = "\n".join(column_lines)
    
    # Afficher les numéros dans un text area pour le copier
    st.text_area("Numéros générés (vous pouvez copier ici)", formatted_numbers, height=300)

    # Bouton de téléchargement pour télécharger les numéros
    st.download_button(
        label="Télécharger les numéros",
        data="\n".join(generated_numbers),  # Télécharger sans colonnes
        file_name='numeros_telephone.txt',
        mime='text/plain'
    )
