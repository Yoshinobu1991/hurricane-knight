import pandas as pd
import sys

file_path = r"c:\Users\Admir\Desktop\Project\Hurricane Knight\2026颶風騎士收支明細費用表.xlsx"

try:
    xls = pd.ExcelFile(file_path)
    print('Sheets:', xls.sheet_names)
    print('====================')
    for sheet in xls.sheet_names:
        print('Sheet:', sheet)
        print(pd.read_excel(xls, sheet).head(20).to_markdown())
        print('====================')
except Exception as e:
    print("Error:", e)
    sys.exit(1)
