# 🧠Advancing Mental Health Care 

📝 **项目简介：**

随着精神心理健康问题日益凸显，如今面临着相关医疗资源严重分布不均和诊疗效率低下的挑战。本项目结合有限状态机🤖、检索算法🔍、语义匹配模型📊以及医疗知识图谱📚等信息技术，设计了一种创新的智能辅助评估工具和个性化医疗建议生成应用，用于提升精神心理健康评估的效率并生成个性化医疗建议。

## 📋 **目录**

### 🌐 总体框架
* [框架图](#框架图)

### 🤖 精神心理健康辅助诊断工具实现

* 1️⃣ [M.I.N.I 概述](#1-mini-概述)
* 2️⃣ [有限状态机](#2-有限状态机)
* 3️⃣ [信息收集流程设计](#3-信息收集流程设计)

### 🏥 个性化医疗建议生成

* 1️⃣ [关键词-权重模糊匹配算法](#1--关键词-权重模糊匹配算法)
* 2️⃣ [MySQL数据库信息检索](#2-mysql-数据库信息检索)
* 3️⃣ [文本对语义相似度计算](#3-文本对语义相似度计算)
* 4️⃣ [医疗建议生成](#4-医疗建议生成)

### 📊 医疗知识图谱应用

* 1️⃣ [医疗知识图谱](#1-医疗知识图谱)
* 2️⃣ ️ [知识生成过程](#2-知识生成过程)


### 🚀 如何启动程序并运行代码

* 1️⃣ [数据集获取](#1-数据集获取)
* 2️⃣ [MySQL数据库安装及数据导入](#2-mysql-数据库安装及数据导入)
* 3️⃣ [利用算法与模型筛选数据](#3-利用算法与模型筛选数据)
* 4️⃣ [个性化医疗建议生成](#4-个性化医疗建议生成)


## 🌐 总体框架
### 框架图
![Overall Architecture.png](picture%2FOverall%20Architecture.png)

本项目包含以下三个核心模块：

* 精神心理健康辅助评估工具构建与实现🤖
* 个性化医疗建议生成📝
* 医疗知识图谱的应用📚

首先，通过辅助评估工具来收集患者信息，并对结果进行评估。基于这些信息，系统会生成个性化医疗建议。如果数据质量不佳或模型匹配精度低于设定阈值，则系统会利用知识图谱来生成普适性的医疗建议。

🔗 更多详情可参考我们的论文📄：https://www.mdpi.com/2076-3417/14/20/9447

🔑 **关键词**： 精神心理健康🧠，人工智能🤖，自然语言处理🗣️，医疗知识图谱📚，自动生成📝

## 🤖 精神心理健康辅助评估工具构建与实现

我们基于 [M.I.N.I 6.0.0](https://pdfcoffee.com/mini-600-3-pdf-free.html) 版本，结合有限状态机和 WEB 交互技术，构建了一种智能化的精神心理疾病辅助评估工具，为诊断提供信息自动化支持，效果图如下（**各种原因暂不提供工具源码**）：

![Auxiliary Assessment Effect.png](picture%2FAuxiliary%20Assessment%20Effect.png)

### 1️⃣ M.I.N.I 概述

M.I.N.I 是一种综合性的诊断评估工具，包含 A 到 P 共 16 个独立模块，每个模块运用复杂的逻辑判断机制。
为了实现智能化，我们对每个模块进行了专门建模，采用有限状态机对用户回答进行逻辑计算和跳转，从而实现灵活的信息收集与全面的结果评估。

### 2️⃣️ 有限状态机

状态机是一种计算模型，用于描述对象或系统在不同状态间的转换行为。工作原理图如下：
![Finite State Machine Working Principle Diagram.jpg](picture%2FFinite%20State%20Machine%20Working%20Principle%20Diagram.jpg)

 ### 3️⃣ 信息收集流程设计

利用状态机模型的原理，对M.I.N.I 6.0.0的各个模块进行建模。每当用户回答一个问题时，都会触发某个事件，从而决定下一个要问的问题，直到达到评估条件或者完成该模块的所有问题，最后进行结果评估。其流程设计图如下所示：
![Program Flowchart.png](picture%2FProgram%20Flowchart.png)

## 🏥 个性化医疗建议生成

### 1️⃣ 🔑 关键词-权重⚖️模糊匹配算法

该算法的处理流程如下：

![Key Words Weight.png](picture%2FKey%20Words%20Weight.png)

通过为关键词列表中的关键词分配权重⚖️，系统可以更精确地匹配医疗建议。例如：

关键词列表：['抑郁症', '失眠', '低落', '食欲', '运动抑制', '女', '24']

权重⚖️分配：['抑郁症': 0.4, '失眠': 0.2, '低落': 0.1, '食欲': 0.1, '运动抑制': 0.1, '女': 0.05, '24': 0.05]

![Key Words Weight.png](picture%2FKey%20Words%20Weight.png)

### 2️⃣ MySQL 数据库🗄️信息检索🔍

利用关键词-权重⚖️模糊匹配算法在 MySQL 数据库🗄️中直接检索🔍，选取综合评分最高的前 50 条数据。

### 3️⃣ 文本对📝语义相似度计算📊

使用各个模型（BERT、ALBERT、RoBERTa、XLNet）分别计算模板问题与问答对答案部分的语义相关度📊。模板问题如下：

"[性别女，24]，患有[抑郁症]，伴有[失眠，低落，食欲不振，运动抑制]等症状，应如何治疗？用什么药？有什么建议？"

模型会从候选数据中选取排名前 10 的最相关数据。

### 4️⃣ 医疗建议生成📝

我们采用了两种方式来生成个性化医疗建议，流程如下：

![Medical Advice Generation Process Flowchart.png](picture%2FMedical%20Advice%20Generation%20Process%20Flowchart.png)

方法一： 数据清洗🧹与提取，识别并筛选不同治疗方案、药物💊和建议。通过新模板生成包含核心治疗方案的个性化医疗建议。代码文件：NLP_generate.py

方法二： 调用大语言模型（LLM）API，如百度的千帆大模型“ERNIE-speed-128k”，生成个性化医疗建议。代码文件：LLM_generate.py
效果图如下：

![Generating Effect.png](picture%2FGenerating%20Effect.png)

## 📊 医疗知识图谱应用

### 1️⃣ 医疗知识图谱

以下是我们构建的医疗知识图谱：

![Knowledge Graph.png](picture%2FKnowledge%20Graph.png)

### 2️⃣ 知识生成过程

当数据质量不佳或模型匹配精度低于阈值时，系统会利用构建的知识📚图谱来生成普适性的医疗建议。

知识图谱📚的知识检索🔍及医疗建议生成过程如下：

![Knowledge Graph Generate Advice.png](picture%2FKnowledge%20Graph%20Generate%20Advice.png)

具体的构建代码不提供，但可以参考部分数据集 heart.json，更多内容请参阅：🔗https://github.com/liuhuanyong/QASystemOnMedicalKG

普适性医疗建议效果图：

![Generation Effect 2.png](picture%2FGeneration%20Effect%202.png)

## 🚀 如何启动程序并运行代码💻

### 1️⃣ 数据集获取📥

问答数据集 (部分)：[点击下载](https://drive.google.com/file/d/1dc4VHsHec8uPh-UFD2HE_pfX14KjsJrB/view?usp=drive_link)

知识图谱构建数据集 (部分)：[点击下载](https://drive.google.com/file/d/1Y0FX5cpk1LO8it-NHfKueulCUmnGbkRx/view?usp=drive_link )

### 2️⃣ MySQL 数据库🗄️安装及数据导入📂

完成安装后，修改 Preprocessing/data_import.py 文件中的数据库连接配置（如数据库名称、连接密码🔑等），运行 data_import.py 即可导入数据📂。

### 3️⃣ 利用算法与模型筛选数据📊

运行 model 文件夹下的 query_BERT.py、query_ALBERT.py、query_RoBERTa.py、query_XLNet.py，即可得到相应的最终数据及模板问题和问答对的相关性分数（如余弦值、欧几里得距离、曼哈顿距离）。

注意：需要到 [Hugging Face](https://huggingface.co/models) 下载中文语料模型。

### 4️⃣ 个性化医疗建议生成📝

根据模型筛选的数据进行进一步处理，采用两种方法：NLP 流程处理和 LLM 处理。运行 test 目录下的文件即可查看生成结果。
