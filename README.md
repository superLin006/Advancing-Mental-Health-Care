# Advancing-Mental-Health-Care
项目简介：随着精神心理健康问题日益凸显，如今面临着相关医疗资源严重分布不均和诊疗效率低下的挑战。本项目结合有限状态机、检索算法、语义匹配模型以及医疗知识图谱等信息技术，设计了一种创新的智能辅助评估工具和个性化医疗建议生成应用。用于提升精神心理健康评估的效率和生成个性化医疗建议。
总体框架图如下：![Overall Architecture.png](picture%2FOverall%20Architecture.png)
由于各种原因这里不提供智能辅助评估工具的源码，将按顺序着重介绍以下内容，个性化医疗建议生成、医疗知识图谱应用、如何启动程序和运行代码

我们的论文：https://www.mdpi.com/2076-3417/14/20/9447  关键词： 精神心理健康，人工智能，自然语言处理，医疗知识图谱，自动生成


一 个性化医疗建议生成



1 关键词-权重模糊匹配算法

![Key Words Weight.png](picture%2FKey%20Words%20Weight.png)
给关键词列表中的关键词分配好权重，以下是一个简单的例子：

['抑郁症','失眠','低落','食欲','运动抑制''女','24']

['抑郁症':0.4,'失眠':0.2,'低落':0.1,'食欲':0.1,'运动抑制':0.1,'女':0.05,'24':0.05]

![Weight Distribution.png](picture%2FWeight%20Distribution.png)


2 MYSQL数据库信息检索

调用关键词-权重模糊匹配算法在MYSQL数据库中直接检索，根据关键词权重取综合评分最高的前50条数据

3 文本对（问题-答案）语义相似度计算

调用各个模型（BERT ALBERT RoBERTa  XLNet）分别计算模板问题与问答对答案部分的语义相关度

模板问题以下面这个为例：

“[性别女，24]，患有[抑郁症]，伴有[失眠，低落，食欲不振，运动抑制]等症状，应如何治疗？用什么药？有什么建议？”

取第二部得到的候选数据和模板问题一起输入模型得到，排名前10的最相关数据

4 数据清洗与NLP技术处理

（1）方法一：数据清洗与提取，筛选出不同治疗方法、药物和建议；信息筛选与分析，识别频繁及单次出现的治疗方案，并去除重复内容，留下独特且相关的建议；最后，基于筛选后的信息，设计新模板生成包含核心治疗方案的个性化医疗建议。做了简单模拟，对应的代码文件为：NLP_generate.py

（2）方法二：调用大语言模型（LLM）API,来整理我们最终得到的数据，进而实现个性化医疗建议的生成,我采用的是百度的千帆大模型“ERNIE-speed-128k”,对应的代码文件为：LLM_generate.py
![Medical Advice Generation Process Flowchart.png](picture%2FMedical%20Advice%20Generation%20Process%20Flowchart.png)


二 医疗知识图谱应用

![Knowledge Graph.png](picture%2FKnowledge%20Graph.png)
![Knowledge Graph Generate Advice.png](picture%2FKnowledge%20Graph%20Generate%20Advice.png)
在检索的数据质量不佳或模型匹配精度低于设定阈值的情况下，不足以生成个性化医疗建议，这时系统会利用我们构建的医疗知识图谱来生成普适性的医疗建议
这里不提供具体的构建代码，只是提供了构建图谱的部分数据集heart.json，具体可参考：https://github.com/liuhuanyong/QASystemOnMedicalKG

三 如何启动程序，运行代码

1 数据集获取

问答数据集(部分)（data.jsonl）：https://drive.google.com/file/d/1dc4VHsHec8uPh-UFD2HE_pfX14KjsJrB/view?usp=drive_link

精神心理疾病领域知识图谱构建数据集（部分）（heart.json）：https://drive.google.com/file/d/1Y0FX5cpk1LO8it-NHfKueulCUmnGbkRx/view?usp=drive_link 参考了：https://github.com/liuhuanyong/QASystemOnMedicalKG

2 MYSQL数据库安装及数据导入

安装完成后，修改Preprocessing/data_import.py文件中的数据库连接配置，包括数据库名称、数据库连接密码等，配置好后运行data_import.py即可导入数据

3 利用算法、模型筛选出最终数据

直接运行model这个文件夹下的 query_BERT.py  query_ALBERT.py  query_RoBERTa.py  query_XLNet.py 即可分别得到相应的最终数据，以及对应到模板问题和问答对的相关性分数（余弦值），欧几里得距离，曼哈顿距离。注意：论文中关于用专业领域数据RoBERTa微调后的FT_RoBERTa这里不提供具体的数据和代码。

需要注意的是，我这里没有直接提供BERT ALBERT RoBERTa XLNet 这几个模型的原文件，需要到hugging face去下载基于中文语料模型训练的模型

4 个性化医疗建议生成

利用模型筛选出的数据，进一步处理，这里我采用了两种方法，分别是NLP流程处理和大预言模型LLM处理，运行test这个目录下的文件就能看到结果