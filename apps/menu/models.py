# menu/models.py
from django.db import models
from apps.branches.models import Branch
from apps.storage.models import Category, Item, Ingredient
from apps.accounts.models import CustomUser

class Menu(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.branch.name_of_shop} - {self.category.name} - {self.item.name} - {self.ingredient.name}"


class Order(models.Model):
    """
    Order model.
    """

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, related_name='orders')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.user.username}"
