from rest_framework import serializers
from .models import (Chair, Course, Department, EvaluationTest, Lecture, Major, Module, Person, Program, Practice,
                     Subject, StudentResult, StudyGroup, Teacher, QuestionSection)


class ChairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chair
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    chair = ChairSerializer()

    class Meta:
        model = Department
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class ProgramSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = Program
        fields = '__all__'


class MajorSerializer(serializers.ModelSerializer):
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
    department = DepartmentSerializer()

    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'email', 'department', 'position']


class StudyGroupSerializer(serializers.ModelSerializer):
    major = MajorSerializer()

    class Meta:
        model = StudyGroup
        fields = ['id', 'name', 'major', 'education_degree']


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'


class PracticeSerializer(serializers.ModelSerializer):
    by_lecture = LectureSerializer()
    by_module = ModuleSerializer()

    class Meta:
        model = Practice
        fields = ['id', 'title', 'max_score', 'by_lecture', 'by_module', 'description', 'deadline_date']


class CourseSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    majors = serializers.PrimaryKeyRelatedField(many=True, queryset=Major.objects.all())
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=Person.objects.all())
    modules = serializers.PrimaryKeyRelatedField(many=True, queryset=Module.objects.all())

    class Meta:
        model = Course
        fields = ['id', 'title', 'teacher', 'majors', 'evaluation_criteria', 'members', 'modules']


class EvaluationTestSerializer(serializers.ModelSerializer):
    by_lecture = LectureSerializer()
    by_module = ModuleSerializer()
    by_course = CourseSerializer()

    class Meta:
        model = EvaluationTest
        fields = ['id', 'title', 'by_course', 'by_lecture', 'by_module', 'max_score', 'question_sections',
                  'deadline_date', 'start_time', 'end_time', 'allowed_attempts', 'complete_time']


class StudentResultSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    practice = PracticeSerializer()
    evaluation_test = EvaluationTestSerializer()

    class Meta:
        model = StudentResult
        fields = ['id', 'student', 'practice', 'evaluation_test', 'is_completed', 'answer_file', 'answer_text', 'score',
                  'attempt']


class QuestionSectionSerializer(serializers.ModelSerializer):
    evaluation_test = EvaluationTestSerializer()

    class Meta:
        model = QuestionSection
        fields = ['id', 'evaluation_test', 'max_score', 'question_file']
