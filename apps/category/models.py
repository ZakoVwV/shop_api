from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=25)
    image = models.ImageField(upload_to='category-images/')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name = 'children'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'