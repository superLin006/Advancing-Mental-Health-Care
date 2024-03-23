# Advancing-Mental-Health-Care
项目总体框架图
![Overall Architecture.png](picture%2FOverall%20Architecture.png)
一 这个部分主要是个性化医疗建议生成的核心代码，主要功能分为4个部分

1 关键词-权重模糊匹配算法

给关键词列表中的关键词分配好权重，以下是一个简单的例子：

['抑郁症','失眠','低落','食欲','运动抑制''女','24']

['抑郁症':0.4,'失眠':0.2,'低落':0.1,'食欲':0.1,'运动抑制':0.1,'女':0.05,'24':0.05]

![Weight Distribution.png](picture%2FWeight%20Distribution.png)


2 MYSQL数据库信息检索

调用关键词-权重模糊匹配算法在MYSQL数据库中直接检索，根据关键词权重取综合评分最高的前50条数据

3 利用模型计算两段文本的语义相似度

调用各个模型分别计算模板问题与问答对的语义相关度（BERT ALBERT RoBERTa  XLNet）

模板问题以下面这个为例：

“[性别女，24]，患有[抑郁症]，伴有[失眠，低落，食欲不振，运动抑制]等症状，应如何治疗？用什么药？有什么建议？”

取第二部得到的候选数据和模板问题一起输入模型得到，排名前10的最相关数据

4 数据清洗与NLP技术处理

数据清洗与提取，筛选出不同治疗方法、药物和建议；信息筛选与分析，识别频繁及单次出现的治疗方案，并去除重复内容，留下独特且相关的建议；最后，基于筛选后的信息，设计新模板生成包含核心治疗方案的个性化医疗建议。
![Medical Advice Generation Process Flowchart.png](picture%2FMedical%20Advice%20Generation%20Process%20Flowchart.png)

二 如何启动程序，运行代码

1 数据集获取

问答数据集（data.jsonl）：https://drive.google.com/file/d/1dc4VHsHec8uPh-UFD2HE_pfX14KjsJrB/view?usp=drive_link

精神心理疾病领域知识图谱构建数据集（heart.json）：https://drive.google.com/file/d/1Y0FX5cpk1LO8it-NHfKueulCUmnGbkRx/view?usp=drive_link

2 MYSQL数据库安装及数据导入

安装完成后，修改data_import.py文件中的数据库连接配置，包括数据库名称、数据库连接密码等，配置好后运行data_import.py即可导入数据

3 利用算法、模型筛选出最终数据

直接运行 query_BERT.py  query_ALBERT.py  query_RoBERTa.py  query_XLNet.py 即可分别得到相应的最终数据
query_Cross_Encoder_RoBERTa.py是用医疗问答数据集微调后的模型，运行能得到模板问题和问答对的相关性分数

需要注意的是，我这里没有直接提供BERT ALBERT RoBERTa XLNet 这几个模型的原文件，需要到hugging face去下载基于中文语料模型训练的模型

4 个性化医疗建议生成

利用模型筛选出的数据，进一步处理，这里我简单模拟了一下，运行test_generate.py即可看到结果

三 医疗知识图谱构建部分

这里不提供代码，只是提供了构建的数据集heart.json
