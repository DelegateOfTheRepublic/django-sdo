import os.path
import shutil
from typing import Dict, Iterable, Type, List, Union

from django.db.models.base import Model
from django.db.models import QuerySet, Q
from rest_framework.serializers import Serializer

from sdo_core.settings import BASE_DIR, MEDIA_DIR
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

    def get(self, pk: int) -> Model | None:
        model_obj: Model = self.__model__.objects.filter(pk=pk).first()
        return model_obj

    def list(self) -> dict | None:
        model_obj_list: QuerySet[Model] = self.__model__.objects.all()
        return self.to_serialize(model_obj_list) if len(model_obj_list) != 0 else None

    def create(self, request_data) -> Model:
        serializer = self.__serializer__(data=request_data)

        if serializer.is_valid(raise_exception=True):
            return self.__model__.objects.create(**serializer.validated_data)

    def create_many(self, request_data) -> List[Model]:
        serializer = self.__serializer__(data=request_data, many=True)

        if serializer.is_valid(raise_exception=True):
            return self.__model__.objects.bulk_create([self.__model__(**validated_data)
                                                       for _, validated_data in enumerate(serializer.validated_data)])

    def update(self, pk: int, request_data) -> int:
        serializer = self.__serializer__(data=request_data, partial=True)

        if serializer.is_valid(raise_exception=True):
            return self.__model__.objects.filter(pk=pk).update(**serializer.validated_data)

    def delete(self, pk: int, request_data=None):
        return self.__model__.objects.get(pk=pk).delete()

    def validate_data(self, data) -> dict:
        model_serializer = self.__serializer__(data=data, many=isinstance(data, list))

        if model_serializer.is_valid(raise_exception=True):
            return model_serializer.validated_data

    def to_serialize(self, data: Union[Model, QuerySet[Model]]):
        return self.__serializer__(data, many=isinstance(data, QuerySet)).data

    def is_exist(self, pk: int) -> bool:
        return self.__model__.objects.filter(pk=pk).exists()

    @property
    def serializer(self) -> Type[Serializer]:
        return self.__serializer__

    @property
    def serializer_data(self):
        return self.__serializer__.data

    @property
    def serializer_validated_data(self):
        return self.__serializer__.validated_data


class ChairService(BaseService):
    def __init__(self):
        super().__init__(Chair, ChairSerializer)


class CourseService(BaseService):
    def __init__(self):
        super().__init__(Course, CourseSerializer)

    def create(self, request_data) -> Model:
        serializer = self.__serializer__(data=request_data)

        if serializer.is_valid(raise_exception=True):
            validated_data: dict = serializer.validated_data
            majors: list = validated_data.pop('majors')
            modules: list = validated_data.pop('modules')
            members: list = validated_data.pop('members')

            validated_data['title'] += f' для {', '.join([major.__str__() for major in majors])}'
            course: Course = Course.objects.create(**validated_data)
            course.majors.set(majors)
            course.modules.set(modules)
            course.members.set(members)

            return course

    def update(self, pk: int, request_data) -> int:
        data: dict = {**request_data}
        majors: list = data.pop('majors', [])
        modules: list = data.pop('modules', [])
        members: list = data.pop('members', [])

        course = Course.objects.get(pk=pk)
        course.majors.add(*majors)
        course.modules.add(*modules)
        course.members.add(*members)
        return super().update(pk, data)

    def delete(self, pk: int, request_data=None):
        course: Course = self.__model__.objects.get(pk=pk)
        majors_to_del: list = request_data.get('majors', [])
        modules_to_del: list = request_data.get('modules', [])
        members_to_del: list = request_data.get('members', [])

        if len(majors_to_del) != 0 or len(modules_to_del) != 0 or len(members_to_del) != 0:
            course.majors.remove(*majors_to_del)
            course.modules.remove(*modules_to_del)
            course.members.remove(*members_to_del)
        else:
            shutil.rmtree(os.path.join(MEDIA_DIR / 'courses', course.title))
            course.delete()


