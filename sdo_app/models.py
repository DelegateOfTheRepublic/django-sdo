from typing import Union

from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db.models import QuerySet, Q
from django.utils.translation import gettext_lazy as _
from django.db import models

from .utils import course_dir_path, description_file_path, answer_file_path, eval_criteria_file_path
from validators import validate_deadline_date, validate_positive_score, validate_eval_criteria_file


class BaseTask(models.Model):
    class Meta:
        abstract = True

    class FinalScoreIs(models.TextChoices):
        BEST_ATTEMPT = 'BA', 'Лучшаяя попытка'
        LAST_ATTEMPT = 'LA', 'Последняя попытка'

    deadline_date = models.DateField(_('Крайний срок сдачи'), validators=[validate_deadline_date])
    final_score_is = models.CharField(max_length=2, default=FinalScoreIs.BEST_ATTEMPT, choices=FinalScoreIs.choices,
                                      verbose_name='Конечный результат оценивается, как')

    def get_final_attempt(self, student_id: int) -> int | None:
        base_task_filter = Q(**{'evaluation_test_id': self.id}) if isinstance(self, EvaluationTest) \
            else Q(**{'practice_id': self.id})

        student_results: QuerySet[StudentResult] = StudentResult.objects.filter(base_task_filter, student_id=student_id)

        if not student_results:
            return None

        if self.final_score_is == BaseTask.FinalScoreIs.BEST_ATTEMPT:
            return student_results.order_by('-score').first().id

        return student_results.last().id


