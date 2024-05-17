from typing import List, Type

from django.db import transaction, IntegrityError
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

        return JsonResponse(self.__model_service__.list(), safe=False)

    def patch(self, request: Request) -> JsonResponse:
        model_id: int | None = request.query_params.get('id', None)

        if not self.__model_service__.is_exist(model_id):
            return JsonResponse({'code': status.HTTP_404_NOT_FOUND})

        upd_status: int = self.__model_service__.update(model_id, request.data)
        return JsonResponse({'code': status.HTTP_200_OK}) if upd_status != 0 \
            else JsonResponse({'code': status.HTTP_400_BAD_REQUEST})

    def delete(self, request: Request) -> JsonResponse:
        model_id: int | None = request.query_params.get('id', None)

        if self.__model_service__.is_exist(model_id):
            self.__model_service__.delete(model_id)

            return JsonResponse({'code': status.HTTP_204_NO_CONTENT})

        return JsonResponse({'code': status.HTTP_404_NOT_FOUND})


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


class StudentResultAPIView(BaseAPIView):
    def __init__(self, *args, **kwargs):
        super().__init__(StudentResultService)


class QuestionSectionAPIView(BaseAPIView):
    def __init__(self, *args, **kwargs):
        super().__init__(QuestionSectionService)


class QuestionAnswersAPIView(BaseAPIView):
    def __init__(self, *args, **kwargs):
        super().__init__(QuestionAnswersService)


class EvaluationTestAPIView(BaseAPIView):
    def __init__(self, *args, **kwargs):
        super().__init__(EvaluationTestService)

    def post(self, request: Request) -> JsonResponse:
        data: dict = {**request.data}

        question_sections: list = data.pop('question_sections', [])

        if len(question_sections) == 0:
            return JsonResponse({'code': status.HTTP_400_BAD_REQUEST})

        try:
            with transaction.atomic():
                e_test_obj = EvaluationTestService().create(data)

                q_section_service = QuestionSectionService()
                for i, question_section in enumerate(question_sections):
                    question_section['evaluation_test'] = e_test_obj.pk
                    q_section_answers = question_section.pop('answers', [])
                    question_sections[i] = q_section_service.create(question_section)

                    for j in range(len(q_section_answers)):
                        q_section_answers[j]['question_section'] = question_sections[i].pk

                    QuestionAnswersService().create_many(q_section_answers)

            return JsonResponse({'code': status.HTTP_201_CREATED,
                                 'evaluation_test': EvaluationTestService().to_serialize(e_test_obj)})
        except IntegrityError as ie:
            return JsonResponse({'code': status.HTTP_400_BAD_REQUEST, 'error_text': ie})


class CourseAPIView(BaseAPIView):
    def __init__(self, *args, **kwargs):
        super().__init__(CourseService)

    def post(self, request: Request) -> JsonResponse:
        pass
