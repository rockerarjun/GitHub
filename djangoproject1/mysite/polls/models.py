from django.db import models
from django.utils import timezone
import datetime
from django.db.models import Field, FloatField 
from django.db.models.expressions import CombinedExpression, Func, Value
from django.db.models.functions import Coalesce
from django.db.models.lookups import Lookup
#from blog.models import Blog

#from .models import Question,Choice,Contact
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    #question = models.ForeignKey(Question, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text
    

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text






class Contact(models.Model):
    #subject = models.CharField(max_length=200)
    #message = models.TextField()
    contact_name = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    emailAddress = models.EmailField()
    created_date = models.DateTimeField(default=timezone.now)
    votes = models.IntegerField(default=0)
    
    

    def __str__(self):
        return self.contact_text






class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):
        return self.headline
    
     
