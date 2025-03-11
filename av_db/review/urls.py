from django.urls import path, include
from rest_framework.routers import DefaultRouter

from review.controller.survey_controller import SurveyController

router = DefaultRouter()
router.register(r'review', SurveyController, basename='review')

urlpatterns = [
    #path('', include(router.urls)),
    path('creat-form', SurveyController.as_view({'post': 'createSurveyForm'}), name='review-create-form'),
    path('register-title-description', SurveyController.as_view({'post': 'registerTitleDescription'}), name='register-title-description'),
    path('register-question', SurveyController.as_view({'post': 'registerQuestion'}), name='review-question'),
    path('register-selection', SurveyController.as_view({'post': 'registerSelection'}), name='review-selection'),
    path('review-title-list', SurveyController.as_view({'get': 'surveyList'}), name='review-title-list'),
    path('read-review-form/<str:randomString>', SurveyController.as_view({'get': 'readSurveyForm'}), name='read-review-form'),
    path('submit-review', SurveyController.as_view({'post': 'submitSurvey'}), name='submit-review'),
    path('randomstring',SurveyController.as_view({'post':'pushRandomstring'}),name='push-randomstring'),
    path('review-result/<int:surveyId>', SurveyController.as_view({'get': 'surveyResult'}), name='review-result'),
    path('check-first-submit', SurveyController.as_view({'post': 'checkIsFirstSubmit'}), name='check-first-submit'),
]