from django.db import models


class LastVisit(models.Model):
    user_id  = models.IntegerField(null=True)
    time     = models.CharField(max_length=22, null=True)
    visit    = models.IntegerField(null=True)
    class Meta:
        db_table = 'lastvisit'
        indexes  = [
            models.Index(fields=['user_id']),
        ]


class Person(models.Model):
    name     = models.CharField(max_length=22, null=True)
    uid      = models.CharField(max_length=77, null=True, unique=True)
    email    = models.CharField(max_length=22, null=True, unique=True)
    password = models.CharField(max_length=22, null=True)
    lang     = models.CharField(max_length=11, null=True)
    country  = models.CharField(max_length=22, null=True)
    region   = models.CharField(max_length=22, null=True)
    city     = models.CharField(max_length=22, null=True)
    lat      = models.CharField(max_length=33, null=True)
    lng      = models.CharField(max_length=33, null=True)
    other    = models.CharField(max_length=11, null=True)
    class Meta:
        db_table = 'person'
        indexes  = [
            models.Index(fields=['email', 'uid']),
        ]


class Collection(models.Model):
    user_id    = models.IntegerField(null=True)
    date       = models.CharField(max_length=22, null=True)
    pallets    = models.IntegerField(null=True)
    kilos      = models.IntegerField(null=True)
    uid        = models.CharField(null=True, max_length=33)
    file_name  = models.CharField(max_length=22, null=True)
    week       = models.IntegerField(null=True) 

    class Meta:
        db_table = 'colection'
        indexes  = [
            models.Index(fields=['user_id']),
        ] 


class CollectionLines(models.Model):
    user_id       = models.IntegerField(null=True)
    colection_id  = models.IntegerField(null=True)
    order_id      = models.IntegerField(null=True)
    client_name   = models.CharField(null=True, max_length=33)
    delivery_date = models.CharField(max_length=33)
    palets        = models.IntegerField(null=True)
    kilos         = models.IntegerField(null=True)
    export        = models.CharField(max_length=11, null=True)
    country       = models.CharField(max_length=22, null=True)
    region        = models.CharField(max_length=22, null=True)
    city          = models.CharField(max_length=22, null=True)
    lat           = models.CharField(max_length=33, null=True)
    lng           = models.CharField(max_length=33, null=True)
    truck         = models.IntegerField(null=True)
    truck_name    = models.CharField(max_length=33, null=True)
    by_order      = models.IntegerField(null=True)
    meters        = models.IntegerField(null=True)
    zipcode       = models.CharField(max_length=22, null=True)
    conductor_id  = models.IntegerField(null=True)
    line_id       = models.IntegerField(null=True)

    class Meta:
        db_table = 'colectionlines'
        indexes  = [
            models.Index(fields=['colection_id', 'user_id']),
        ] 


class Location(models.Model):
    country   = models.CharField(max_length=22, null=True)
    region    = models.CharField(max_length=22, null=True)
    city      = models.CharField(max_length=22, null=True)
    zipcode   = models.CharField(max_length=22, null=True)
    lat       = models.DecimalField(max_digits=13, decimal_places=11, null=True)
    lng       = models.DecimalField(max_digits=13, decimal_places=11, null=True)

    class Meta:
        db_table = 'location'
        indexes  = [
            models.Index(fields=['zipcode']),
        ]
