from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from ...models import AditionalInfoUser

class ConfirmAccountView(TemplateView):
    template_name = "account_confirmation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        aditional_info = get_object_or_404(AditionalInfoUser, user=user)

        if not aditional_info.is_confirmed:
            aditional_info.is_confirmed = True
            aditional_info.save()
            context['message'] = "¡Tu Correo ha sido confirmada exitosamente!. Ahora la aplicación puede enviar correos correctamente"
        else:
            context['message'] = "¡Tu cuenta ya estaba confirmada!"

        return context
