from django.db import models
from django.contrib import admin

class QandA(models.Model):
    question = models.TextField()
    answer = models.TextField()
    def __str__(self):
        return self.question
    
class Oridata(models.Model):
    question = models.TextField()
    answer = models.TextField()
    def __str__(self):
        return self.question

# 创建索引表 
class ODIndex(models.Model): 
    q_keyword = models.CharField(max_length=256) 
    q_doclist = models.TextField() 
    def __str__(self): 
        return self.q_keyword
    

