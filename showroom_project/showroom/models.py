from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_countries.fields import CountryField


class CreateUpdate(models.Model):
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()

    class Meta:
        abstract = True


class Car(CreateUpdate):
    class Colors(models.TextChoices):
        white = "WH", ("White")
        red = "RE", ("Red")
        green = "GR", ("Green")
        blue = "BL", ("Blue")
        black = "BK", ("Black")

    class Bodies(models.TextChoices):
        sedan = "SE", ("Sedan")
        hatchback = "HB", ("Hatchback")
        liftback = "LB", ("Liftback")
        crossover = "CO", ("Crossover")
        universal = "UN", ("Universal")
        pickup = "PU", ("Pickup")
        minivan = "MV", ("Minivan")

    year = models.IntegerField(
        validators=[MinValueValidator(1940), MaxValueValidator(2023)]
    )
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    image = models.URLField()
    vin = models.CharField(max_length=17)
    power = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5000)]
    )
    color = models.CharField(
        max_length=20, choices=Colors.choices, default=Colors.black
    )
    body = models.CharField(max_length=20, choices=Bodies.choices, default=Bodies.sedan)

    def __str__(self):
        return f"{self.year} {self.brand} {self.model} {self.vin} {self.power} {self.color} {self.body} {self.created_date} {self.updated_date}"


class User(CreateUpdate):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    location = CountryField()

    def __str__(self):
        return f"{self.name} {self.surname} {self.balance} {self.location} {self.created_date} {self.updated_date}"


class Showroom(CreateUpdate):
    name = models.CharField(max_length=50)
    location = CountryField()
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    unique_members = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="unique_members"
    )
    criteries = models.JSONField(
        blank=True,
        default={
            "year": "",
            "brand": "",
            "model": "",
            "power": 0,
            "color": "",
            "body": "",
        },
    )
    cars = models.ManyToManyField(Car, through="ShowroomCar")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} {self.location} {self.balance} {self.unique_members} {self.criteries} {self.is_active} {self.created_date} {self.updated_date}"


class Provider(CreateUpdate):
    name = models.CharField(max_length=50)
    clients_count = models.IntegerField(default=0)
    location = CountryField()
    cars = models.ManyToManyField(Car, through="ProviderCar")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} {self.creation_date} {self.clients_count} {self.location} {self.is_active} {self.updated_date}"


class SaleHistory(CreateUpdate):
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="sale_history_cars"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sale_history_users"
    )
    showroom = models.ForeignKey(
        Showroom, on_delete=models.CASCADE, related_name="sale_history_showrooms"
    )

    def __str__(self):
        return f"{self.price} {self.car} {self.user} {self.showroom} {self.created_date} {self.updated_date}"


class ShowroomCar(models.Model):
    cars_count = models.IntegerField(validators=[MinValueValidator(0)])
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    showroom = models.ForeignKey(
        Showroom, on_delete=models.CASCADE, related_name="showroom_car_showrooms"
    )
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="showroom_car_cars"
    )

    def __str__(self):
        return f"{self.cars_count} {self.price} {self.showroom} {self.car}"


class ProviderCar(models.Model):
    cars_count = models.IntegerField(validators=[MinValueValidator(0)])
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, related_name="provider_car_providers"
    )
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="provider_car_cars"
    )

    def __str__(self):
        return f"{self.cars_count} {self.price} {self.provider} {self.car}"


class ShowroomSales(CreateUpdate):
    showroom = models.ForeignKey(
        Showroom, on_delete=models.CASCADE, related_name="showrooms_sales_showroom"
    )
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="showroom_sales_car"
    )
    is_active = models.BooleanField(default=True)
    sale = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        return f"{self.showroom} {self.car} {self.is_active} {self.sale} {self.created_date} {self.updated_date}"


class ProviderSales(CreateUpdate):
    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, related_name="providers_sales_provider"
    )
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="provider_sales_cars"
    )
    is_active = models.BooleanField(default=True)
    sale = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        return f"{self.provider} {self.car} {self.is_active} {self.sale} {self.created_date} {self.updated_date}"
