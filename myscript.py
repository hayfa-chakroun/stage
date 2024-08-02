import os
import shutil
import pandas as pd
from datetime import datetime

# Lire les noms des applications depuis un fichier Excel
excel_file = r'C:\Users\hayfa\Desktop\MonExcel1.xlsx'
df = pd.read_excel(excel_file, header=None)  # Lire sans en-tête
app_names = df[0].dropna().tolist()  # Lire les noms dans la première colonne

# Chemin vers le dossier 'hayfa'
hayfa_folder = r'C:\Users\hayfa\Desktop\hayfa'  # Remplacez par le chemin de votre dossier
downloads_folder = r'C:\Users\hayfa\Desktop\Downloads'  # Dossier des téléchargements

# Assurez-vous que le dossier de base existe
os.makedirs(hayfa_folder, exist_ok=True)

# Obtenir la date actuelle
current_date = datetime.now().strftime('%m%Y')

# Parcourir les noms des applications et vérifier les dossiers dans 'hayfa'
for app_name in app_names:
    # Nettoyer le nom de l'application pour éviter les problèmes
    clean_app_name = app_name.strip().replace(" ", "_")
    app_folder_path = os.path.join(hayfa_folder, clean_app_name)
    
    # Imprimer les chemins pour vérifier
    print(f"Chemin du dossier de l'application : {app_folder_path}")

    if os.path.exists(app_folder_path):
        new_folder_path = os.path.join(app_folder_path, current_date)
        print(f"Chemin du nouveau dossier : {new_folder_path}")

        try:
            os.makedirs(new_folder_path, exist_ok=True)
            print(f"Dossier créé ou déjà existant : {new_folder_path}")
        except Exception as e:
            print(f"Erreur lors de la création du dossier {new_folder_path}: {e}")
        
        ta_folder_path = os.path.join(new_folder_path, 'TA')
        idm_folder_path = os.path.join(new_folder_path, 'IDM')
        
        try:
            os.makedirs(ta_folder_path, exist_ok=True)
            os.makedirs(idm_folder_path, exist_ok=True)
            print(f"Dossiers TA et IDM créés ou déjà existants")
        except Exception as e:
            print(f"Erreur lors de la création des dossiers TA ou IDM : {e}")
        
        # Recherche des fichiers dans le dossier des téléchargements
        assignment_file_pattern = f"Recon_CurrentAssignmentsFile_{clean_app_name}_{current_date}.csv"
        account_file_pattern = f"Recon_CurrentAccountFile_{clean_app_name}_{current_date}.csv"
        
        print(f"Recherche des fichiers pour {clean_app_name}...")
        found_assignment = False
        found_account = False
        
        for file_name in os.listdir(downloads_folder):
            if assignment_file_pattern in file_name:
                shutil.copy(os.path.join(downloads_folder, file_name), ta_folder_path)
                found_assignment = True
                print(f"Fichier {file_name} copié dans {ta_folder_path}")
            elif account_file_pattern in file_name:
                shutil.copy(os.path.join(downloads_folder, file_name), idm_folder_path)
                found_account = True
                print(f"Fichier {file_name} copié dans {idm_folder_path}")
        
        if not found_assignment:
            print(f"Aucun fichier trouvé pour le modèle {assignment_file_pattern}")
        if not found_account:
            print(f"Aucun fichier trouvé pour le modèle {account_file_pattern}")
    else:
        print(f"Le dossier {app_folder_path} n'existe pas.")

print("Processus terminé.")
