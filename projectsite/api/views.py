from rest_framework import generics

from studentorg.models import College, Program, Student

from .serializers import CollegeSerializer, ProgramSerializer, StudentSerializer


class CollegeListCreateAPIView(generics.ListCreateAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer


class CollegeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer


class ProgramListCreateAPIView(generics.ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


class ProgramDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


class StudentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
