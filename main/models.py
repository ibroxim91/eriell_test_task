from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group as PermissionGroup
from .positions import Position, GroupStatus, StudentStatus, student, teacher, director
from django.contrib.auth.models import Permission
from django.contrib.auth.models import PermissionsMixin
from .get_request import current_request


# # модель пользователя (учитель студент и директор)
class User(AbstractUser):
    position = models.CharField("Position", choices=Position.choices, max_length=20, blank=True)
    phone = models.CharField("Phone", max_length=50, blank=True)
    brith = models.DateField("Date of birth", blank=True, null=True)
    password_is_hash = models.BooleanField("Password is hash", editable=False, default=False)

    def __str__(self):
        return self.get_full_name()

    def teacher_students(self):
        students = []
        if self.position == 'teacher':
            students = User.objects.filter(student_groups__group__teacher=self, position=Position.student.value)   
        return students        

    # Чтобы установить is_staff или is_superuser в зависимости от позиции пользователя
    def save(self, *args, **kwargs):
        if self.password_is_hash is False and self.is_superuser is False:
            self.set_password(self.password)
            self.password_is_hash = True
        if self.position in (teacher, student):
            self.is_staff = True
            self.is_superuser = False
        if self.is_superuser:
            self.position = director
        super().save(*args, **kwargs)


# модель группы
class Group(models.Model):
    teacher = models.ForeignKey(User, verbose_name="Teacher", on_delete=models.CASCADE, related_name="teacher_groups")
    name = models.CharField("Group name", max_length=50)
    status = models.CharField("Status", choices=GroupStatus.choices, max_length=20)
    start_date = models.DateField("Start date", blank=True, null=True)
    end_date = models.DateField("End date", blank=True, null=True)
    reg_date = models.DateField("Reg date", auto_now_add=True)
    price = models.IntegerField("Payment amount", default=0)

    def __str__(self):
        return f" {self.name} Teacher: {self.teacher}"


# модель предметы
class Science(models.Model):
    name = models.CharField("Science name", max_length=120)

    def __str__(self):
        return self.name


# Модель сохранения статуса ученика в группе (когда присоединился, когда ушел, его последний статус в группе)
class GroupStudents(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_groups")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_students", null=True, blank=True)
    status = models.CharField("Status", choices=StudentStatus.choices, max_length=20)
    add_date = models.DateTimeField("Add date", auto_now_add=True)
    left_date = models.DateTimeField("Left date", blank=True, null=True)
    pay_summa = models.IntegerField("Individual payment amount", default=0)

    def __str__(self):
        return f" {self.student}"


# модель оценки
class Score(models.Model):
    teacher = models.ForeignKey(User, verbose_name="Teacher", editable=False,  on_delete=models.CASCADE)
    student = models.ForeignKey(User, verbose_name="Student", on_delete=models.CASCADE, related_name="points")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_score", null=True, blank=True)
    science = models.ForeignKey(Science, verbose_name="Science", on_delete=models.CASCADE)
    reg_date = models.DateField("Reg date", auto_now_add=True)
    point = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # Получаем,  пользователья которий  пытается сохранить данные
        request = current_request()
        self.teacher = request.user
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f" {self.student.first_name} Science: {self.science} Point: {self.point}"


# модель расписания
class LessonPlan(models.Model):
    name = models.CharField("Lesson name", max_length=120)
    teacher = models.ForeignKey(User, verbose_name="Teacher", on_delete=models.CASCADE)
    group = models.ForeignKey(Group, verbose_name="Group", on_delete=models.CASCADE, related_name="lessons")
    science = models.ForeignKey(Science, verbose_name="Science", on_delete=models.CASCADE)
    lesson_date = models.DateField("Lesson date",  blank=True, null=True)
    reg_date = models.DateField("Reg date", auto_now_add=True)

    def __str__(self):
        return self.name
