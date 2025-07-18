from django.contrib.auth.models import User
from django.db import models
import uuid
from django.db import transaction

class AditionalInfoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación con el modelo User predeterminado
    userDNI = models.CharField(max_length=8, unique=True)
    userPhone = models.CharField(max_length=9, unique=True)
    userPlace = models.CharField(max_length=50)
    is_confirmed = models.BooleanField(default=False)  # <--- nuevo campo
    # otros campos adicionales específicos del Cuidador

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

#child
    
class Child(models.Model):
    childId = models.AutoField(primary_key=True)
    childName = models.CharField(max_length=50)
    childLastName = models.CharField(max_length=50)
    childAgeMonth = models.IntegerField()
    childGender = models.BooleanField()  # True para masculino, False para femenino
    childCurrentWeight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Permitir nulos
    childCurrentHeight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Permitir nulos
    childBirthDate = models.DateField()  # Fecha de nacimiento del niño
    user = models.ForeignKey(User, related_name="children", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.childName} {self.childLastName}"
    
#Detecciones

class MalnutritionDetection(models.Model):
    detectionId = models.AutoField(primary_key=True)
    detectionDate = models.DateField(auto_now_add=True)  # Fecha de detección, se asigna automáticamente
    detectionResult = models.CharField(max_length=50)  # Resultado de la detección
    detectionImageUrl = models.URLField(max_length=1000)  # URL de la imagen en S3
    expirationDate = models.DateTimeField(null=True, blank=True)  # Fecha de expiración de la URL
    confidence = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # ← Nuevo campo
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name="detections")

    def __str__(self):
        return f"Detection {self.detectionId} for child {self.child.childName}"

#Reset password code
class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)  # Código de 6 dígitos
    created_at = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()  # Tiempo de expiración

    def __str__(self):
        return f"Password reset code for {self.user.username}"

#Notificaciones
class Notification(models.Model):
    notificationTitle = models.CharField(max_length=255)
    notificationDescription = models.TextField()
    notificationDate = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")

    def __str__(self):
        return f"{self.notificationTitle} for {self.user.username}"


#Verification code
class VerificationCode(models.Model):
    phone = models.CharField(max_length=15)  # Cambiado de user a phone
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()  # Tiempo de expiración del código

    def __str__(self):
        return f"Verification code for {self.phone}"


class RecommendationTemplate(models.Model):
    CATEGORY_CHOICES = [
        ('Desnutricion severa', 'Desnutricion severa'),
        ('Normal', 'Normal'),
        ('Riesgo desnutricion', 'Riesgo desnutricion'),
    ]
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    message = models.TextField()  # Mensaje de la recomendación

    def __str__(self):
        return f"Recommendation for {self.category}: {self.message[:30]}"  # Muestra los primeros 30 caracteres


class ImmediateRecommendation(models.Model):
    inmediateRecomId = models.AutoField(primary_key=True)
    detection = models.OneToOneField(MalnutritionDetection, on_delete=models.CASCADE, related_name="immediate_recommendation")
    inmediateRecomMessage = models.TextField()  # Mensaje de la recomendación inmediata

    def __str__(self):
        return f"Immediate recommendation for detection {self.detection.detectionId}"


class GrowthHistory(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name="growth_history")
    date_recorded = models.DateField(auto_now_add=True)  # Fecha de registro
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # Peso en kg
    height = models.DecimalField(max_digits=5, decimal_places=2)  # Altura en cm

    def __str__(self):
        return f"Growth record for {self.child.childName} on {self.date_recorded}"
    
class NutritionTip(models.Model):
    title = models.CharField(max_length=100)  # Título breve del consejo
    description = models.TextField()  # Descripción detallada del consejo
    calories = models.IntegerField(null=True, blank=True)  # Calorías opcionales
    portion_size = models.CharField(max_length=50, blank=True)  # Tamaño de la porción
    image_url = models.URLField(max_length=255, blank=True)  # Enlace de imagen de S3
    date_created = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    # Nuevo campo
    tipo = models.CharField(
        max_length=50,
        choices=[
            ('Nutrición', 'Nutrición'),
            ('Hidratación', 'Hidratación'),
            ('Alimentación', 'Alimentación'),
        ],
        default='Nutrición'
    )

    def __str__(self):
        return self.title

class NutritionalTerm(models.Model):
    name = models.CharField(max_length=100)  # Nombre del término nutricional
    description = models.TextField()  # Descripción del término
    examples = models.TextField()  # Ejemplos de alimentos
    image_url = models.URLField(max_length=255, blank=True)  # URL de imagen para representación visual

    def __str__(self):
        return self.name


#tablas para datos estaticos

class AppInfo(models.Model):
    appName = models.CharField(max_length=100, default="NutriScan")
    appVersion = models.CharField(max_length=10, default="1.0.0")
    developer = models.CharField(max_length=100, default="Equipo de NutriScan")
    description = models.TextField(
        default="Esta aplicación tiene como objetivo ayudar a los padres a monitorear la nutrición infantil y mejorar la calidad de vida."
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación automática
    updated_at = models.DateTimeField(auto_now=True)      # Fecha de actualización automática

    def __str__(self):
        return f"{self.appName} - {self.appVersion}"

class Feedback(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback de {self.user.username}"

class PrivacyPolicy(models.Model):
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Política de Privacidad - {self.date_modified.strftime("%d/%m/%Y")}'

class TermsAndConditions(models.Model):
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Términos y Condiciones - {self.date_modified.strftime("%d/%m/%Y")}'