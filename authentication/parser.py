
import pandas as pd
from collections import defaultdict
import pyodbc

df = 'latest_file.xlsx'
cols = pd.read_excel(df, usecols="O:CK")
num_cols = []
for col in cols:
    num_cols.append(col)
print(num_cols)
record_main_cols_temp = []
record_main = cols = pd.read_excel(df)
for col in record_main.columns:
    if col not in num_cols:
        record_main_cols_temp.append(col)
print('records main cols main',record_main_cols_temp)

conn = pyodbc.connect(
        'Driver= {ODBC Driver 17 for SQL Server};SERVER=UL-ARC1003-1416;DATABASE=TradeDB;UID=project_user;PWD=project_password;Trusted_Connection=yes;')
cursor = conn.cursor()
last_record_id = "SELECT TOP 1 RecordID FROM test.record_main ORDER BY RecordID DESC;"
cursor.execute(last_record_id)
last_row = cursor.fetchall()[0][0]
print(last_row)
conn.commit()

# ----------Working solution of Trashitem Table -------------------------
trash_number_of_cols = defaultdict(list)
trash_item = ["trashitem_id", "recordid", "material_category", "material_group", "itemcount"]
for col in num_cols:
    if "Total" not in col:
        col = col.split("-")
        a, b = col[0], col[1]
        a = a.split(",")
        b = b.strip()
        for i in a:
            i = i.strip()
            if len(i) > 1:
                trash_number_of_cols[b].append(i)

print('trash no of cols',trash_number_of_cols)
maintain_record_id = []

new_df = pd.read_excel("latest_file.xlsx")
final_list = []
trash_row = new_df[num_cols]
count = 0
for num in num_cols:
    if "Total" not in num:
        index = 1
        for ind in new_df.index:
            if new_df[num][ind] > 0:
                print(str(index + 1) + "-----", num)
                print(new_df[num][ind])
                count += 1
                print([count, index + last_row, num, str(new_df[num][ind])])
                final_list.append([count, index + last_row, num, int(new_df[num][ind])])
            index += 1
    maintain_record_id.append(1 + last_row)
    print("\n")

print('final list',final_list)

trash_final_list = []
for trashid, record, material, count in final_list:
    material = material.split("-")
    trash_final_list.append((record, material[0].strip(), material[1].strip(), count))

print('trash final list',trash_final_list)

print(type(trash_final_list))

'''connection = pyodbc.connect(
    'Driver= {ODBC Driver 17 for SQL Server};SERVER=UL-ARC1003-1416;DATABASE=TradeDB;UID=project_user;PWD=project_password;Trusted_Connection=yes;')
cursor = connection.cursor()

mySql_insert_query = "INSERT INTO test.record_trashitem(recordid, material_category, material_group, itemcount) VALUES (?, ?,?,?)"
for i in trash_final_list:
    cursor.execute(mySql_insert_query, i)
connection.commit()'''
# print(cursor.rowcount, "Record inserted successfully into record_trashtable")

new_record__df = pd.read_excel('latest_file.xlsx')
new_record__df.fillna("", inplace=True)
default_dict_record_main = defaultdict(list)
record_main_df = new_record__df[record_main_cols_temp]
count = 0
total_records = record_main_df[record_main_cols_temp[0]].size
record_main = [[last_row + i] for i in range(1, total_records + 1)]
record_main_df['Date'] = record_main_df['Date'].astype(str)
record_main_df['CreationDate'] = record_main_df['CreationDate'].astype(str)
record_main_df['EditDate'] = record_main_df['EditDate'].astype(str)

