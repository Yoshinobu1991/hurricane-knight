import pandas as pd
import json
import re
import os

file_path = r"c:\Users\Admir\Desktop\Project\Hurricane Knight\2026颶風騎士收支明細費用表.xlsx"
roster_path = r"c:\Users\Admir\Desktop\Project\Hurricane Knight\2026一軍名單.txt"

# 讀取背號對應表
number_map = {}
if os.path.exists(roster_path):
    with open(roster_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                num = parts[0].strip()
                name = parts[1].strip()
                if num.isdigit():
                    # 處理例外：有些名字可能有差異，例如 佘文甫 / 余文甫
                    if name == "余文甫": name = "佘文甫"
                    number_map[name] = num

xls = pd.ExcelFile(file_path)
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
    is_student = (initial_balance == 1500)
    
    clean_name = str(name).strip()
    
    # 查找背號
    player_number = number_map.get(clean_name, "")
    
    players.append({
        "id": index + 1,
        "name": clean_name,
        "number": player_number,
        "isStudent": is_student,
        "initialBalance": int(initial_balance) if pd.notna(initial_balance) else 0,
        "balance": int(current_balance) if pd.notna(current_balance) else 0
    })

# 2. 處理歷史比賽紀錄
games = []
game_columns = [col for col in df_games.columns if str(col).startswith('比賽日') or str(col).startswith('Column')]

for col in game_columns:
    col_str = str(col).replace('\n', '')
    match_title = re.search(r'比賽日(.*?)\s*[（(](.*?)[)）]', col_str)
    date_str = match_title.group(1).strip() if match_title else "未知日期"
    opponent = match_title.group(2).strip() if match_title else "未知對手"
    
    match_cost = re.search(r'總費用:\s*(\d+)', col_str)
    total_cost = int(match_cost.group(1)) if match_cost else 0
    
    participants = []
    student_count = 0
    adult_count = 0
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
                if int(val) > adult_fee:
                    adult_fee = int(val)

    if len(participants) > 0:
        games.append({
            "date": date_str,
            "opponent": opponent,
            "totalCost": total_cost,
            "adultFee": adult_fee,
            "participants": participants
        })

# 排序球員： 身分(一般優先) -> 背號
def sort_player(p):
    # 學生排在後面，所以 isStudent == True 給 1, False 給 0
    role_score = 1 if p["isStudent"] else 0
    # 背號轉數字，沒有背號的給 999 墊底
    try:
        num = int(p["number"]) if p["number"] else 999
    except:
        num = 999
    return (role_score, num)

players.sort(key=sort_player)

# 3. 處理隊費 (公積金)
total_expense = df_team['收入/支出金額'].sum() if '收入/支出金額' in df_team.columns else 0
team_fund = 15000 + int(total_expense)

data_js_content = f"// 自動生成的資料庫 (基於 Excel 解析)\nconst teamData = {json.dumps({'teamFund': team_fund, 'players': players, 'games': games}, ensure_ascii=False, indent=4)};\n"

with open(r"c:\Users\Admir\Desktop\Project\Hurricane Knight\data.js", 'w', encoding='utf-8') as f:
    f.write(data_js_content)

print("data.js generated with numbers successfully!")
