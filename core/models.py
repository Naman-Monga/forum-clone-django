from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class question(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    category = models.ManyToManyField(Category, null = True, blank = True)
    time = models.DateTimeField(auto_now=True)
    upvotes = models.PositiveIntegerField(default = 0)
    def __str__(self):
        return self.title

    def incrementUpvotes(self):
        new_votes = self.upvotes + 1
        self.upvotes = new_votes
    
    def decrementUpvotes(self):
        if not self.upvotes==0:
            new_votes = self.upvotes - 1
            self.upvotes = new_votes

    def get_absolute_url(self):
        return reverse("question-detail", kwargs={"pk": self.pk})

class answer(models.Model):
    answerer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=4000)
    question = models.ForeignKey(question, on_delete=models.CASCADE)
    time = models.DateField(auto_now=True, null=True)
    upvotes = models.PositiveIntegerField(default = 0)
    
    def incrementUpvotes(self):
        new_votes = self.upvotes + 1
        self.upvotes = new_votes
    
    def decrementUpvotes(self):
        if not self.upvotes==0:
            new_votes = self.upvotes - 1
            self.upvotes = new_votes

    def __str__(self):
        return self.text


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ques_upvoted = models.ManyToManyField(question,null=True, blank=True)
    ans_upvoted = models.ManyToManyField(answer,null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    
    def check_q(self, quest):
        if quest in self.ques_upvoted.all():
            return True
        else:
            return False

    def check_a(self, ans):
        if ans in self.ans_upvoted.all():
            return True
        else:
            return False