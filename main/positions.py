from django.db import models


class Position(models.TextChoices):
    director = "director", "director"
    student = "student", "student"
    teacher = "teacher", "teacher"


class GroupStatus(models.TextChoices):
    new = "new", "new"
    active = "active", "active"
    arxived = "arxived", "arxived"
    completed = "completed", "completed"


class StudentStatus(models.TextChoices):
    lid = "lid", "lid"
    active = "active", "active"
    trial = "trial", "trial"
    paused = "paused", "paused"
    arxived = "arxived", "arxived"
    left = "left", "left"
    completed = "completed", "completed"


student, teacher, director = Position.student.value, Position.teacher.value, Position.director.value
