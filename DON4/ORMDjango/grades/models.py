from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

# Q? p3 : Utile de créer une class pour le groupe car il peut y avoir plusieurs groupes et un étudiant ne fait pas forcément partie du même groupe.

# Héritages :
# déscendant : recopie tout le parent dans la table fille
# materialisation : les classes filles ont un lien au parent (mutlitable heritance)
# ascendant : manager et proxy (pas à connaitre dans django)

class Group(models.Model):
    id = models.CharField("Numero du groupe", max_length=5, primary_key=True)

class Course(models.Model):
    short_form = models.CharField("Cours réduit", max_length=5, primary_key=True)
    wording = models.CharField("Cours", max_length=25)
    ects = models.IntegerField("ECTS", validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])

class Student(models.Model):
    serial_number = models.CharField("Matricule", max_length=5)
    first_name = models.CharField("Prénom", max_length=50)
    last_name = models.CharField("Nom", max_length=50)
    birth_date = models.DateField("Date de naissance")
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
#    course = models.ManyToManyField(Course)

class Enrolment(models.Model):
    noteStudent = models.IntegerField("noteStudent", validators=[
        MaxValueValidator(20),
        MinValueValidator(0)
    ])
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)

    class Meta:
        unique_together = [['student', 'course']]

class Teacher(models.Model):
    trigram = models.CharField("Abrégé", max_length=3, primary_key=True)
    first_name = models.CharField("Prénom", max_length=50)
    last_name = models.CharField("Nom", max_length=50)
    course = models.ManyToManyField(Course)