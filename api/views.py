from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin , CreateModelMixin , RetrieveModelMixin, UpdateModelMixin,DestroyModelMixin
from rest_framework import status , generics, viewsets
from blogs.models import Blog, Comment, Review
from blogs.serializers import BlogSerializer, CommentSerializer, ReviewSerializer
from .paginations import CustomPagination, CustomLimitOffsetPagination
from employees.filters import EmployeesFilter 
from rest_framework.filters import SearchFilter , OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend



# Create your views here.
# manual serialize and getting static data 
def StudentsAPi(request):
    # for static data 
    # students = {"id":1, "name": "abdullah"}
    students = Student.objects.all()
    print("querry set/", students)


    st = students.values()
    print(st)

    # we are converting querset to list serializing 
    student_list  = list(students.values())
    print(student_list)


    # jsonresponse expect that we will pass the dict by default but wer are passing the list
    # and saying this is safe by writing safe = false 
    return JsonResponse(student_list, safe= False)


# serialization is the way of converting the model objects / query set into the json formate or other 
# that the clients require 

# serializing through serialzer class 
@api_view(['GET', "POST"])
def StudentsApiSer(request):
    if request.method == "GET":
        # student = Student.objects.get(name = "abdullah") # to get single object 
        students = Student.objects.all()
        serializer = StudentSerializer(students, many = True) # Giving fields like id, name , branch 
        
        return Response(serializer.data, status = status.HTTP_200_OK)
    

    # in form we use request.post like 
    # form = StudentForm(request.POST)
    # serializers = StudentSerializers(data = request.data)

    elif request.method == "POST":
        serializer = StudentSerializer(data = request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        



# single object fetching 
@api_view(['GET' ,'PUT', "DELETE"])
def StudentDetailsView(request, pk):
    try:
        student = Student.objects.get(pk = pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = StudentSerializer(student)

        return Response(serializer.data,status= status.HTTP_200_OK)
    
    elif request.method == "PUT":
        serializer = StudentSerializer(student, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == "DELETE":
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    




#------------------------------------
# fetching all the employees and Creating record 
class Employees(APIView):
    def get(self,request):
        employees = Employee.objects.all()
        serializers = EmployeeSerializer(employees, many = True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    

    def post(self,request):
        serializer = EmployeeSerializer(data = request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    

# Get single object other operations 
class EmployeeDetails(APIView):
    def get_object(self,pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Http404
        
    def get(self, request,pk):
        employee = self.get_object(pk)
        print(employee)
        serializers = EmployeeSerializer(employee)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






# MIXINS --------------------------
class EmployeeMixin(ListModelMixin, CreateModelMixin, generics.GenericAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

    def get(self, request):
        return self.list(request)
    
    def post(self,request):
        return self.create(request)


class EmployeeDetailsMixin(RetrieveModelMixin, generics.GenericAPIView, UpdateModelMixin, DestroyModelMixin ):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

    def get(self,request,pk):
        return self.retrieve(request)

    
    def put(self,request,pk):
        return self.update(request)
    
    def delete(self,request,pk):
        return self.destroy(request)


# Genric Views -------------------------------
# ListApiView 
# CreateApiView
# RetrieveApiView
# UpdateApiView
# DestroyApiView

# combination GenericView

# ListCreateApiView
# RetriveUpdateApiView
# RetriveUpdateDestroyApiView


# PRactical-----

class EmployeeGeneric(generics.ListAPIView, generics.CreateAPIView):
# class EmployeeGeneric(generics.ListCreateAPIView): # You can do this too
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    pagination_class = CustomPagination
    # pagination_class = CustomLimitOffsetPagination
    # filterset_fields = ['desgination'] # exact search 
    filterset_class =  EmployeesFilter


# class EmployeeDetailsGeneric(generics.RetrieveAPIView,  generics.UpdateAPIView, generics.DestroyAPIView):
class EmployeeDetailsGeneric(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = "pk"



# VIEWSET ---------------------------------------------------------
class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()



# NON MODEL VIEWSET 
class EmployeeNonModelViewSet(viewsets.ViewSet):
    """
    A ViewSet that interacts with Employee data without directly linking to it as a model viewset.
    """

    def list(self, request):
        """
        List all employees.
        """
        queryset = Employee.objects.all()
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific employee by id (pk).
        """
        try:
            employee = Employee.objects.get(pk=pk)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        Create a new employee.
        """
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Update an existing employee.
        """
        try:
            employee = Employee.objects.get(pk=pk)
            serializer = EmployeeSerializer(employee, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        Delete an employee by id.
        """
        try:
            employee = Employee.objects.get(pk=pk)
            employee.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

    
#------------------------------------- NESTED SERIALIZER 

class BLogsView(generics.ListCreateAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['blog_title', "blog_body", "^blog_title"]
    ordering_fields = ['id', "blog_title"]


class CommentsView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class ReviewsView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()



# PK BASED Nested Serializer 

class BlogPkView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = "pk"


class CommentPkView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "pk"



# PAGINATION -------------------- 
# TWO TYPES OF PAGINATIONS
    # PageNumberPagination 
        # Take pagesize parameter and response accoringly (eg)--> page_size = 10 10 blocks per page

    # LimitOffsetPagination
        # limit --- How many items you want to see per page
        # offset --- from where to start 

# GLOBAL WORKS WITH GENERIC AND VIEWSET
    # JUST APPLY THIS IN THE SETTING 
    # REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 2, 
    # }

    """
    FOR LimitOffPagination
    REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 3, 
}
both works same just a offset diffrence 
no need to include anything in the view if the global is set up 
   """

# CUSTOM 
# using LimitOffsetPagination class for global 
# using PageNumberPagination class for specific model 




# FILTERS -------------- install django filters 
# Global Filters 
# in setting under rest_framework --> 'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
# This means all of our views have support for this filter now 
# u have to use this in the view like this -----> filterset_fields = ['desgination'] # exact search 

# in view
# filterset_fields = ['designation']
# global only works with generics and viewset and mixins  

# custom filter for complete details go to employees app filter 



# search filter 
# ibuilt search class from rest_framework.filters import SearchFilter
# serach_fields = ['blog_title', 'blog_body' , '^blog_title'] ^ is start with 
# filter_backends = [SearchFilter]

# very important if u want to use the searchfilter along with other filter u have to 
# to mention like this ilter_backends = [SearchFilter, DjangoFilterBackend], u have to 
# import the djangofilterbacken from django_filters.rest_framework import DjangoFilterBackend 



# ORDERING FILTER (OrderingFilter) import from where the serach is imported
# takes filter_backends = [OrderingFilter]
# ordering_fields = ['id'] 















