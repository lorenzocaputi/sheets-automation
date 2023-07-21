# PROGRAMMA PER REALIZZARE FILE GOOGLE SHEETS PER UNA NICCHIA, CAMBIANDONE ALCUNI VALORI
# IN QUESTO ESEMPIO IL TREND E' "I LIKE X, Y AND MAYBE 3 PEOPLE"
# PROVA A INSERIRE LA MAIL DEL TUO ACCOUNT GOOGLE E TI VERRA' MANDATO IL FILE CSV


from oauth2client.service_account import ServiceAccountCredentials
import gspread

scope = ["https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('../sheetsAPI.json', scopes=scope)
client = gspread.authorize(creds)


GOOGLE_ACCOUNT = "lorenzo.caputi@liceotasso.edu.it"


# define basic variables
# list names: hobbies, jobs, years, drinks
niche = 'i like cats and maybe 3 people'
broad_niche = 'cats'
list_name = 'hobbies'
broad_tags = []
specific_tags = []

# ----------------------- APOD SPREADSHEET
# create a spreadsheet
sh = client.create(f'AUTOMATION.{niche}')
sh.share(GOOGLE_ACCOUNT, perm_type='user', role='writer')
sh_APOD = sh.sheet1

# 1st row
apod_first_row = ['VAR1', 'File Name']
sh_APOD.append_row(apod_first_row)

# other 60 rows
list_sh = client.open('POD-lists').worksheet(list_name)
val_list = list_sh.get_all_values()
for row in val_list:
    row.append(row[0] + ' ' + niche)

sh_APOD.append_rows(val_list)


# ------------------------- FLYING UPLOAD SPREADSHEET

# adding a worksheet
sh_FU = client.open(f'AUTOMATION.{niche}').add_worksheet('FU', 1000, 1000)

# first row
fu_first_row = ['Image Path', 'Language', 'Title', 'Description', 'Tags', 'Type', 'Color']
sh_FU.append_row(fu_first_row)

# other 60 lines

# define list variables
file_name = sh_APOD.get_values('b2:b61')
var1 = sh_APOD.get_values('a2:a61')
standard_descr = f'funny {broad_niche} shirt. Perfect birthday gift for dad, grandpa or a good friend.'

# define single line list and repeat x60
l = []
for x in range(60):
    a = [file_name[x][0] + '.png', 'EN', f'{niche} funny {var1[x][0]}',
         f'{var1[x][0]} {standard_descr}', 'WEB SCRAPING', 'man, woman youth', 'black']
    l.append(a)

sh_FU.append_rows(l)
