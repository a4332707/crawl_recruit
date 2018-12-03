# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class RecruitInfo(models.Model):
    website = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    job_category = models.CharField(max_length=255)
    job_name = models.CharField(max_length=255)
    salary = models.CharField(max_length=255)
    experience_time = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    job_info = models.CharField(max_length=5000)
    request_num = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    address = models.CharField(max_length=800)
    company_scale = models.CharField(max_length=255)
    company_net = models.CharField(max_length=255)
    company_property = models.CharField(max_length=255)
    company_business = models.CharField(max_length=255)
    issue_time = models.CharField(max_length=255)
    remark = models.CharField(unique=True, max_length=255)
    time = models.DateTimeField()
    status = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'recruit_info'
        unique_together = (('website', 'city', 'job_category', 'job_name'),)

class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    status = models.IntegerField()
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 't_user'

