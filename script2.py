import pytesseract
from PIL import Image
import openpyxl
import pandas as pd

# Chemin vers l'exécutable Tesseract (modifie-le si nécessaire)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Fonction pour extraire le texte d'une image
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

# Fonction pour écrire le texte dans un fichier Excel
def write_text_to_excel(text, excel_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Texte extrait"
    
    # Diviser le texte en lignes et les écrire dans des cellules
    for i, line in enumerate(text.split('\n')):
        ws.cell(row=i+1, column=1, value=line)
    
    wb.save(excel_path)

# Chemin de l'image à traiter
image_path = 'C:\\Users\\hayfa\\Desktop\\mine.jpg'

# Chemin du fichier Excel de sortie
excel_path = 'C:\\Users\\hayfa\\Desktop\\MonExcel.xlsx'

# Extraire le texte de l'image
text = extract_text_from_image(image_path)

# Écrire le texte dans le fichier Excel
write_text_to_excel(text, excel_path)

print(f"Le texte a été extrait et sauvegardé dans {excel_path}") 
# *********************************************     Excel>>>>Excel IDM(fichier personnalisé) ************************************************************* #

# Lire le fichier Excel aléatoire
input_file = 'C:\Users\hayfa\myenv\Lib\site-packages\numpy\random'
df = pd.read_excel(input_file)

df.columns = ['Account Name ', 'Account Disabled', 'Application']
df.columns = ['Account Name ', 'Entitlement Disabled', 'Application']


# Ajouter des colonnes nécessaires pour le format IDM
df['IDM_Metadata'] = 'Example Metadata'

# Écrire le fichier formaté en utilisant openpyxl
output_file = 'formatted_idm_file.xlsx'
df.to_excel(output_file, index=False, engine='openpyxl')

# Appliquer un formatage spécifique
workbook = openpyxl.load_workbook(output_file)
worksheet = workbook.active

# Appliquer des styles spécifiques
for cell in worksheet[1]:
    cell.font = openpyxl.styles.Font(bold=True)

# Sauvegarder le fichier avec les styles appliqués
workbook.save(output_file)

print(f"Le fichier {output_file} a été créé avec succès.")
