
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

Rating = [
    ('b', 'Bad'),
    ('a', 'Average'),
    ('e', 'Excellent')
]

#DataFlair
class Product(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField()
    mfg_date = models.DateTimeField(auto_now_add = True)
    rating = models.CharField(max_length = 1, choices = Rating)

    def __str__(self):
        return self.name

    def show_desc(self):
        return self.description[:50]


class Person(models.Model):
    last_name = models.TextField()
    first_name = models.TextField()
    courses = models.ManyToManyField("Course", blank=True)
    
    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name_plural = "People"
        ordering = ("last_name", "first_name")

class Course(models.Model):
    name = models.TextField()
    year = models.IntegerField()
    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "year", )

class Grade(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    grade = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self):
        return self.person.first_name