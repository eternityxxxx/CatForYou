import uuid

from django.db import models
from django.core.validators import MaxValueValidator


class Breed(models.Model):
    """
        Класс описывает описывает модель 'порода'
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=128, verbose_name="Порода")
    breed_description = models.TextField(verbose_name="Описание породы")
    code = models.CharField(max_length=128, verbose_name="Код для поиска")

    def __str__(self):
        return self.name


class Registration(models.Model):
    """
        Класс описывает модель 'регистрационный документ'
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date = models.DateField(verbose_name="Дата регистрации")
    cage = models.CharField(max_length=10, verbose_name="Номер клетки")
    reg_num = models.CharField(max_length=256, auto_created=True, null=True, blank=True, verbose_name="Номер документа")

    def __str__(self):
        return self.reg_num if self.reg_num else self.date.strftime("%d-%m-%Y")


class Food(models.Model):
    """
        Класс описывает модель 'любимое лакомство'
    """
    name = models.CharField(max_length=128, verbose_name="Название продукта")

    def __str__(self):
        return self.name


class Pet(models.Model):
    """
        Класс описывает модель 'питомец'
    """
    COLOR_CHOICES = [
        ("BL", "Black"),
        ("GR", "Grey"),
        ("WH", "White"),
        ("RD", "Redhead")
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=128, verbose_name="Кличка")
    story = models.TextField(verbose_name="История кошки")
    age = models.PositiveSmallIntegerField(verbose_name="Возраст", validators=[MaxValueValidator(100)])
    color = models.CharField(max_length=2, choices=COLOR_CHOICES, verbose_name="Цвет")
    mood = models.CharField(max_length=128, verbose_name="Настроение кошки")
    photo = models.ImageField(upload_to="media/pets_photo", blank=True, verbose_name="Фото")

    breed = models.ForeignKey(
        Breed, 
        on_delete=models.CASCADE, 
        related_name="pet_breed", 
        verbose_name="Порода"
    )
    doc = models.ForeignKey(
        Registration, 
        on_delete=models.CASCADE,
        related_name="pet_doc",
        verbose_name="Регистрационный документ"    
    )
    food = models.ManyToManyField(
        Food,
        related_name="pet_food",
        verbose_name="Любимое лакомство"
    )

    def make_word_end(self):
        if self.age < 21:
            if self.age == 1:
                word = "год"
            elif self.age in range(2, 5):
                word = "года"
            else:
                word = "лет"
        else:
            if self.age % 10 == 1:
                word = "год"
            elif self.age % 10 in range(2, 5):
                word = "года"
            else:
                word = "лет"

        return "{} {}".format(self.age, word)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.doc.reg_num = self.breed.name[0] + self.doc.date.strftime("%d%m%Y")
        self.doc.save()
        super().save()

    def __str__(self):
        return "{} ({}, {})".format(self.name, self.breed, self.make_word_end())