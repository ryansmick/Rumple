from django.db import models

# Create your models here

# Model to define a poll question
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    creator_id = models.IntegerField()

    def __str__(self):
        return self.question_text
    
# Model to define an option for a given Question
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=200)

    def __str__(self):
        return self.option_text

# Model to define a vote for a given option
class Vote(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    voter_id = models.IntegerField()

    def __str__(self):
        return str(self.voter_id) + ": " + str(self.option)

