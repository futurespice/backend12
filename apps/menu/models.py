# menu/models.py
from django.db import models
from apps.branches.models import Branch
from apps.storage.models import Category, Item, Ingredient


class Menu(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recommendations = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return f"{self.branch.name_of_shop} - {self.category.name} - {self.item.name} - {self.ingredient.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Check if recommendations need to be updated (object has an id)
        if self.id is not None:
            # Clear existing recommendations
            self.recommendations.clear()

            # Set recommendations based on the get_recommendations method
            recommendations = self.get_recommendations()
            if recommendations.exists():
                # Add new recommendations only if there are any
                self.recommendations.add(*recommendations)

    def get_recommendations(self):
        # Your existing logic for getting recommendations
        recommendations = Menu.objects.filter(
            ingredient__in=self.ingredient.all(),
            branch=self.branch
        ).exclude(id=self.id).distinct()

        # Limit the number of categories to 5
        categories = recommendations.values_list('category', flat=True).distinct()[:categories_limit]

        return recommendations.filter(category__in=categories)