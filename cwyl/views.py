from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
import re
import jieba
from django.conf import settings
from .models import Oridata, ODIndex,QandA
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    return render(request, 'index.html')  # 确保你有一个 index.html 模板

@csrf_exempt
def buildindex(request):
    res = {
        'status': 404,
        'text': 'Unknown request!'
    }
    if request.method == 'POST':
        name = request.POST.get('id')
        if name == 'submit2index':
            stopwords = []
            stopwords_file_path = 'C:\\Users\\xxuu\\Desktop\\社交网络\\徐瑜+22920212204471+作业三\\stopwords.txt'  # 您定义的stopwords文件路径

            with open(stopwords_file_path, encoding='utf-8') as f:
                stopwords = [word.strip() for word in f]
            # 获取所有电影的文本属性用于索引
            movie_list = Oridata.objects.values('id', 'question', 'answer')
            all_keywords = []
            movie_set = dict()
            for movie in movie_list:
                movie_id = movie['id']
                text = movie['question']+movie['answer']
                # 正则表达式去除非文字和数字的字符
                movie_text = re.sub(r'[^\w]+', '', text.strip())
                cut_text=jieba.cut(movie_text, cut_all=False)
                keywordlist = []
                for word in cut_text:
                	# 此处去停用词
                    if word not in stopwords:
                        keywordlist.append(word)
                all_keywords.extend(keywordlist)
                movie_set[movie_id] = keywordlist
            # 利用set删除重复keywords
            set_all_keywords = set(all_keywords)
            # 建立倒排索引
            for term in set_all_keywords:
                temp=[]
                for m_id in movie_set.keys():
                    cut_text = movie_set[m_id]
                    if term in cut_text:
                        temp.append(m_id)
                # 存储索引到数据库
                try:
                    exist_list = ODIndex.objects.get(q_keyword=term)
                    exist_list.q_doclist = json.dumps(temp)
                    exist_list.save()
                except ObjectDoesNotExist:
                    new_list = ODIndex(q_keyword=term, q_doclist=json.dumps(temp))
                    new_list.save()
            res = {
                'status': 200,
                'text': 'Index successfully!'
            }
    return HttpResponse(json.dumps(res), content_type='application/json')

# 定义问答页面. 
def questionAnswering(request): 
    return render(request, 'questionAnswering.html') 

# 定义问答检索请求链接.
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import numpy as np
import jieba.analyse
from transformers import BertTokenizer, BertForQuestionAnswering
import torch
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from .models import QandA  # 假设QandA模型在同一应用中
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

# 星火认知大模型相关配置
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
SPARKAI_APP_ID = 'd7524846'
SPARKAI_API_SECRET = 'YmM1MjVmNTdjYmRkNzY1NWI1NDY0YWJh'
SPARKAI_API_KEY = '8bdcd6fd30b3c3bb084535c2d11e16f5'
SPARKAI_DOMAIN = 'generalv3.5'

# 定义问答库
qa_data = QandA.objects.all()

# 提取问题和答案
questions = [qa.question for qa in qa_data]
answers = [qa.answer for qa in qa_data]

# 使用TF-IDF向量化文本数据
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

# 使用KNN算法进行最近邻搜索
knn = NearestNeighbors(n_neighbors=3)
knn.fit(X)

# 自定义函数进行关键字提取
def extract_keywords(text, topK=20):
    keywords = jieba.analyse.extract_tags(text, topK=topK, withWeight=False)
    return ', '.join(keywords)

def get_question_and_text_from_database():
    # 从数据库中检索最新的问题和答案
    q_and_a = QandA.objects.latest('id')
    question = q_and_a.question
    text = q_and_a.answer
    return question, text

def answer_question(question, text):
    # 加载预训练的 BERT 模型和分词器
    tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
    model = BertForQuestionAnswering.from_pretrained('bert-base-chinese')

    # 对问题和文本进行编码处理
    inputs = tokenizer.encode_plus(question, text, add_special_tokens=True, return_tensors="pt")

    # 获取模型的答案
    answer_start_scores, answer_end_scores = model(**inputs)

    # 找到答案的开始和结束位置
    answer_start = torch.argmax(answer_start_scores)
    answer_end = torch.argmax(answer_end_scores) + 1

    # 转换id到token，提取答案
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end]))

    return answer

@csrf_exempt
def searchanswer(request):
    res = {
        'status': 404,
        'text': 'Unknown request!',
        'retrieval_answers': [],
        'ml_answers': [],
        'fine_tuned_answers': []
    }
    if request.method == 'GET':
        name = request.GET.get('id')
        if name == 'chatbotsendbtn':
            try:
                # 获取前端的问题文本
                text = request.GET.get('text')

                # 对输入问题文本进行关键字提取
                keywords = extract_keywords(text)

                # 使用TF-IDF向量化输入问题
                text_vec = vectorizer.transform([keywords])

                # 计算输入问题与问答库中问题的余弦相似度
                similarities = cosine_similarity(text_vec, X).flatten()

                # 获取最相似的问题的索引
                most_similar_idx = np.argmax(similarities)
                max_similarity = similarities[most_similar_idx]

                # 设置相似度阈值，根据需求自行调整
                threshold = 0.1

                # 基于检索返回最相关的一个答案
                retrieval_indices = knn.kneighbors(text_vec, return_distance=False)[0]
                res['retrieval_answers'] = [answers[idx] for idx in retrieval_indices]

                if max_similarity >= threshold:
                    res['status'] = 200
                    res['text'] = answers[most_similar_idx]

                # 使用机器学习模型返回最相关的一个答案
                question, db_text = get_question_and_text_from_database()
                ml_answer = answer_question(text, db_text)  # 使用前端的问题而不是数据库中的问题
                res['ml_answers'] = [ml_answer]

                # 使用星火模型微调返回最相关的一个答案
                spark = ChatSparkLLM(
                    spark_api_url=SPARKAI_URL,
                    spark_app_id=SPARKAI_APP_ID,
                    spark_api_key=SPARKAI_API_KEY,
                    spark_api_secret=SPARKAI_API_SECRET,
                    spark_llm_domain=SPARKAI_DOMAIN,
                    streaming=False,
                )
                spark_messages = [ChatMessage(role="user", content=text)]
                handler = ChunkPrintHandler()
                spark_response = spark.generate([spark_messages], callbacks=[handler])
                res['fine_tuned_answers'] = [spark_response]

            except Exception as e:
                print(e)
                res['text'] = answers[most_similar_idx]

    return HttpResponse(json.dumps(res), content_type='application/json')
