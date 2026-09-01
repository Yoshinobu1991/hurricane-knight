import pandas as pd
import json
import re

file_path = r"c:\Users\Admir\Desktop\Project\Hurricane Knight\2026颶風騎士收支明細費用表.xlsx"
xls = pd.ExcelFile(file_path)

df_players = pd.read_excel(xls, '隊費及儲值金收費紀錄')
df_games = pd.read_excel(xls, '比賽逐場費用明細')
df_team = pd.read_excel(xls, '隊費明細')

# 1. 處理球員基本資料
players = []
for index, row in df_games.iterrows():
    name = row['球員姓名']
    if pd.isna(name):
        continue
    
    initial_balance = row['比賽儲值金']
    current_balance = row['儲值金餘額']
    
    # 根據初始儲值金判斷是否為學生 (1500)
    is_student = (initial_balance == 1500)
    
    players.append({
        "id": index + 1,
        "name": str(name).strip(),
        "isStudent": is_student,
        "initialBalance": int(initial_balance) if pd.notna(initial_balance) else 0,
        "balance": int(current_balance) if pd.notna(current_balance) else 0
    })

# 2. 處理歷史比賽紀錄
games = []
# 找出所有代表比賽的欄位
game_columns = [col for col in df_games.columns if str(col).startswith('比賽日') or str(col).startswith('Column')]

for col in game_columns:
    # 解析欄位名稱，例如: "比賽日3/8 （八里熱身賽）\n(總費用: 1900)" 或 "Column 12比賽日8/2 (VS 戰神)\n(總費用: \n 2946）"
    col_str = str(col).replace('\n', '')
    
    # 嘗試用正則表達式擷取資訊
    # 找日期和對手
    match_title = re.search(r'比賽日(.*?)\s*[（(](.*?)[)）]', col_str)
    date_str = match_title.group(1).strip() if match_title else "未知日期"
    opponent = match_title.group(2).strip() if match_title else "未知對手"
    
    # 找總費用
    match_cost = re.search(r'總費用:\s*(\d+)', col_str)
    total_cost = int(match_cost.group(1)) if match_cost else 0
    
    participants = []
    student_count = 0
    adult_count = 0
    total_deducted = 0
    adult_fee = 0
    
    for index, row in df_games.iterrows():
        name = row['球員姓名']
        if pd.isna(name): continue
        
        val = row[col]
        if pd.notna(val) and val > 0:
            is_student = (row['比賽儲值金'] == 1500)
            participants.append({
                "name": str(name).strip(),
                "fee": int(val)
            })
            
            if is_student:
                student_count += 1
            else:
                adult_count += 1
                adult_fee = int(val) # 記錄一般成人的扣款額 (通常一樣)

    if len(participants) > 0:
        games.append({
            "date": date_str,
            "opponent": opponent,
            "totalCost": total_cost,
            "adultFee": adult_fee,
            "participants": participants
        })

# 3. 處理隊費 (公積金)
team_fund = 0
# 先簡單用一個預設值，或者計算隊費明細的總和
# 從隊費明細中計算總支出
total_expense = df_team['收入/支出金額'].sum() if '收入/支出金額' in df_team.columns else 0
team_fund = 15000 + int(total_expense) # 假設初始有15000

# 輸出成 data.js
data_js_content = f"// 自動生成的資料庫 (基於 Excel 解析)\nconst teamData = {json.dumps({'teamFund': team_fund, 'players': players, 'games': games}, ensure_ascii=False, indent=4)};\n"

with open(r"c:\Users\Admir\Desktop\Project\Hurricane Knight\data.js", 'w', encoding='utf-8') as f:
    f.write(data_js_content)

print("data.js generated successfully!")
