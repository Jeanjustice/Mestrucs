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
    for number in generated_numbers:
        st.write(number)
