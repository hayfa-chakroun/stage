import pytesseract
from PIL import Image
import openpyxl

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
