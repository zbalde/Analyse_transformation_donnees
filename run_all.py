"""Installe les dépendances, télécharge les données et exécute les 4 notebooks dans l'ordre."""
import subprocess
import sys

print("Installation des dépendances...")
subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

print("Téléchargement des données...")
subprocess.run([sys.executable, "download_data.py"], check=True)

notebooks = [
    "jour_1_analyse.ipynb",
    "jour_2_types_nettoyage.ipynb",
    "jour_3_transformation_statistiques.ipynb",
    "jour_4_analyse.ipynb",
]

for nb in notebooks:
    print(f"Exécution de {nb}...")
    subprocess.run([
        sys.executable, "-m", "jupyter", "nbconvert",
        "--to", "notebook", "--execute", "--inplace", nb,
    ], check=True)

print("Terminé : toutes les étapes ont été exécutées dans l'ordre.")
