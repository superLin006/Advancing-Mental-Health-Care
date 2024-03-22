import tensorflow as tf
from transformers import BertTokenizer, TFBertModel
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Flatten

# 加载预训练的BERT模型和tokenizer
model_path = './roberta-base-chinese'
tokenizer = BertTokenizer.from_pretrained(model_path)
bert_model = TFBertModel.from_pretrained(model_path)

# Cross-Encoder模型定义
def build_cross_encoder_model():
    # 输入是两个文本
    input_ids = Input(shape=(128,), dtype=tf.int32, name="input_ids")
    token_type_ids = Input(shape=(128,), dtype=tf.int32, name="token_type_ids")
    attention_mask = Input(shape=(128,), dtype=tf.int32, name="attention_mask")

    # BERT模型
    bert_output = bert_model(input_ids, token_type_ids=token_type_ids, attention_mask=attention_mask)
    cls_token = bert_output[0][:, 0, :]  # 取CLS标记的输出

    # 全连接层
    out = Dense(128, activation='relu')(cls_token)
    out = Dense(1, activation='sigmoid')(out)  # 二分类输出

    model = Model(inputs=[input_ids, token_type_ids, attention_mask], outputs=out)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model

# 构建模型
model = build_cross_encoder_model()

# 准备数据：将文本对转换为BERT的输入格式
def prepare_data(text1, text2):
    encoding = tokenizer.encode_plus(text1, text2, return_tensors='tf', max_length=128, truncation=True, padding='max_length')
    return encoding

# 示例文本
text1 = "[性别女，24]，患有[抑郁症]，伴有[失眠，低落，食欲，运动抑制]等症状，应如何治疗？用什么药？有什么建议？"
text2 = "老是失眠，心情低落，会不会是抑郁症', '问题分析：您好，您心情每次晚上低落，失眠考虑是神经衰弱，与植物神经功能紊乱有关系的，指导建议：建议你口服谷维素、刺五加、B1片来调理。平时生活规律一点，不能熬夜上火的。"

# 转换数据
encoded_input = prepare_data(text1, text2)

# 使用模型进行预测
prediction = model.predict({'input_ids': encoded_input['input_ids'], 'token_type_ids': encoded_input['token_type_ids'], 'attention_mask': encoded_input['attention_mask']})

print(f"文本相关性预测: {prediction[0][0]}")
