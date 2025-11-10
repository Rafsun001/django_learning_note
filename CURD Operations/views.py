from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from .serializers import ProfileSerializer
from django.contrib.auth.models import User
from .models import UserProfile
import random
import string
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
# Create your views here.

################################################
############## Save Data ##############
################################################
@api_view(['POST'])
def updatedata(request):
    student_class_name = request.data.get("student_class_name")
    student_section = request.data.get("student_section")
    teacher_id  = request.data.get("teacher")
    
    ########## Save method 1 ###########
    StudentClassModel = StudentClass()
    StudentClassModel.student_class_name = student_class_name
    StudentClassModel.student_section = student_section
    StudentClassModel.teacher_id = teacher_id
    StudentClassModel.save()
  
    ########## Save method 2 ###########
    # note = Note.objects.create(student_class_name = student_class_name,student_section =student_section, teacher = teacher )
    # note.save()
   
    return Response(
        {
            "Data": "Worked"
        }, status=201
    )

################################################
########## Fetch Data From Database #############
################################################

############# Method 1 #############
@api_view(['GET'])
def getData_Method_1(request):
    all_notes = Subject.objects.all()

    serializer = Subject(all_notes, many=True)

    return Response(
        {
            "Data": serializer.data
        },
        status=200
    )
############# Method 2 #############
@api_view(['POST'])  # Change GET to POST
def getData_Method_2(request):
    student_email = request.data.get("student_email")
    student_id = request.data.get("student_id")

    # Get full row of the given student_id
    student = Student.objects.get(student_id=student_id)

    # You can return relevant data from the student
    return Response(
        {
            "Dat2": student.student_email,
            "Dat3": student.student_class.student_class_name,
        },
        status=200
    )
    
    
################################################
############## Update Data From ################
################################################
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_profile_data(request):
    user = request.user
    first_name = request.data.get('first_name')
    last_Name = request.data.get('last_Name')
    bio = request.data.get('bio')
    phone = request.data.get('phone')
    image = request.data.get('image')

    marks_tbl = UserProfile.objects.get(user=user)

    marks_tbl.first_Name = first_name
    marks_tbl.last_Name = last_Name
    marks_tbl.bio = bio
    marks_tbl.phone = phone
    if 'image' in request.FILES:
        marks_tbl.image = request.FILES['image']
        
    marks_tbl.save()
    return Response("data_update", status=200)

    
################################################
################ Delete Data ###################
################################################
@api_view(["DELETE"])
def delete_date(request):
    teacher_id = request.data.get("teacher_id")

    note = Teacher.objects.get(teacher_id = teacher_id)
    note.delete()
    return Response(
            {
                "Error": "delete done"
            },
            status=200
        )
