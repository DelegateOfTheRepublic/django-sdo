from typing import Dict, Iterable, Type

from django.db.models.base import Model
from rest_framework.serializers import Serializer

from .models import (Chair, Course, Department, EvaluationTest, Lecture, Major, Module, Person, Program, Practice,
                     Subject, Student, StudentResult, StudyGroup, Teacher, QuestionSection)
from .serializers import ChairSerializer


class BaseService:
    def __init__(self, model: Type[Model], serializer: Type[Serializer]):
        self.__model__ = model
        self.__serializer__ = serializer

    def get(self, pk: int) -> Type[Model] | None:
        return self.__model__.objects.filter(pk=pk).first()

    def list(self):
        return self.__model__.objects.all()

    def create(self, request_data) -> Type[Model] | Dict:
        serializer = self.__serializer__(data=request_data)

        if serializer.is_valid():
            return self.__model__.objects.create(**serializer.validated_data)

        return serializer.errors

    def update(self, pk: int, request_data) -> int:
        serializer = self.__serializer__(data=request_data, partial=True)

        if serializer.is_valid():
            return self.__model__.objects.filter(pk=pk).update(**serializer.validated_data)

        return -1

    def delete(self, pk: int):
        self.__model__.objects.get(pk=pk).delete()


class ChairService(BaseService):
    def __init__(self):
        super().__init__(Chair, ChairSerializer)
