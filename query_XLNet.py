import mysql.connector
from mysql.connector import Error
from concurrent.futures import ThreadPoolExecutor, as_completed
from transformers import XLNetTokenizer, XLNetModel
import torch
from scipy.spatial.distance import cosine, cityblock, euclidean
from tqdm import tqdm

# 数据库连接配置
config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'database': 'medical_qa',
    'raise_on_warnings': True
}

# 示例关键词及其权重
keywords = {
    '抑郁症': 0.4,
    '失眠': 0.2,
    '低落': 0.1,
    '食欲': 0.05,
    '运动抑制': 0.05,
    '女': 0.15,
    '24': 0.05
}

# 加载XLNet模型和分词器
model_path = './XLNet-base-chinese'

# 删除模型文件和缓存（可选）
tokenizer = XLNetTokenizer.from_pretrained(model_path, cache_dir=None)
model = XLNetModel.from_pretrained(model_path, cache_dir=None)


# 生成RoBERTa嵌入
def get_XLNet_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
    if torch.cuda.is_available():
        inputs = {k: v.to('cuda') for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings[0].cpu().numpy()

# 计算余弦相似度
def calculate_cosine_similarity(embedding1, embedding2):
    return 1 - cosine(embedding1, embedding2)

# 计算曼哈顿距离
def calculate_manhattan_distance(embedding1, embedding2):
    return cityblock(embedding1, embedding2)

# 计算欧几里得距离
def calculate_euclidean_distance(embedding1, embedding2):
    return euclidean(embedding1, embedding2)


# 批处理大小
batch_size = 20000

# 计算每个问答对的得分
def calculate_score(pair, keywords):
    question, _ = pair
    score = 0
    found_keywords = set()
    for word, weight in keywords.items():
        if word in question and word not in found_keywords:
            score += weight
            found_keywords.add(word)
    return (pair, score)


# 分批从数据库获取问答对
def get_pairs_from_db(config, offset, batch_size):
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor()
            query = f"SELECT Question_text, Answer_text FROM qa_pairs LIMIT {batch_size} OFFSET {offset}"
            cursor.execute(query)
            return cursor.fetchall()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# 生成问题模板
def generate_question_template(keywords):
    high_weight = [k for k, v in keywords.items() if v >= 0.4]
    medium_weight = [k for k, v in keywords.items() if 0.1 <= v < 0.4]
    low_weight = [k for k, v in keywords.items() if v < 0.1]

    high_weight_str = "，".join(high_weight)
    medium_weight_str = "，".join(medium_weight)
    low_weight_str = "，".join(low_weight)

    return f"[性别女，24]，患有[抑郁症]，伴有[失眠，低落，食欲不振，运动抑制]等症状，应如何治疗？用什么药？有什么建议？"


# 并行处理每一批问答对来计算模糊匹配得分
def process_batch_for_fuzzy_matching(offset, batch_size):
    pairs = get_pairs_from_db(config, offset, batch_size)
    with ThreadPoolExecutor() as executor:
        future_to_pair = {executor.submit(calculate_score, pair, keywords): pair for pair in pairs}
        results = []
        for future in as_completed(future_to_pair):
            pair, score = future.result()
            results.append((pair, score))
    return results


# 计算相似度
def calculate_similarity(pair, question_template_embedding):
    _, answer = pair
    answer_embedding = get_XLNet_embedding(answer)
    similarity = calculate_cosine_similarity(question_template_embedding, answer_embedding)
    manhattan_distance = calculate_manhattan_distance(question_template_embedding, answer_embedding)
    euclidean_distance = calculate_euclidean_distance(question_template_embedding, answer_embedding)
    return similarity, manhattan_distance, euclidean_distance


# 主程序也保持不变，只需要更改嵌入生成函数即可
def main():
    # 在主程序中初始化累加器
    sum_similarity, sum_manhattan, sum_euclidean = 0, 0, 0
    total_pairs = 0

    # 生成问题模板
    question_template = generate_question_template(keywords)
    print("问题模板:", question_template)
    question_template_embedding = get_XLNet_embedding(question_template)

    # 首先进行模糊匹配筛选
    offset = 0
    fuzzy_matched_results = []
    while True:
        results = process_batch_for_fuzzy_matching(offset, batch_size)
        if not results:
            break
        fuzzy_matched_results.extend(results)
        offset += batch_size

    # 根据模糊匹配得分排序，并取前20个作为候选集
    sorted_pairs_by_fuzzy_score = sorted(fuzzy_matched_results, key=lambda x: x[1], reverse=True)
    top_n_pairs = sorted_pairs_by_fuzzy_score[:15]  # N 是你选择的候选集大小

    # 输出模糊匹配得分的前20条候选集数据及其分数
    print("根据模糊匹配得分排序的前15个候选集及其分数：")
    for pair, score in sorted_pairs_by_fuzzy_score[:15]:
        question, answer = pair
        print(f"Score: {score},Question: {question}, Answer: {answer}")

    # 对候选集中的答案进行语义相关度匹配
    semantic_matched_results = []
    for pair, _ in tqdm(top_n_pairs, desc="Processing Semantic Matching"):
        similarity, manhattan_distance, euclidean_distance = calculate_similarity(pair, question_template_embedding)
        # 累加计算结果
        sum_similarity += similarity
        sum_manhattan += manhattan_distance
        sum_euclidean += euclidean_distance
        total_pairs += 1
        semantic_matched_results.append((pair, similarity, manhattan_distance, euclidean_distance))

    # 计算均值
    average_similarity = sum_similarity / total_pairs
    average_manhattan = sum_manhattan / total_pairs
    average_euclidean = sum_euclidean / total_pairs

    # 根据语义相关度得分排序，并输出最相关的问答对
    sorted_pairs_by_semantic_similarity = sorted(semantic_matched_results, key=lambda x: x[1], reverse=True)
    for pair, similarity, manhattan_distance, euclidean_distance in sorted_pairs_by_semantic_similarity[:15]:
        question, answer = pair
        print(
            f" Similarity: {similarity}, Manhattan Distance: {manhattan_distance}, Euclidean Distance: {euclidean_distance}")
    # 输出均值
    print("Average Cosine Similarity:", average_similarity)
    print("Average Manhattan Distance:", average_manhattan)
    print("Average Euclidean Distance:", average_euclidean)

if __name__ == "__main__":
    main()