class Subject(models.Model):
    name = models.CharField(_('Наименование дисциплины'), max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Chair(models.Model):
    name = models.CharField(_('Наименование института/факультета'), max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Department(models.Model):
    name = models.CharField(_('Наименование кафедры'), max_length=100, unique=True)
    chair = models.ForeignKey(Chair, on_delete=models.RESTRICT, verbose_name='Наименование института/факультета')

    def __str__(self) -> str:
        return self.name


class Program(models.Model):
    name = models.CharField(_('Наименование программы подготовки'), max_length=100)
    department = models.ForeignKey(Department, on_delete=models.RESTRICT, verbose_name='Наименование кафедры')

    def __str__(self) -> str:
        return self.name


class Major(models.Model):
    name = models.CharField(_('Наименование направления подготовки'), max_length=100)
    code = models.CharField(_('Код'), max_length=12, unique=True)
    programs = models.ManyToManyField(Program, related_name='major_programs',
                                      verbose_name='Программы подготовки')

    def __str__(self) -> str:
        return f"{self.code} {self.name}"


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(_('Имя'), max_length=100)
    middle_name = models.CharField(_('Фамилия'), max_length=100)
    last_name = models.CharField(_('Отчество'), max_length=100)

    def __str__(self) -> str:
        return f"{self.first_name} {self.middle_name} {self.last_name}"


class Student(Person):
    pass


class Teacher(Person):
    class Position(models.TextChoices):
        PROF = 'PF', 'Профессор'
        DOCENT = 'DC', 'Доцент'
        SENIOR_LECTURER = 'SL', 'Старший преподаватель'
        ASSISTANT = 'AS', 'Ассистент'

    position = models.CharField(_('Должность'), max_length=2, choices=Position.choices, default=Position.DOCENT)
    department = models.ForeignKey(Department, on_delete=models.RESTRICT, verbose_name='Кафедра')


class StudyGroup(models.Model):
    class EducationDegree(models.TextChoices):
        BACHELOR = 'BC', 'Бакалавриат',
        MASTER = 'MS', 'Магистратура',
        SPECIALIST = 'SP', 'Специалитет',
        POSTGRADUATE = 'PG', 'Аспирантура'

    name = models.CharField(_('Наименование учебной группы'), max_length=100)
    major = models.ForeignKey(Major, on_delete=models.RESTRICT, verbose_name='Наименование программы подготовки')
    education_degree = models.CharField(_('Уровень образования'), max_length=32, choices=EducationDegree)

    def __str__(self) -> str:
        return self.name


class Lecture(models.Model):
    title = models.TextField(_('Наименование лекции'))
    is_read = models.BooleanField(default=False, verbose_name='Прочтена ли лекция?')
    deadline_date = models.DateField(_('Крайний срок завершения'), validators=[validate_deadline_date])
    materials = models.FileField(_('Материалы лекции'), upload_to=course_dir_path,
                                 validators=[FileExtensionValidator(['md'])])
    module = models.ForeignKey('sdo_app.Module', on_delete=models.RESTRICT, verbose_name='Модуль')
    practice = models.ForeignKey('sdo_app.Practice', on_delete=models.RESTRICT, blank=True, null=True,
                                 verbose_name='Задание/контрольная работа')
    evaluation_test = models.ForeignKey('sdo_app.EvaluationTest', on_delete=models.RESTRICT, blank=True, null=True,
                                        verbose_name='Оценочный тест')

    def __str__(self) -> str:
        return self.title


class Practice(BaseTask):
    title = models.TextField(_('Наименование задания'))
    max_score = models.FloatField(_('Максимальный балл'), default=0.0, validators=[validate_positive_score])
    description = models.FileField(_('Описание задания'), upload_to=description_file_path,
                                   validators=[FileExtensionValidator(['json'])])

    def __str__(self) -> str:
        return self.title


class StudentResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.RESTRICT, verbose_name='Студент')
    evaluation_test = models.ForeignKey('EvaluationTest', on_delete=models.RESTRICT, verbose_name='Тест', blank=True,
                                        null=True)
    practice = models.ForeignKey('Practice', on_delete=models.RESTRICT, verbose_name='Практическое задание',
                                 blank=True, null=True)
    is_completed = models.BooleanField(default=False, verbose_name='Выполнено ли задание?')
    answer_file = models.FileField(_('Ответ на задание в виде файла'), upload_to=answer_file_path,
                                   validators=[FileExtensionValidator(['json'])], blank=True)
    answer_text = models.TextField(_('Ответ на задание в виде текста'), blank=True)
    score = models.FloatField(_('Полученный балл'), blank=True, default=0.0, validators=[validate_positive_score])
    attempt = models.IntegerField(_('Попытка №'), default=1)

    def __str__(self) -> str:
        to_print: str = f'Результат студента {self.student} по XXX'

        if self.evaluation_test:
            to_print = to_print.replace('XXX', f'тесту {self.evaluation_test}')
        else:
            to_print = to_print.replace('XXX', f'практическому заданию {self.practice}')

        return to_print


class Module(models.Model):
    title = models.CharField(_('Наименование модуля'), max_length=32)
    practice = models.ForeignKey(Practice, on_delete=models.RESTRICT, verbose_name='Контрольная работа',
                                 blank=True, null=True)
    evaluation_test = models.ForeignKey('sdo_app.EvaluationTest', on_delete=models.RESTRICT,
                                        verbose_name='Контрольный тест', blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    @property
    def lectures(self) -> QuerySet[Lecture]:
        return Lecture.objects.filter(module__id=self.id)


class Course(models.Model):
    title = models.TextField(_('Наименование курса'), unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.RESTRICT, verbose_name='Преподаватель')
    majors = models.ManyToManyField(Major, related_name='course_majors', verbose_name='Направления подготовки')
    evaluation_criteria = models.FileField(_('Критерии оценивания'), upload_to=eval_criteria_file_path,
                                           validators=[validate_eval_criteria_file])
    members = models.ManyToManyField(StudyGroup, related_name='course_members', verbose_name='Участники курса',
                                     blank=True)
    modules = models.ManyToManyField(Module, related_name='course_modules', verbose_name='Модули', blank=True)
    practice = models.ForeignKey(Practice, on_delete=models.RESTRICT, blank=True, null=True,
                                 verbose_name='Итоговая работа')
    evaluation_test = models.ForeignKey('sdo_app.EvaluationTest', on_delete=models.RESTRICT, blank=True, null=True,
                                        verbose_name='Итоговый тест')

    def __str__(self) -> str:
        return f'{self.title}'


class QuestionSection(models.Model):
    evaluation_test = models.ForeignKey('sdo_app.EvaluationTest', on_delete=models.CASCADE,
                                        verbose_name='Оценочный тест')
    question = models.TextField(verbose_name='Вопрос')

    def __str__(self) -> str:
        return f'Вопрос по тесту {self.evaluation_test}'

    @property
    def answers(self) -> QuerySet['QuestionAnswers']:
        return QuestionAnswers.objects.filter(question_section_id=self.id)

    @property
    def max_score(self) -> float:
        question_answers: QuerySet[QuestionAnswers] = self.answers
        return sum(question_answer.score for question_answer in question_answers)


class QuestionAnswers(models.Model):
    question_section = models.ForeignKey(QuestionSection, on_delete=models.CASCADE, verbose_name='Блок вопроса')
    answer = models.TextField(verbose_name='Ответ на вопрос')
    is_correct = models.BooleanField(default=False, verbose_name='Это верный ответ')
    score = models.FloatField(default=0.0, verbose_name='Получаемый балл', validators=[validate_positive_score])

    def __str__(self) -> str:
        return f'Ответ на вопрос {self.question_section.question}'


class EvaluationTest(BaseTask):
    title = models.TextField(_('Наименование оценочной работы'))
    start_time = models.DateTimeField(_('Дата начала оценочной работы студентом'), null=True, blank=True)
    end_time = models.DateTimeField(_('Дата завершения оценочной работы студентом'), null=True, blank=True)
    allowed_attempts = models.IntegerField(_('Разрешенное количество попыток'), default=1)
    complete_time = models.IntegerField(_('Время на выполнение(мин.)'))

    def __str__(self) -> str:
        return self.title

    @property
    def answers(self) -> QuerySet[QuestionAnswers]:
        return QuestionAnswers.objects.filter(question_section__evaluation_test_id=self.id, is_correct=True)

    @property
    def max_score(self) -> float:
        question_sections: QuerySet[QuestionSection] = QuestionSection.objects.filter(evaluation_test_id=self.id)

        if not question_sections:
            return 0

        return sum(question_section.max_score for question_section in question_sections)
