# Importation des bibliothèques nécessaires
import numpy as np
import matplotlib.pyplot as plt

# Génération de données aléatoires
x = np.linspace(0, 10, 100)
y = np.sin(x) + np.random.randn(100) * 0.1

# Création du graphique
plt.figure(figsize=(8, 5))
plt.plot(x, y, label='Données aléatoires', color='blue')
plt.title('Graphique des données aléatoires')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)

# Affichage du graphique
plt.show()
