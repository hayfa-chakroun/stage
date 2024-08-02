import pandas as pd

# Charger le fichier Excel
file_path = r'C:\Users\hayfa\Desktop\pip.xlsx'  # remplacez par le chemin de votre fichier
df = pd.read_excel(file_path, header=None)

# Initialiser les listes pour les nouvelles colonnes
account_names = []
applications = []
disabled_status = []

# Parcourir les données pour les trier dans les bonnes colonnes
for row in df.itertuples(index=False):
    for cell in row:
        cell_str = str(cell).lower()  # Convertir en minuscules pour faciliter la comparaison
        if cell_str in ['disabled', 'enabled']:
            disabled_status.append(cell)
        elif cell_str in [ 'Facebook', 'Instagram', 'Snapchat', 'Twitter', 'TikTok', 'LinkedIn', 'Pinterest', 'Reddit', 'Tumblr', 'Quora',
    'WhatsApp', 'Telegram', 'Messenger', 'WeChat', 'Viber', 'Line', 'Signal', 'Skype', 'KakaoTalk', 'Discord',
    'Microsoft Word', 'Microsoft Excel', 'Microsoft PowerPoint', 'Outlook', 'Google Docs', 'Google Sheets', 'Google Slides', 'Gmail',
    'Slack', 'Trello', 'Asana', 'Notion', 'Evernote', 'OneNote', 'Dropbox', 'Todoist',
    'YouTube', 'Netflix', 'Hulu', 'Spotify', 'Amazon Prime Video', 'Disney+', 'HBO Max', 'Apple Music', 'SoundCloud', 'Twitch',
    'Amazon', 'eBay', 'Alibaba', 'AliExpress', 'Etsy', 'Shopify', 'Walmart', 'Rakuten', 'JD.com', 'Taobao',
    'PayPal', 'Venmo', 'Cash App', 'Robinhood', 'Revolut', 'Square', 'Mint', 'Acorns', 'Coinbase', 'Binance',
    'MyFitnessPal', 'Fitbit', 'Strava', 'Nike Training Club', 'Peloton', 'Garmin Connect', 'Headspace', 'Calm', 'Apple Health', 'Google Fit',
    'Uber', 'Lyft', 'Airbnb', 'Booking.com', 'Expedia', 'TripAdvisor', 'Skyscanner', 'Google Maps', 'Waze', 'Hopper',
    'BBC News', 'CNN', 'The New York Times', 'The Guardian', 'Reuters', 'Bloomberg', 'Al Jazeera', 'Fox News', 'NPR', 'The Washington Post',
    'Uber Eats', 'DoorDash', 'Grubhub', 'Deliveroo', 'Postmates', 'Just Eat', 'Zomato', 'Yelp', 'OpenTable', 'Starbucks']:  # Ajoutez toutes les applications que vous voulez reconnaître
            applications.append(cell)
        else:
            account_names.append(cell)

# Assurer que les colonnes ont la même longueur
max_length = max(len(account_names), len(applications), len(disabled_status))
account_names.extend([''] * (max_length - len(account_names)))
applications.extend([''] * (max_length - len(applications)))
disabled_status.extend([''] * (max_length - len(disabled_status)))

# Créer un nouveau DataFrame avec la structure souhaitée
data = {
    'Account name': account_names,
    'disabled': disabled_status,
    'application': applications
}
new_df = pd.DataFrame(data)

# Sauvegarder le nouveau DataFrame dans un fichier Excel
output_path = r'C:\Users\hayfa\formatted_idm_file.xlsx'  # remplacez par le chemin de votre fichier de sortie
new_df.to_excel(output_path, index=False)

print(f'Transformed file saved to {output_path}')
