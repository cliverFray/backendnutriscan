from django.db import models

# Create your models here.

#Programas de ayuda
class AidPrograms(models.Model):
    programId = models.AutoField(primary_key=True)
    programName = models.CharField(max_length=255)
    programDescription = models.TextField()
    programType = models.CharField(max_length=50)
    programContact = models.CharField(max_length=255)

    def __str__(self):
        return self.programName

#Articulos y tips
class ArticlesAndTips(models.Model):
    articleTipId = models.AutoField(primary_key=True)
    articleTipTitle = models.CharField(max_length=255)
    articleTipContent = models.TextField()
    articleTipType = models.CharField(max_length=50)
    articleTipPublicationDate = models.DateField()

    def __str__(self):
        return self.articleTipTitle

#Niño
class Child(models.Model):
    childId = models.AutoField(primary_key=True)
    childName = models.CharField(max_length=50)
    childLastName = models.CharField(max_length=50)
    childAgeMonth = models.IntegerField()
    childGender = models.BooleanField()  # True for Male, False for Female
    childCurrentWeight = models.DecimalField(max_digits=5, decimal_places=2)
    childCurrentHeight = models.DecimalField(max_digits=5, decimal_places=2)
    userId = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.childName

#Tips diarios
class DailyTips(models.Model):
    dailyTipId = models.AutoField(primary_key=True)
    dailyTipContent = models.TextField()
    dailyTipDate = models.DateField()
    dailyTipCategory = models.CharField(max_length=50)

    def __str__(self):
        return self.dailyTipCategory

#Reportes o graficos
class GrowthReports(models.Model):
    reportId = models.AutoField(primary_key=True)
    reportDate = models.DateField()
    reportDescription = models.TextField()
    reportUrl = models.CharField(max_length=255)
    childId = models.ForeignKey(Child, on_delete=models.CASCADE)

    def __str__(self):
        return f"Growth Report {self.reportDate}"

#Centros de salud
class HealthCenters(models.Model):
    healthCenterId = models.AutoField(primary_key=True)
    healthCenterName = models.CharField(max_length=255)
    healthCenterAddress = models.CharField(max_length=255)
    healthCenterEmail = models.EmailField(max_length=255)
    healthCenterPhone = models.CharField(max_length=20)
    healthCenterContactPerson = models.CharField(max_length=255)

    def __str__(self):
        return self.healthCenterName

#Deteccion de desnutricion
class MalnutritionDetection(models.Model):
    detectionId = models.AutoField(primary_key=True)
    detectionDate = models.DateField()
    detectionResult = models.CharField(max_length=50)
    detectionImageUrl = models.CharField(max_length=255)
    childId = models.ForeignKey(Child, on_delete=models.CASCADE)
    healthCenterId = models.ForeignKey(HealthCenters, on_delete=models.CASCADE)

    def __str__(self):
        return f"Detection {self.detectionDate} for {self.childId.childName}"

#Notificaciones
class Notifications(models.Model):
    notificationId = models.AutoField(primary_key=True)
    notificationTitle = models.CharField(max_length=255)
    notificationDescription = models.TextField()
    notificationDate = models.DateField()
    userId = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.notificationTitle
    
#Recomendaciones nutricionales
class NutritionalRecommendations(models.Model):
    recommendationId = models.AutoField(primary_key=True)
    recommendationTitle = models.CharField(max_length=255)
    recommendationDescription = models.TextField()
    recommendationType = models.CharField(max_length=50)
    childId = models.ForeignKey(Child, on_delete=models.CASCADE)

    def __str__(self):
        return self.recommendationTitle

#Tips para embarazadas
class PregnancyTips(models.Model):
    pregnancyTipId = models.AutoField(primary_key=True)
    pregnancyTipContent = models.TextField()
    pregnancyTipStage = models.CharField(max_length=50)
    pregnancyTipDate = models.DateField()
    pregnancyTipCategory = models.CharField(max_length=50)

    def __str__(self):
        return self.pregnancyTipCategory

#Recetas
class Recipes(models.Model):
    recipeId = models.AutoField(primary_key=True)
    recipeName = models.CharField(max_length=255)
    recipeDescription = models.CharField(max_length=255)
    recipeIngredients = models.CharField(max_length=255)
    recipeInstructions = models.CharField(max_length=255)
    recipeEstimatedPrice = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.recipeName

#Recomendacions por recetas
class RecommendationRecipes(models.Model):
    recipeId = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    nutrrecommendationId = models.ForeignKey(NutritionalRecommendations, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('recipeId', 'nutrrecommendationId')

    def __str__(self):
        return f"Recipe {self.recipeId.recipeName} linked to Recommendation {self.nutrrecommendationId.recommendationTitle}"
    
#Usuario
class User(models.Model):
    userId = models.AutoField(primary_key=True)
    userFirstName = models.CharField(max_length=50)
    userLastName = models.CharField(max_length=50)
    userPassword = models.CharField(max_length=255)
    userDNI = models.CharField(max_length=8)
    userPhone = models.CharField(max_length=9)
    userEmail = models.EmailField(max_length=255)
    userRegistrationDate = models.DateField()
    UserPlace = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.userFirstName} {self.userLastName}"