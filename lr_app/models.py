# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class RecruitInfo(models.Model):
    website = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    job_category = models.CharField(max_length=255, blank=True, null=True)
    job_name = models.CharField(max_length=255, blank=True, null=True)
    salary = models.CharField(max_length=255, blank=True, null=True)
    experience_time = models.CharField(max_length=255, blank=True, null=True)
    education = models.CharField(max_length=255, blank=True, null=True)
    job_info = models.CharField(max_length=5000, blank=True, null=True)
    request_num = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=800, blank=True, null=True)
    company_scale = models.CharField(max_length=255, blank=True, null=True)
    company_net = models.CharField(max_length=255, blank=True, null=True)
    company_property = models.CharField(max_length=255, blank=True, null=True)
    company_business = models.CharField(max_length=255, blank=True, null=True)
    issue_time = models.CharField(max_length=255, blank=True, null=True)
    remark = models.CharField(unique=True, max_length=255, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recruit_info'
        unique_together = (('website', 'city', 'job_category', 'job_name'),)


class RecruitInfoMyTest(models.Model):
    id = models.IntegerField(primary_key=True)
    job_name = models.CharField(max_length=255, blank=True, null=True)
    salary = models.CharField(max_length=255, blank=True, null=True)
    experience_time = models.CharField(max_length=255, blank=True, null=True)
    education = models.CharField(max_length=255, blank=True, null=True)
    job_info = models.CharField(max_length=1000, blank=True, null=True)
    job_require = models.CharField(max_length=1000, blank=True, null=True)
    request_num = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    company_scale = models.CharField(max_length=255, blank=True, null=True)
    company_net = models.CharField(max_length=255, blank=True, null=True)
    company_property = models.CharField(max_length=255, blank=True, null=True)
    company_business = models.CharField(max_length=255, blank=True, null=True)
    issue_time = models.CharField(max_length=255, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    class Meta:

        db_table = 'recruit_info_my_test'


class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    status = models.IntegerField()
    time = models.DateTimeField()
    ip=models.CharField(max_length=255)
    index=models.IntegerField()
    ip_address=models.CharField(max_length=255)
    salt = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)


    class Meta:
        db_table = 't_user'
