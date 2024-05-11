from typing import Dict, Iterable, Type

from django.db.models.base import Model
from django.db.models import QuerySet
from rest_framework.serializers import Serializer

from .models import (Chair, Course, Department, EvaluationTest, Lecture, Major, Module, Person, Program, Practice,
                     Subject, Student, StudentResult, StudyGroup, Teacher, QuestionSection, QuestionAnswers)
from .serializers import (ChairSerializer, CourseSerializer, DepartmentSerializer, EvaluationTestSerializer,
                          LectureSerializer, MajorSerializer, ModuleSerializer, PersonSerializer, ProgramSerializer,
                          PracticeSerializer, SubjectSerializer, StudentSerializer, StudentResultSerializer,
                          StudyGroupSerializer, TeacherSerializer, QuestionSectionSerializer, QuestionAnswersSerializer)


class BaseService:
    def __init__(self, model: Type[Model], serializer: Type[Serializer]):
        self.__model__ = model
        self.__serializer__ = serializer

    def get(self, pk: int) -> Type[Model] | None:
        model_obj: Model = self.__model__.objects.filter(pk=pk).first()
        return self.__serializer__(model_obj).data if model_obj else None

    def list(self) -> QuerySet[Model] | None:
        model_obj_list: QuerySet[Model] = self.__model__.objects.all()
        return self.__serializer__(model_obj_list, many=True).data if len(model_obj_list) != 0 else None

    def create(self, request_data) -> Type[Model]:
        serializer = self.__serializer__(data=request_data)

        if serializer.is_valid(raise_exception=True):
            return self.__model__.objects.create(**serializer.validated_data)

    def update(self, pk: int, request_data) -> int:
        serializer = self.__serializer__(data=request_data, partial=True)

        if serializer.is_valid(raise_exception=True):
            return self.__model__.objects.filter(pk=pk).update(**serializer.validated_data)

    def delete(self, pk: int):
        return self.__model__.objects.get(pk=pk).delete()

    @property
    def serializer(self) -> Type[Serializer]:
        return self.__serializer__


class ChairService(BaseService):
    def __init__(self):
        super().__init__(Chair, ChairSerializer)


class CourseService(BaseService):
    def __init__(self):
        super().__init__(Course, CourseSerializer)


class DepartmentService(BaseService):
    def __init__(self):
        super().__init__(Department, DepartmentSerializer)


class EvaluationTestService(BaseService):
    def __init__(self):
        super().__init__(EvaluationTest, EvaluationTestSerializer)


class LectureService(BaseService):
    def __init__(self):
        super().__init__(Lecture, LectureSerializer)


class MajorService(BaseService):
    def __init__(self):
        super().__init__(Major, MajorSerializer)


class ModuleService(BaseService):
    def __init__(self):
        super().__init__(Module, ModuleSerializer)


class PersonService(BaseService):
    def __init__(self):
        super().__init__(Person, PersonSerializer)


class ProgramService(BaseService):
    def __init__(self):
        super().__init__(Program, ProgramSerializer)


class PracticeService(BaseService):
    def __init__(self):
        super().__init__(Practice, PracticeSerializer)


class SubjectService(BaseService):
    def __init__(self):
        super().__init__(Subject, SubjectSerializer)


class StudentService(BaseService):
    def __init__(self):
        super().__init__(Student, StudentSerializer)


class StudentResultService(BaseService):
    def __init__(self):
        super().__init__(StudentResult, StudentResultSerializer)


class StudyGroupService(BaseService):
    def __init__(self):
        super().__init__(StudyGroup, StudyGroupSerializer)


class TeacherService(BaseService):
    def __init__(self):
        super().__init__(Teacher, TeacherSerializer)


class QuestionSectionService(BaseService):
    def __init__(self):
        super().__init__(QuestionSection, QuestionSectionSerializer)


class QuestionAnswersService(BaseService):
    def __init__(self):
        super().__init__(QuestionAnswers, QuestionAnswersSerializer)
