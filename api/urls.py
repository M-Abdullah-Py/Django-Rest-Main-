from django.urls import path, include
from . import  views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("employee-viewset", views.EmployeeViewSet, basename="employee-viewset")
router.register('employees-non-viewset', views.EmployeeNonModelViewSet, basename='employees-non-viewset')  # Register your non-model ViewSet


urlpatterns = [
    path('students/', views.StudentsApiSer, name = "students-api" ),
    path('students/<int:pk>', views.StudentDetailsView),
    path("employees/" , views.Employees.as_view()),
    path("employees/<int:pk>", views.EmployeeDetails.as_view()),

    # MIXIN
    path("employees-mixin/", views.EmployeeMixin.as_view()),
    path("employees-details-mixin/<int:pk>", views.EmployeeDetailsMixin.as_view()),


    

    # GENERICS 
    path("employees-generics/", views.EmployeeGeneric.as_view()),
    path("employees-generics/<int:pk>", views.EmployeeDetailsGeneric.as_view()),




    

    # VIEWSET
    path('', include(router.urls)),


    path("blogs/" , views.BLogsView.as_view()),
    path("comments/" , views.CommentsView.as_view()),
    path("reviews/" , views.ReviewsView.as_view()),

    path("blogs/<int:pk>", views.BlogPkView.as_view()),
    path("comments/<int:pk>", views.CommentPkView.as_view()),






          
         
]


