import os
import shutil
import pandas as pd
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/process-files', methods=['POST'])
def process_files():
    try:
        hayfa_folder = request.form['hayfa_folder']
        downloads_folder = request.form['downloads_folder']

        os.makedirs(hayfa_folder, exist_ok=True)
        current_date = datetime.now().strftime('%m%Y')

        missing_folders = []  # Liste pour stocker les applications sans dossier correspondant

        # Lire les noms des applications depuis un fichier Excel
        excel_file = request.files.get('excel_file')  # Fichier Excel téléchargé

        if not excel_file:
            return jsonify({"status": "failure", "message": "Aucun fichier Excel téléchargé."})

        df = pd.read_excel(excel_file, header=None)  # Lire sans en-tête

        if df.empty:
            return jsonify({"status": "failure", "message": "Le fichier Excel est vide ou n'a pas pu être lu."})

        app_names = df[0].dropna().tolist()

        for app_name in app_names:
            clean_app_name = app_name.strip().replace(" ", "_")
            app_folder_path = os.path.join(hayfa_folder, clean_app_name)
            
            if os.path.exists(app_folder_path):
                new_folder_path = os.path.join(app_folder_path, current_date)
                
                try:
                    os.makedirs(new_folder_path, exist_ok=True)
                    
                    ta_folder_path = os.path.join(new_folder_path, 'TA')
                    idm_folder_path = os.path.join(new_folder_path, 'IDM')
                    
                    os.makedirs(ta_folder_path, exist_ok=True)
                    os.makedirs(idm_folder_path, exist_ok=True)

                    # Recherche des fichiers avec l'horodatage
                    found_assignment = False
                    found_account = False
                    
                    for file_name in os.listdir(downloads_folder):
                        if file_name.startswith(f"Recon_CurrentAssignmentsFile_{clean_app_name}_") and file_name.endswith(".csv"):
                            shutil.copy(os.path.join(downloads_folder, file_name), ta_folder_path)
                            found_assignment = True
                        elif file_name.startswith(f"Recon_CurrentAccountFile_{clean_app_name}_") and file_name.endswith(".csv"):
                            shutil.copy(os.path.join(downloads_folder, file_name), idm_folder_path)
                            found_account = True
                    
                    if not found_assignment or not found_account:
                        return jsonify({"status": "failure", "message": "Fichiers non trouvés."})
                
                except Exception as e:
                    return jsonify({"status": "failure", "message": str(e)})

            else:
                # Ajouter le nom de l'application à la liste des dossiers manquants
                missing_folders.append(clean_app_name)

        success_message = "Processus terminé."
        if missing_folders:
            success_message += f" les dossiers pour les applications suivantes sont manquants : {', '.join(missing_folders)}."

        return jsonify({"status": "success", "message": success_message})
    
    except Exception as e:
        return jsonify({"status": "failure", "message": str(e)})

@app.route('/process-excel', methods=['POST'])
def process_excel():
    try:
        excel_file = request.files.get('excel_file')  # Fichier Excel téléchargé

        if not excel_file:
            return jsonify({"status": "failure", "message": "Aucun fichier Excel téléchargé."})

        df = pd.read_excel(excel_file, header=None)  # Lire sans en-tête

        if df.empty:
            return jsonify({"status": "failure", "message": "Le fichier Excel est vide ou n'a pas pu être lu."})

        account_names = []
        applications = []
        disabled_status = []

        status_list = ['disabled', 'enabled']
        max_account_length = 20

        for row in df.itertuples(index=False):
            account_name_found = False
            for cell in row:
                cell_str = str(cell).strip().lower()

                if cell_str in status_list:
                    disabled_status.append(cell_str)
                elif len(cell_str) <= max_account_length and (' ' in cell_str or cell_str.isalpha()):
                    if not account_name_found:
                        account_names.append(cell_str)
                        account_name_found = True
                    else:
                        applications.append(cell_str)
                else:
                    applications.append(cell_str)

            if not account_name_found:
                account_names.append('')
            if len(applications) < len(account_names):
                applications.append('')

        max_length = max(len(account_names), len(applications), len(disabled_status))
        account_names.extend([''] * (max_length - len(account_names)))
        applications.extend([''] * (max_length - len(applications)))
        disabled_status.extend([''] * (max_length - len(disabled_status)))

        data = {
            'Account name': account_names,
            'Disabled Status': disabled_status,
            'Application': applications
        }
        new_df = pd.DataFrame(data)

        output_dir = 'static'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        output_path = os.path.join(output_dir, 'formatted_idm_file.xlsx')
        new_df.to_excel(output_path, index=False)

        return jsonify({"status": "success", "message": f"Fichier transformé enregistré à {output_path}", "file_url": f"/static/formatted_idm_file.xlsx"})
    except Exception as e:
        print("Erreur rencontrée:", str(e))
        return jsonify({"status": "failure", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