for row in record_main_cols_temp:
    index = 0
    for ind in record_main_df:
        count += 1
        for i in range(total_records):
            curr_value = record_main_df[row][i]
            print(curr_value)
            if row == "ObjectID":
                curr_value = int(curr_value) + 1
                # record_main_df[row][index] += 1
            elif row == "GlobalID":
                if curr_value:
                    curr_value = str(curr_value)
                else:
                    curr_value = ""
            elif row == "Username":
                if curr_value:
                    curr_value = str(curr_value)
                else:
                    curr_value = ""
            elif row == "Password":
                if curr_value:
                    curr_value = str(curr_value)
                else:
                    curr_value = ""
            elif row == "What is your name?":
                if curr_value:
                    curr_value = str(curr_value)
                else:
                    curr_value = ""
            elif row == "Permittee Name":
                if curr_value:
                    curr_value = str(curr_value)
                else:
                    curr_value = ""
            elif row == "Priority Land Uses (PLUs) or Equivalent Alternate Land Uses":
                if curr_value:
                    curr_value = str(curr_value)
                else:
                    curr_value = ""
            elif row == "Do you have the required Personal Protection Equipment?":
                if curr_value:
                    curr_value = str(curr_value)
                else:
                    curr_value = ""
            elif row == "Survey Primary Location (Pick One):":
                if curr_value:
                    curr_value = str(curr_value)
                else:
                    curr_value = ""
            elif row == "What is the litter assessment (Pick One)?":
                if curr_value:
                    curr_value = int(curr_value)
                else:
                    curr_value = 0
            elif row == "Location Name and City/County":
                if curr_value:
                    curr_value = str(curr_value)
                else:
                    curr_value = ""
            elif row == "Surrounding Land Use (Mark All Applicable)":
                if curr_value:
                    curr_value = str(curr_value)
                else:
                    curr_value = ""
            elif row == "Creek Conditions":
                if curr_value:
                    curr_value = str(curr_value)
                else:
                    curr_value = ""
            elif row == "Site Survey (Check All Applicable):":
                if curr_value:
                    curr_value = str(curr_value)
                else:
                    curr_value = ""
            elif row == "Number of Volunteers":
                if curr_value:
                    curr_value = int(curr_value)
                else:
                    curr_value = 0
            elif row == "Total number bags filled":
                if curr_value:
                    curr_value = int(curr_value)
                else:
                    curr_value = 0
            elif row == "Approximate weight of trash (excluding bulky items):":
                if curr_value:
                    curr_value = str(curr_value)
                else:
                    curr_value = 0
            elif row == "Homeless Camps Encountered (Pick One)?":
                if curr_value:
                    curr_value = str(curr_value)
                else:
                    curr_value = ""
            elif row == "Illegal Dumpsite (Pick One)?":
                if curr_value:
                    curr_value = str(curr_value)
                else:
                    curr_value = ""
            elif row == "Notes about site":
                if curr_value:
                    curr_value = str(curr_value)
                else:
                    curr_value = ""
            elif row == "Date":
                if curr_value:
                    curr_value = str(curr_value)
                else:
                    curr_value = ""
            elif row == "CreationDate":
                if curr_value:
                    curr_value = str(curr_value)
                else:
                    curr_value = ""
            elif row == "Creator":
                if curr_value:
                    curr_value = str(curr_value)
                else:
                    curr_value = ""
            elif row == "EditDate":
                if curr_value:
                    curr_value = str(curr_value)
                else:
                    curr_value = ""
            elif row == "Editor":
                if curr_value:
                    curr_value = str(curr_value)
                else:
                    curr_value = ""
            elif row == "CreationDate":
                if curr_value:
                    curr_value = str(curr_value)
                else:
                    curr_value = ""
            elif row == "Watch the Training Video":
                continue
            if row == "x":
                if curr_value:
                    curr_value = float(curr_value)
                else:
                    curr_value = 0
            if row == "y":
                if curr_value:
                    curr_value = float(curr_value)
                else:
                    curr_value = 0
            record_main[i].append(curr_value)
        break
    index += 1
    print("\n")

print('record main',record_main)
print("Now create tuple")
final_record_main_list = []
for d0, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, d16, d17, d18, d19, d20, d21, d22, d23, d24, d25, d26, d27 in record_main:
    final_record_main_list.append((d0, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, d16, d17, d18,
                                   d19, d20, d21, d22, d23, d24, d25, d26, d27))

print('final',final_record_main_list)
print(type(final_record_main_list))
'''
connection = pyodbc.connect(
        'Driver= {ODBC Driver 17 for SQL Server};SERVER=UL-ARC1003-1416;DATABASE=TradeDB;UID=project_user;PWD=project_password;Trusted_Connection=yes;')
cursor = connection.cursor()
record_main_query = "INSERT INTO test.record_main(RecordID, ObjectID, GlobalID, Username, Password, Name, permittee, plu, assessment, surveyLocation, LitterAssessment, location_name, Surrounding_Land_Use, Creek_Conditions, Site_Survey, Child_Volunteers_count, total_number_bags_filled, weight_of_trash, homeless_camps_encountered, illegal_dumpsite, notes_about_site, display_date, Creation_date, Creator, Edit_date, Editor, x_value, y_value) VALUES (?,?,?, ?, ?, ?,?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?)"
print(record_main_query)
for i in final_record_main_list:
    cursor.execute(record_main_query, i)
connection.commit()
print(cursor.rowcount, "Record inserted successfully into record_trashtable")'''

