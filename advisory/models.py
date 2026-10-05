from django.db import models


class CropAdvisory(models.Model):

    crop_name = models.CharField(max_length=100)
    crop_category = models.CharField(max_length=100)
    planting_season = models.CharField(max_length=100)
    soil_type = models.CharField(max_length=150)
    planting_advice = models.TextField()
    fertilizer_advice = models.TextField()
    pest_information = models.TextField()
    disease_information = models.TextField()
    harvesting_advice = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Crop Advisory"
        verbose_name_plural = "Crop Advisories"

    def __str__(self):
        return self.crop_name


class PestDisease(models.Model):

    crop_name = models.CharField(max_length=100)
    problem_name = models.CharField(max_length=150)
    problem_type = models.CharField(max_length=50)
    symptoms = models.TextField()
    causes = models.TextField()
    prevention = models.TextField()
    control_measures = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pest/Disease Advisory"
        verbose_name_plural = "Pest/Disease Advisories"

    def __str__(self):
        return f"{self.crop_name} - {self.problem_name}"


class FarmingTip(models.Model):

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    practical_advice = models.TextField()
    season = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class LivestockAdvisory(models.Model):

    animal_name = models.CharField(max_length=100)
    animal_category = models.CharField(max_length=100)
    feeding_advice = models.TextField()
    housing_advice = models.TextField()
    common_diseases = models.TextField()
    disease_prevention = models.TextField()
    management_advice = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Livestock Advisory"
        verbose_name_plural = "Livestock Advisories"

    def __str__(self):
        return self.animal_name


class Feedback(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Farmer Feedback"
        verbose_name_plural = "Farmer Feedback"

    def __str__(self):
        return f"{self.name} - {self.subject}"
