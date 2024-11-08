import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backnutriscan.settings')
django.setup()



from nutriscan.models import RecommendationTemplate  # Cambia 'your_app' al nombre de tu aplicación

# Lista de mensajes de recomendaciones para cada categoría
recommendations_severe = [
    "Consulte al médico de inmediato para atención urgente.",
    "Se recomienda hospitalización para una evaluación completa.",
    "Evite la pérdida de peso adicional, busque ayuda médica ya.",
    "Asegúrese de que el niño reciba atención médica especializada.",
    "Su hijo necesita intervención médica urgente, consulte a un pediatra.",
    "Proporcione alimentos ricos en proteínas y calorías bajo supervisión médica.",
    "Consulte a un nutricionista para un plan de recuperación.",
    "Busque ayuda en el centro de salud más cercano.",
    "Se recomienda iniciar un programa de recuperación nutricional.",
    "Es fundamental que reciba cuidados intensivos.",
    "Evite la deshidratación, consulte a un médico pediatra.",
    "Asegure la ingesta de líquidos y nutrientes esenciales.",
    "Evalúe el entorno para evitar infecciones adicionales.",
    "No intente resolver el problema sin ayuda médica.",
    "Monitoree su peso semanalmente bajo supervisión médica.",
    "Contacte a su centro de salud local inmediatamente.",
    "Haga una cita de emergencia con su proveedor de salud.",
    "Revisar si tiene otras condiciones que agraven su estado.",
    "Asegure un entorno limpio y seguro mientras busca ayuda.",
    "El médico puede sugerir suplementos nutricionales especializados."
]

recommendations_normal = [
    "Felicitaciones, su hijo está saludable. Siga así.",
    "Continúe proporcionando una dieta equilibrada y variada.",
    "Fomente el consumo de frutas y verduras frescas.",
    "Asegúrese de que el niño mantenga una rutina de actividad física.",
    "No olvide incluir proteínas en cada comida.",
    "Hidrátelo bien durante el día, especialmente en actividades físicas.",
    "Evite los azúcares y alimentos procesados para mantener la salud.",
    "Supervise su crecimiento y desarrollo periódicamente.",
    "Asegúrese de que duerma adecuadamente para un desarrollo óptimo.",
    "Brinde alimentos ricos en vitaminas y minerales.",
    "Fomente el consumo de pescado y grasas saludables.",
    "Recuerde programar chequeos regulares con su pediatra.",
    "Evite las bebidas azucaradas y prefiera agua y jugos naturales.",
    "Proporcione una variedad de alimentos para estimular su apetito.",
    "Aliente el consumo de productos lácteos para huesos fuertes.",
    "Limite los snacks y opte por opciones nutritivas.",
    "Recuerde la importancia de las proteínas para su crecimiento.",
    "Siga con una rutina de comida saludable para su bienestar.",
    "Ofrezca alimentos ricos en fibra para mejorar la digestión.",
    "Mantenga un ambiente familiar saludable y positivo."
]

recommendations_risk = [
    "Su hijo está en riesgo de desnutrición. Mejore su alimentación.",
    "Aumente las calorías en su dieta con alimentos saludables.",
    "Visite un nutricionista para obtener una evaluación completa.",
    "Proporcione alimentos ricos en proteínas y calorías.",
    "Asegúrese de que el niño coma frutas y verduras diariamente.",
    "Evite la pérdida de peso innecesaria mediante alimentos nutritivos.",
    "Monitoree su peso semanalmente para observar mejoras.",
    "Asegúrese de que el niño tenga tres comidas y dos meriendas diarias.",
    "Incluya una mayor variedad de alimentos en su dieta.",
    "Considere suplementos vitamínicos según la recomendación médica.",
    "Proporcione alimentos como legumbres, carnes y productos lácteos.",
    "Limite el consumo de alimentos procesados y bebidas azucaradas.",
    "Organice comidas familiares para fomentar el apetito del niño.",
    "Asegure una ingesta adecuada de hierro y calcio.",
    "Anime a su hijo a probar nuevos alimentos saludables.",
    "Mantenga el seguimiento de sus síntomas y cambios.",
    "Refuerce su dieta con alimentos energéticos y nutritivos.",
    "Proporcione meriendas nutritivas y regulares entre comidas.",
    "Evite que se salte las comidas, especialmente el desayuno.",
    "Aumente el consumo de carbohidratos saludables."
]

# Insertar los datos en la base de datos
for message in recommendations_severe:
    RecommendationTemplate.objects.create(category="Desnutricion severa", message=message)

for message in recommendations_normal:
    RecommendationTemplate.objects.create(category="Normal", message=message)

for message in recommendations_risk:
    RecommendationTemplate.objects.create(category="Riesgo desnutricion", message=message)

print("Recomendaciones insertadas correctamente.")
