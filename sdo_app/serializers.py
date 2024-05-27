from rest_framework import serializers
from .models import (Chair, Course, Department, EvaluationTest, Lecture, Major, Module, Person, Program, Practice,
                     Subject, StudentResult, StudyGroup, Teacher, QuestionSection, Student, QuestionAnswers)


class ChairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chair
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    chair = serializers.PrimaryKeyRelatedField(queryset=Chair.objects.all())

    class Meta:
        model = Department
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class ProgramSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())

    class Meta:
        model = Program
        fields = '__all__'


class MajorSerializer(serializers.ModelSerializer):
    programs = serializers.PrimaryKeyRelatedField(many=True, queryset=Program.objects.all())

    class Meta:
        model = Major
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Person
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'email']


class StudentSerializer(PersonSerializer):
    pass


class TeacherSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email')
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())

    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'email', 'department', 'position']


class StudyGroupSerializer(serializers.ModelSerializer):
    major = serializers.PrimaryKeyRelatedField(queryset=Major.objects.all())

    class Meta:
        model = StudyGroup
        fields = ['id', 'name', 'major', 'education_degree']


class LectureSerializer(serializers.ModelSerializer):
    module = serializers.PrimaryKeyRelatedField(queryset=Module.objects.all())
    practice = serializers.PrimaryKeyRelatedField(queryset=Practice.objects.all(), required=False)
    evaluation_test = serializers.PrimaryKeyRelatedField(queryset=EvaluationTest.objects.all(), required=False)

    class Meta:
        model = Lecture
        fields = ['id', 'title', 'is_read', 'deadline_date', 'materials', 'module', 'practice', 'evaluation_test']


class ModuleSerializer(serializers.ModelSerializer):
    lectures = LectureSerializer('lectures', many=True, read_only=True)
    practice = serializers.PrimaryKeyRelatedField(queryset=Practice.objects.all(), required=False)
    evaluation_test = serializers.PrimaryKeyRelatedField(queryset=EvaluationTest.objects.all(), required=False)

    class Meta:
        model = Module
        fields = ['id', 'title', 'lectures', 'practice', 'evaluation_test']


class PracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practice
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    practice = serializers.PrimaryKeyRelatedField(queryset=Practice.objects.all(), required=False)
    evaluation_test = serializers.PrimaryKeyRelatedField(queryset=EvaluationTest.objects.all(), required=False)

    class Meta:
        model = Course
        fields = ['id', 'title', 'teacher', 'majors', 'evaluation_criteria', 'members', 'modules', 'practice',
                  'evaluation_test']


class EvaluationTestSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField('get_answers')

    class Meta:
        model = EvaluationTest
        fields = ['id', 'title', 'max_score', 'deadline_date', 'start_time', 'end_time',
                  'allowed_attempts', 'complete_time', 'final_score_is', 'answers']

    def get_answers(self, instance):
        return QuestionAnswersSerializer(instance.answers, many=True).data


class StudentResultSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    evaluation_test = serializers.PrimaryKeyRelatedField(queryset=EvaluationTest.objects.all(), required=False)
    practice = serializers.PrimaryKeyRelatedField(queryset=Practice.objects.all(), required=False)

    class Meta:
        model = StudentResult
        fields = ['id', 'student', 'evaluation_test', 'practice', 'is_completed', 'answer_file', 'answer_text', 'score',
                  'attempt']


class QuestionSectionSerializer(serializers.ModelSerializer):
    evaluation_test = serializers.PrimaryKeyRelatedField(queryset=EvaluationTest.objects.all())
    answers = serializers.SerializerMethodField('get_answers', read_only=True)

    class Meta:
        model = QuestionSection
        fields = ['id', 'evaluation_test', 'question', 'answers']

    def get_answers(self, obj: QuestionSection):
        return QuestionAnswersSerializer(obj.answers, many=True).data


class QuestionAnswersSerializer(serializers.ModelSerializer):
    question_section = serializers.PrimaryKeyRelatedField(queryset=QuestionSection.objects.all())
    is_correct = serializers.BooleanField(write_only=True)
    score = serializers.FloatField(write_only=True)

    class Meta:
        model = QuestionAnswers
        fields = ['id', 'question_section', 'answer', 'is_correct', 'score']


class TQuestionAnswersSerializer(serializers.ModelSerializer):
    question_section = serializers.PrimaryKeyRelatedField(queryset=QuestionSection.objects.all())

    class Meta:
        model = QuestionAnswers
        fields = ['id', 'question_section', 'answer', 'is_correct', 'score']
