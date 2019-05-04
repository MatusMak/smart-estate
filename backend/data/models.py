from django.db import models

TIMEBLOCKS = [
    (6, 'night'),
    (1, 'morning'),
    (2, 'forenoon'),
    (3, 'noon'),
    (4, 'afternoon'),
    (5, 'evening'),
]


class Parking(models.Model):
    name = models.CharField(max_length=200)
    capacity = models.PositiveSmallIntegerField()

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.name} ({self.capacity})'


class Timeslot(models.Model):
    name = models.CharField(max_length=50)

    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return self.name


class Usage(models.Model):
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(Timeslot, on_delete=models.PROTECT)

    full = models.PositiveSmallIntegerField()
    weight = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.parking} - {self.full}'
