import mysql.connector
import json
from tqdm import tqdm  # 引入 tqdm

# 数据库配置
config = {
    'user': 'root',  # 请修改为你的MySQL用户名
    'password': 'root',  # 请修改为你的MySQL密码
    'host': '127.0.0.1',
    'database': 'medical_qa',  # 请修改为你的数据库名称
    'charset': 'utf8mb4'  # 确保使用 utf8mb4 编码
}

# 连接数据库
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# 修改数据库和表的字符集为utf8mb4
cursor.execute("ALTER DATABASE `medical_QA` CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;")
cursor.execute("ALTER TABLE qa_pairs CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")

# 创建数据表
create_table_sql = """
CREATE TABLE IF NOT EXISTS qa_pairs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    question_text TEXT,
    answer_text TEXT
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
"""
cursor.execute(create_table_sql)

# 为question_text和answer_text列创建全文索引
create_index_sql = """
ALTER TABLE qa_pairs ADD FULLTEXT INDEX idx_qa_text (question_text, answer_text);
"""
cursor.execute(create_index_sql)

# 从JSONL文件读取数据并插入到数据库
file_path = "D:/soft/treatmentPlan_generation/data.jsonl"
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 使用 tqdm 创建进度条
for line in tqdm(lines, desc="导入数据进度", unit="line"):
    data = json.loads(line.strip())
    question_text = data["questions"][0]  # 因为每个问题只对应一个答案
    answer_text = data["answers"][0]

    insert_sql = "INSERT INTO qa_pairs (question_text, answer_text) VALUES (%s, %s)"
    cursor.execute(insert_sql, (question_text, answer_text))

conn.commit()  # 提交事务
cursor.close()
conn.close()

print("数据导入完成！")
