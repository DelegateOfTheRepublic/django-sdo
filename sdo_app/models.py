from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.db import models

from validators import *


class Subject(models.Model):
    name = models.CharField(_('Наименование дисциплины'), max_length=100)

    def __str__(self) -> str:
        return self.name


class Chair(models.Model):
    name = models.CharField(_('Наименование института/факультета'), max_length=100)

    def __str__(self) -> str:
        return self.name


class Department(models.Model):
    name = models.CharField(_('Наименование кафедры'), max_length=100)
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
    code = models.CharField(_('Код'), max_length=12)
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
    position = models.CharField(_('Должность'), max_length=100)


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


def course_dir_path(instance, filename) -> str:
    module = instance.module_lectures.all()[0]
    course = module.course_modules.all()[0]
    return f'courses/{course}/module_{module}/lecture_{instance}/{filename}'


def answer_file_path(instance, filename) -> str:
    module = instance.module_lectures.all()[0]
    course = module.course_modules.all()[0]

    if instance.by_lecture:
        return f'courses/{course}/module_{module}/practice_{instance}/lecture_{instance.by_lecture}/{filename}'

    return f'courses/{course}/module_{module}/practice_{instance}/{filename}'


def description_file_path(instance, filename) -> str:
    return answer_file_path(instance, filename)


def question_file_path(instance, filename) -> str:
    evaluation_test = instance.evaluation_test

    if evaluation_test.by_lecture:
        module = evaluation_test.by_lecture.module_lectures.all()[0]
        course = module.course_modules.all()[0]
        return (f'courses/{course}/module_{module}/lecture_{evaluation_test.by_lecture}'
                f'/evaluation_test_{evaluation_test}/{filename}')

    if evaluation_test.by_module:
        course = evaluation_test.by_module.course_modules.all()[0]
        return f'courses/{course}/module_{evaluation_test.by_module}/evaluation_test_{evaluation_test}/{filename}'

    if evaluation_test.by_course:
        return f'courses/{evaluation_test.by_course}/evaluation_test_{evaluation_test}/{filename}'


def eval_criteria_file_path(instance, filename) -> str:
    return f'courses/{instance}/{filename}'


class Lecture(models.Model):
    title = models.TextField(_('Наименование лекции'))
    is_read = models.BooleanField(default=False, verbose_name='Прочтена ли лекция?')
    deadline_date = models.DateField(_('Крайний срок завершения'))
    materials = models.FileField(_('Материалы лекции'), upload_to=course_dir_path, blank=True,
                                 validators=[FileExtensionValidator(['json']), validate_lecture_materials_file])

    def __str__(self) -> str:
        return self.title


class Practice(models.Model):
    title = models.TextField(_('Наименование задания'))
    max_score = models.FloatField(_('Максимальный балл'))
    by_lecture = models.ForeignKey(Lecture, on_delete=models.RESTRICT, blank=True, null=True, verbose_name='По лекции')
    by_module = models.ForeignKey('sdo_app.Module', on_delete=models.RESTRICT, blank=True, null=True,
                                  verbose_name='По модулю')
    description = models.FileField(_('Описание задания'), upload_to=description_file_path,
                                   validators=[FileExtensionValidator(['json'])])
    deadline_date = models.DateField(_('Крайний срок сдачи'))

    def __str__(self) -> str:
        return self.title


class StudentResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.RESTRICT, verbose_name='Студент')
    practice = models.ForeignKey(Practice, on_delete=models.RESTRICT, verbose_name='Задание', blank=True)
    evaluation_test = models.ForeignKey('sdo_app.EvaluationTest', on_delete=models.RESTRICT,
                                        verbose_name='Оценочный тест', blank=True)
    is_completed = models.BooleanField(default=False, verbose_name='Выполнено ли задание?')
    answer_file = models.FileField(_('Ответ на задание в виде файла'), upload_to=answer_file_path,
                                   validators=[FileExtensionValidator(['json'])], blank=True)
    answer_text = models.TextField(_('Ответ на задание в виде текста'), blank=True)
    score = models.FloatField(_('Полученный балл'), blank=True, default=0.0)

    def __str__(self) -> str:
        return f'Ответ студента {self.student} на задание {self.practice}'


class Module(models.Model):
    title = models.CharField(_('Наименование модуля'), max_length=32)
    lectures = models.ManyToManyField(Lecture, related_name='module_lectures', verbose_name='Лекции', blank=True)
    practices = models.ManyToManyField(Practice, related_name='module_practices',
                                       verbose_name='Практические задания/контрольные', blank=True)

    def __str__(self) -> str:
        return self.title


class Course(models.Model):
    title = models.TextField(_('Наименование курса'))
    chair = models.ForeignKey(Chair, on_delete=models.RESTRICT, verbose_name='Институт/факультет')
    department = models.ForeignKey(Department, on_delete=models.RESTRICT, verbose_name='Кафедра')
    teacher = models.ForeignKey(Teacher, on_delete=models.RESTRICT, verbose_name='Преподаватель')
    majors = models.ManyToManyField(Major, related_name='course_majors', verbose_name='Направления подготовки')
    evaluation_criteria = models.FileField(_('Критерии оценивания'), upload_to=eval_criteria_file_path,
                                           validators=[validate_eval_criteria_file])
    members = models.ManyToManyField(Student, related_name='course_members', verbose_name='Участники курса')
    modules = models.ManyToManyField(Module, related_name='course_modules', verbose_name='Модули')

    def __str__(self) -> str:
        return f'{self.title} для {', '.join(major.__str__() for major in self.majors.all())}'


class QuestionSection(models.Model):
    evaluation_test = models.ForeignKey('sdo_app.EvaluationTest', on_delete=models.RESTRICT,
                                        verbose_name='Оценочный тест')
    max_score = models.FloatField(_('Максимальный балл'))
    question_file = models.FileField(_('Вопрос с ответами'), upload_to=question_file_path,
                                     validators=[validate_question_file])

    def __str__(self) -> str:
        return f'Вопрос по тесту {self.evaluation_test}'


class EvaluationTest(models.Model):
    title = models.TextField(_('Наименование оценочной работы'))
    by_course = models.ForeignKey(Course, on_delete=models.RESTRICT, blank=True, verbose_name='По курсу')
    by_lecture = models.ForeignKey(Lecture, on_delete=models.RESTRICT, blank=True, verbose_name='По лекции')
    by_module = models.ForeignKey(Module, on_delete=models.RESTRICT, blank=True, verbose_name='По модулю')
    max_score = models.FloatField(_('Максимальный балл'))
    question_sections = models.ManyToManyField(QuestionSection, related_name='questions', verbose_name='Вопросы')
    deadline_date = models.DateField(_('Крайний срок сдачи'))
    start_time = models.DateTimeField(_('Дата начала оценочной работы студентом'))
    end_time = models.DateTimeField(_('Дата завершения оценочной работы студентом'))
    allowed_attempts = models.IntegerField(_('Разрешенное количество попыток'), default=1)
    student_attempts = models.IntegerField(_('Израсходованно попыток'))
    complete_time = models.IntegerField(_('Время на выполнение(мин.)'))

    def __str__(self) -> str:
        return self.title
