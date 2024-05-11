from typing import List, Type
from django.http import JsonResponse, QueryDict
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from .services import (ChairService, CourseService, DepartmentService, EvaluationTestService, LectureService,
                       MajorService, ModuleService, PersonService, ProgramService, PracticeService, SubjectService,
                       StudentResultService, StudyGroupService, StudentService, TeacherService, QuestionSectionService,
                       QuestionAnswersService, BaseService)


class BaseAPIView(APIView):
    def __init__(self, service: Type[BaseService], *args, **kwargs):
        self.__model_service__: BaseService = service()
        super().__init__(*args, **kwargs)

    def get(self, request: Request) -> JsonResponse:
        model_id: int | None = request.query_params.get('id', None)

        if model_id:
            model_obj = self.__model_service__.get(pk=model_id)
            if model_obj is None:
                return JsonResponse({'code': status.HTTP_404_NOT_FOUND})
            return JsonResponse(self.__model_service__.serializer(model_obj).data, safe=False)

        return JsonResponse(self.__model_service__.serializer(self.__model_service__.list(), many=True).data,
                            safe=False)


class ChairAPIView(BaseAPIView):
    def __init__(self, *args, **kwargs):
        super().__init__(ChairService)


class SubjectAPIView(BaseAPIView):
    def __init__(self, *args, **kwargs):
        super().__init__(SubjectService)


class DepartmentAPIView(BaseAPIView):
    def __init__(self, *args, **kwargs):
        super().__init__(DepartmentService)


class ProgramAPIView(BaseAPIView):
    def __init__(self, *args, **kwargs):
        super().__init__(ProgramService)


class MajorAPIView(BaseAPIView):
    def __init__(self, *args, **kwargs):
        super().__init__(MajorService)


class StudentAPIView(BaseAPIView):
    def __init__(self, *args, **kwargs):
        super().__init__(StudentService)


class TeacherAPIView(BaseAPIView):
    def __init__(self, *args, **kwargs):
        super().__init__(TeacherService)


class StudyGroupAPIView(BaseAPIView):
    def __init__(self, *args, **kwargs):
        super().__init__(StudyGroupService)
