from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from cnnmodel.validate_image_aws_rekognition import ValidateImageView
#user
from .views.userViews.UserRegisterView import UserRegisterView
from .views.userViews.UserLoginView import UserLoginView
from .views.userViews.RequestPasswordResetView import RequestPasswordResetView
from .views.userViews.VerifyPasswordResetCodeView import VerifyPasswordResetCodeView
from .views.userViews.ResetPasswordView import ResetPasswordView
from .views.userViews.DeleteAccountView import DeleteAccountView
from .views.userViews.UserProfileUpdateView import UserProfileUpdateView
from .views.userViews.ResendPasswordResetCodeView import ResendPasswordResetCodeView

from .views.userViews.UserProfileRetrieveView import UserProfileRetrieveView


from .views.userViews.identityVerification.VerifyCodeView import VerifyCodeView
from .views.userViews.identityVerification.ResendVerificationCodeView import ResendVerificationCodeView

from .views.userViews.identityVerification.GenerateAndSendVerificationCodeView import GenerateAndSendVerificationCodeView

from .views.userViews.UserProfileView import UserProfileView

from .views.userViews.ConfirmAccountView import ConfirmAccountView
from .views.userViews.ResendConfirmationEmailView import ResendConfirmationEmailView

#correo par al aconfirmacion de correo
from .views.userViews.ResendVerificationEmal import ResendVerificationEmailView

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
from .views.malnDetecViews.CheckDailyDetectionAPIView import CheckDailyDetectionAPIView


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

#Static Info
from .views.statycInfo.AppInfoView import AppInfoView
from .views.statycInfo.FeedbackView import FeedbackView
from .views.statycInfo.PrivacyPolicyView import PrivacyPolicyView
from .views.statycInfo.TermsAndConditionsView import TermsAndConditionsView

#cerrar sesion
from .views.session.LogoutView import LogoutView

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
    path('account/delete/', DeleteAccountView.as_view(), name='delete_account'),
    path('user/update/', UserProfileUpdateView.as_view(), name='update-user'),
    path('verification/generate-send-code/', GenerateAndSendVerificationCodeView.as_view(), name='generate_send_verification_code'),
    path('verification/verify-code/', VerifyCodeView.as_view(), name='verify_code'),
    path('verification/resend-code/', ResendVerificationCodeView.as_view(), name='resend_verification_code'),
    
    path('inmediate-recomedations/<int:child_id>/', GenerateRecommendationView.as_view(), name='inmediate_recomendation'),

    #Confirmar cuenta
    path('confirmar-cuenta/<int:user_id>/', ConfirmAccountView.as_view(), name='confirmar-cuenta'),

    #Confirmar correo
    path('user/send-verification-email/', ResendVerificationEmailView.as_view(), name='send_verification_email'),

    #Verificamos que se realice una solo deteccion por dia por niño
    path('verification/check-detection-today/<int:child_id>/', CheckDailyDetectionAPIView.as_view(), name='check-detection-today'),


    #statistycs
    path('children/<int:child_id>/growth-chart/', GrowthChartDataView.as_view(), name='growth_chart_data'),
    path('children/<int:child_id>/detection-chart/', DetectionCategoryChartView.as_view(), name='detection_category_chart'),

    path('detections/history/', DetectionHistoryView.as_view(), name='detection_history'),
    path('validate-image/<int:child_id>/', ValidateImageView.as_view(), name='validate_image'),
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('user/update-info/', UserProfileRetrieveView.as_view(), name='user-update-info'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('generate_presigned_url/<int:detection_id>/', GenerateNewPresignedUrlView.as_view(), name='generate_presigned_url'),
    path('nutrition-tips/', NutritionTipListView.as_view(), name='nutrition-tip-list'),
    path('nutritional-terms/', NutritionalTermListView.as_view(), name='nutritional-terms'),
    path('confirmar-cuenta/<int:user_id>/', ConfirmAccountView.as_view(), name='confirm_account'),
    path('resend-confirmation/', ResendConfirmationEmailView.as_view(), name='resend-confirmation'),

    #static Info
    path('app-info/', AppInfoView.as_view(), name='app-info'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('terms-and-conditions/', TermsAndConditionsView.as_view(), name='terms-and-conditions'),

    path('user/logout/', LogoutView.as_view(), name='logout'),
]
