import streamlit as st

# Titre de l'application
st.title("Comparateur de Listes")

# Entrée des deux listes
list1 = st.text_area("Entrez la première liste (un élément par ligne)")
list2 = st.text_area("Entrez la deuxième liste (un élément par ligne)")

# Fonction pour comparer les listes
def compare_lists(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    
    only_in_list1 = set1 - set2
    only_in_list2 = set2 - set1
    in_both = set1 & set2
    
    return only_in_list1, only_in_list2, in_both

if st.button("Comparer"):
    # Traitement des entrées
    if list1 and list2:
        # Conversion des chaînes de caractères en listes
        list1 = [item.strip() for item in list1.splitlines() if item.strip()]
        list2 = [item.strip() for item in list2.splitlines() if item.strip()]
        
        only_in_list1, only_in_list2, in_both = compare_lists(list1, list2)

        # Affichage des résultats
        st.subheader("Résultats de la comparaison")
        st.write(f"Éléments seulement dans la première liste : {only_in_list1}")
        st.write(f"Éléments seulement dans la deuxième liste : {only_in_list2}")
        st.write(f"Éléments présents dans les deux listes : {in_both}")
    else:
        st.warning("Veuillez entrer des valeurs dans les deux listes.")
