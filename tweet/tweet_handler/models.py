from django.db import models

# Create your models here.
class CustomUser(models.Model):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    chat_id = models.CharField(max_length=255, unique=True, primary_key=True)



class UserTweetMapping(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rule_id = models.CharField(max_length=255, db_index=True)
    rule_name = models.CharField(max_length=255, null=True)
