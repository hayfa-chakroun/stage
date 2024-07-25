import os
import pandas as pd
from datetime import datetime

# Lire les noms des applications depuis un fichier Excel
excel_file = 'C:/Users/hayfa/Desktop/MonExcel.xlsx'  # Utilisation de barres obliques
df = pd.read_excel(excel_file, header=None)  # Lire sans en-tête
app_names = df[0].dropna().tolist()  # Lire les noms dans la première colonne

# Chemin vers le dossier 'hayfa'
hayfa_folder = 'C:/Users/hayfa/Desktop/hayfa'  # Remplacez par le chemin de votre dossier

# Obtenir la date actuelle
current_date = datetime.now().strftime('%m%Y')

# Parcourir les noms des applications et vérifier les dossiers dans 'hayfa'
for app_name in app_names:
    app_folder_path = os.path.join(hayfa_folder, app_name)
    if os.path.isdir(app_folder_path):
        new_folder_path = os.path.join(app_folder_path, current_date)
        os.makedirs(new_folder_path, exist_ok=True)
        
        ta_folder_path = os.path.join(new_folder_path, 'TA')
        idm_folder_path = os.path.join(new_folder_path, 'IDM')
        
        os.makedirs(ta_folder_path, exist_ok=True)
        os.makedirs(idm_folder_path, exist_ok=True)

print("Processus terminé.")