class DepartmentService(BaseService):
    def __init__(self):
        super().__init__(Department, DepartmentSerializer)


class EvaluationTestService(BaseService):
    def __init__(self):
        super().__init__(EvaluationTest, EvaluationTestSerializer)

    def check(self, student_id: int, evaluation_test_id: int, answers: list) -> float:
        student_score: float = 0.0
        eval_test_answers: QuerySet[QuestionAnswers] = EvaluationTest.objects.get(pk=evaluation_test_id).answers
        student: Student = Student.objects.get(pk=student_id)

        for _, answer in enumerate(answers):
            if isinstance(answer['answer'], list):
                for answer_id in answer['answer']:
                    eval_test_answer: QuestionAnswers = eval_test_answers.filter(pk=answer_id,
                                                                                 question_section_id=
                                                                                 answer['question_section']).first()

                    if eval_test_answer:
                        student_score += eval_test_answer.score

                continue

            eval_test_answer: QuestionAnswers = eval_test_answers.filter(pk=answer['answer'],
                                                                         question_section_id=answer['question_section']
                                                                         ).first()

            if eval_test_answer:
                student_score += eval_test_answer.score

        student_result: StudentResult = StudentResult.objects.filter(student_id=student_id,
                                                                     evaluation_test_id=evaluation_test_id).last()
        if student_result:
            StudentResult.objects.create(student=student_result.student, is_completed=True, score=student_score,
                                         evaluation_test=student_result.evaluation_test,
                                         attempt=student_result.attempt + 1)
        else:
            StudentResult.objects.create(student=student, is_completed=True, score=student_score,
                                         evaluation_test=self.get(evaluation_test_id))

        return student_score


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

    def check(self, student_id: int, practice_id: int, score: float):
        student: Student = Student.objects.get(pk=student_id)

        student_result: StudentResult = StudentResult.objects.filter(student_id=student_id,
                                                                     practice_id=practice_id).last()
        if student_result:
            StudentResult.objects.create(student=student_result.student, is_completed=True, score=score,
                                         practice=student_result.practice,
                                         attempt=student_result.attempt + 1)
        else:
            StudentResult.objects.create(student=student, is_completed=True, score=score,
                                         evaluation_test=self.get(practice_id))


class SubjectService(BaseService):
    def __init__(self):
        super().__init__(Subject, SubjectSerializer)


class StudentService(BaseService):
    def __init__(self):
        super().__init__(Student, StudentSerializer)


class StudentResultService(BaseService):
    def __init__(self):
        super().__init__(StudentResult, StudentResultSerializer)

    def get_final_result(self, student_id: int = None, evaluation_test_id: int = None, practice_id: int = None) -> int | None:
        if evaluation_test_id:
            return EvaluationTest.objects.get(pk=evaluation_test_id).get_final_attempt(student_id)

        return Practice.objects.get(pk=practice_id).get_final_attempt(student_id)

    def get_by(self, **kwargs) -> QuerySet[Model] | None:
        if kwargs.get('evaluation_test_id'):
            return StudentResult.objects.filter(evaluation_test_id=kwargs.get('evaluation_test_id'))
        elif kwargs.get('practice_id'):
            return StudentResult.objects.filter(practice_id=kwargs.get('practice_id'))
        elif kwargs.get('student'):
            if kwargs.get('evaluation_test'):
                return StudentResult.objects.filter(student_id=kwargs.get('student'),
                                                    evaluation_test_id=kwargs.get('evaluation_test'))
            elif kwargs.get('practice'):
                return StudentResult.objects.filter(student_id=kwargs.get('student'),
                                                    practice_id=kwargs.get('practice'))

        return None


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

    def update(self, pk: int, request_data) -> int:
        if not request_data['is_correct']:
            request_data['score'] = 0.0

        return super().update(pk, request_data)
