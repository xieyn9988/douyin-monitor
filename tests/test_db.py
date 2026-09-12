# test_db.py
import os
import sqlite3
from pathlib import Path

# 先创建数据目录
Path("data").mkdir(exist_ok=True)

def test_database():
    """测试 SQLite 数据库能否正常创建和写入"""
    db_path = "data/test.db"
    
    # 删除旧的测试文件
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # 连接数据库并创建表
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建一个简单的测试表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 插入一条数据
    cursor.execute("INSERT INTO test_items (name) VALUES (?)", ("测试数据",))
    conn.commit()
    
    # 查询数据
    cursor.execute("SELECT * FROM test_items")
    rows = cursor.fetchall()
    
    conn.close()
    
    if len(rows) == 1 and rows[0][1] == "测试数据":
        print("✅ 数据库测试通过！")
        print(f"   查询结果: {rows}")
    else:
        print("❌ 数据库测试失败")

if __name__ == "__main__":
    test_database()