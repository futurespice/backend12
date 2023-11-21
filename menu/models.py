# menu/models.py
from django.db import models
from apps.branches.models import Branch
from apps.storage.models import Category, Item, Ingredient

class Menu(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    # Добавляем поле для хранения рекомендаций
    recommendations = models.ManyToManyField('self', blank=True)

    # Добавьте другие поля и методы по мере необходимости

    def __str__(self):
        return f"{self.branch.name} - {self.category.name} - {self.item.name} - {self.ingredient.name}"

    def get_recommendations(self):
        # Логика для получения рекомендаций, например, на основе схожих ингредиентов или категорий
        return Menu.objects.filter(ingredient__in=self.ingredient.all()).exclude(id=self.id).distinct()

    def save(self, *args, **kwargs):
        # При сохранении объекта Menu, обновляем рекомендации
        self.recommendations.set(self.get_recommendations())
        super().save(*args, **kwargs)
