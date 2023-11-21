from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Schedule(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = "branches"


class Workdays(models.Model):
    WEEKDAYS = [
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
        (7, "Sunday"),
    ]

    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name="workdays"
    )
    workday = models.PositiveSmallIntegerField(choices=WEEKDAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.schedule.title} - {self.workday} - {self.start_time} - {self.end_time}"

    class Meta:
        verbose_name_plural = "Workdays"


class Branch(models.Model):
    image = models.ImageField(upload_to="branches", blank=True, null=True)
    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name="branches"
    )
    name_of_shop = models.CharField(max_length=100, default="NeoCafe Dzerzhinka")
    address = models.TextField()
    phone_number = PhoneNumberField()
    link_to_map = models.URLField()

    @property
    def workdays(self):
        return Workdays.objects.filter(schedule=self.schedule)

    def __str__(self):
        return f"{self.name_of_shop}"
