from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from cnnmodel.validate_image import ValidateImageView
#user
from .views.userViews.UserRegisterView import UserRegisterView
from .views.userViews.UserLoginView import UserLoginView
from .views.userViews.RequestPasswordResetView import RequestPasswordResetView
from .views.userViews.VerifyPasswordResetCodeView import VerifyPasswordResetCodeView
from .views.userViews.ResetPasswordView import ResetPasswordView
from .views.userViews.DeleteAccountView import DeleteAccountView
from .views.userViews.UserProfileUpdateView import UserProfileUpdateView
from .views.userViews.ResendPasswordResetCodeView import ResendPasswordResetCodeView
from .views.userViews.SendWelcomeEmailView import SendWelcomeEmailView
from .views.userViews.UserProfileRetrieveView import UserProfileRetrieveView


from .views.userViews.identityVerification.VerifyCodeView import VerifyCodeView
from .views.userViews.identityVerification.ResendVerificationCodeView import ResendVerificationCodeView

from .views.userViews.identityVerification.GenerateAndSendVerificationCodeView import GenerateAndSendVerificationCodeView

from .views.userViews.UserProfileView import UserProfileView

#child
from .views.child.ListChildrenView import ListChildrenView
from .views.child.RegisterChildView import RegisterChildView
from .views.child.UpdateChildView import UpdateChildView
from .views.child.ChildrenNamesView import ChildrenNamesView
from .views.child.GetChildById import RetrieveChildView

#malnutrition detection
from .views.malnDetecViews.MalnDetection import UploadDetectionImageView
from .views.malnDetecViews.DetectionHistoryView import DetectionHistoryView
from .views.malnDetecViews.GenerateNewPresignedUrlView import GenerateNewPresignedUrlView

#Notifications
from .views.notifications.NotificationView import NotificationView

#inmediate recomendations
from .views.inmediateRecomendations.GenerateRecommendationView import GenerateRecommendationView

#nutritionTips
from .views.nutritionTip.NutritionTipListView import NutritionTipListView

#nutritionalTerms
from .views.nutritionalTerm.NutritionalTermListView import NutritionalTermListView

#Graphics
from .views.graphics.GrowthChartDataView import GrowthChartDataView
from .views.graphics.DetectionCategoryChartView import DetectionCategoryChartView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('child/register/', RegisterChildView.as_view(), name='register_child'),
    path('child/update/<int:pk>/', UpdateChildView.as_view(), name='update_child'),
    path('children/', ListChildrenView.as_view(), name='list_children'),
    path('children/<int:child_id>/', RetrieveChildView.as_view(), name='retrieve_child'),
    path('children/names/', ChildrenNamesView.as_view(), name='children-names'),
    path('detections/upload/<int:child_id>/', UploadDetectionImageView.as_view(), name='upload_detection_image'),
    path('password-reset/request/', RequestPasswordResetView.as_view(), name='request_password_reset'),
    path('password-reset/verify/', VerifyPasswordResetCodeView.as_view(), name='verify_password_reset_code'),
    path('password-reset/reset/', ResetPasswordView.as_view(), name='reset_password'),
    path('password-reset/resend/', ResendPasswordResetCodeView.as_view(), name='resend_password_reset_code'),
    path('notifications/', NotificationView.as_view(), name='notifications'),#falta configurar en EC2 se configura y se prueba
    path('account/delete/', DeleteAccountView.as_view(), name='delete_account'),#falata probar
    path('user/update/', UserProfileUpdateView.as_view(), name='update-user'),
    path('verification/generate-send-code/', GenerateAndSendVerificationCodeView.as_view(), name='generate_send_verification_code'),
    path('verification/verify-code/', VerifyCodeView.as_view(), name='verify_code'),
    path('verification/resend-code/', ResendVerificationCodeView.as_view(), name='resend_verification_code'),
    path('welcome-email/', SendWelcomeEmailView.as_view(), name='send_welcome_email'),#falta configurar el SES y probar 
    path('inmediate-recomedations/<int:child_id>/', GenerateRecommendationView.as_view(), name='inmediate_recomendation'),#falta configurar el SES y probar
    path('growth-chart/<int:child_id>/', GrowthChartDataView.as_view(), name='growth_chart_data'),
    path('detections/chart/<int:child_id>/', DetectionCategoryChartView.as_view(), name='detection_category_chart'),
    path('detections/history/', DetectionHistoryView.as_view(), name='detection_history'),
    path('validate-image/', ValidateImageView.as_view(), name='validate_image'),
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('user/update-info/', UserProfileRetrieveView.as_view(), name='user-update-info'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('generate_presigned_url/<int:detection_id>/', GenerateNewPresignedUrlView.as_view(), name='generate_presigned_url'),
    path('nutrition-tips/', NutritionTipListView.as_view(), name='nutrition-tip-list'),
    path('nutritional-terms/', NutritionalTermListView.as_view(), name='nutritional-terms'),
]
