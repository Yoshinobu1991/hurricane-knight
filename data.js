// 球隊資料庫 (每次比賽後由二沼負責更新此檔案)
const teamData = {
    // 公積金總餘額
    teamFund: 15000,
    
    // 球員名單與目前餘額
    players: [
        { id: 1, name: '莊子毅', isStudent: false, balance: 2000 },
        { id: 2, name: '劉信宏', isStudent: false, balance: 206 },
        { id: 3, name: '藍凱翔', isStudent: false, balance: 793 },
        { id: 4, name: '顏嘉宏', isStudent: false, balance: 453 },
        { id: 5, name: '林雍傑', isStudent: false, balance: 2000 },
        { id: 6, name: '黃浩勝', isStudent: false, balance: 910 },
        { id: 7, name: '蕭喬駿', isStudent: false, balance: 2000 },
        { id: 8, name: '佘文甫', isStudent: false, balance: 2000 },
        { id: 9, name: '劉毓銘', isStudent: false, balance: 717 },
        { id: 10, name: '周澤緯', isStudent: false, balance: 1886 },
        { id: 11, name: '李富生', isStudent: false, balance: 1861 },
        { id: 12, name: '莊晨鴻', isStudent: false, balance: 285 },
        { id: 13, name: '鄭安鈞', isStudent: false, balance: 1706 },
        { id: 14, name: '吳英信', isStudent: false, balance: 1467 },
        { id: 15, name: '黃彥智', isStudent: false, balance: 1368 },
        { id: 16, name: '陳乙嘉', isStudent: false, balance: 1267 },
        { id: 17, name: '陳德光', isStudent: false, balance: 1020 },
        { id: 18, name: '學生A', isStudent: true, balance: 1500 }, // 示意用
    ],

    // 歷史比賽紀錄
    games: [
        /* 
        格式範例：
        { 
            date: '2026-08-30', 
            opponent: '戰神', 
            totalCost: 2950, 
            adultFee: 250, 
            participants: ['莊子毅', '劉信宏', '藍凱翔', '學生A'] 
        }
        */
    ]
};
