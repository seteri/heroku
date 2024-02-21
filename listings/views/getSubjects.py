from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from listings.models.subjects import Subject
from listings.serializers import SubjectSerializer


class GetSubjects(APIView):
    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response({'subjects': serializer.data}, status=status.HTTP_200_OK)