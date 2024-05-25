from django.urls import re_path

from sdo_app.views import (ChairAPIView, SubjectAPIView, DepartmentAPIView, ProgramAPIView, MajorAPIView,
                           StudentAPIView, TeacherAPIView, StudyGroupAPIView, StudentResultAPIView,
                           EvaluationTestAPIView, QuestionAnswersAPIView, QuestionSectionAPIView, CourseAPIView,
                           LectureAPIView, ModuleAPIView)

urlpatterns = [
    re_path(r'^chairs/', ChairAPIView.as_view(), name='chair-list'),
    re_path(r'^chairs/<id:int>', ChairAPIView.as_view(), name='chair-detail'),
    re_path(r'^courses/', CourseAPIView.as_view(), name='course-list'),
    re_path(r'^courses/<id:int>', CourseAPIView.as_view(), name='course-detail'),
    re_path(r'^subjects/', SubjectAPIView.as_view(), name='subject-list'),
    re_path(r'^subjects/<id:int>', SubjectAPIView.as_view(), name='subject-detail'),
    re_path(r'^departments/', DepartmentAPIView.as_view(), name='department-list'),
    re_path(r'^departments/<id:int>', DepartmentAPIView.as_view(), name='department-detail'),
    re_path(r'^programs/', ProgramAPIView.as_view(), name='program-list'),
    re_path(r'^programs/<id:int>', ProgramAPIView.as_view(), name='program-detail'),
    re_path(r'^majors/', MajorAPIView.as_view(), name='major-list'),
    re_path(r'^majors/<id:int>', MajorAPIView.as_view(), name='major-detail'),
    re_path(r'^modules/', ModuleAPIView.as_view(), name='module-list'),
    re_path(r'^modules/<id:int>', ModuleAPIView.as_view(), name='module-detail'),
    re_path(r'^students/', StudentAPIView.as_view(), name='student-list'),
    re_path(r'^students/<id:int>', StudentAPIView.as_view(), name='student-detail'),
    re_path(r'^teachers/', TeacherAPIView.as_view(), name='teacher-list'),
    re_path(r'^teachers/<id:int>', TeacherAPIView.as_view(), name='teacher-detail'),
    re_path(r'^study_groups/', StudyGroupAPIView.as_view(), name='study-group-list'),
    re_path(r'^study_groups/<id:int>', StudyGroupAPIView.as_view(), name='study-group-detail'),
    re_path(r'^student_results/', StudentResultAPIView.as_view(), name='student-result-list'),
    re_path(r'^student_results/<id:int>', StudentResultAPIView.as_view(), name='student-result-detail'),
    re_path(r'^e_tests/', EvaluationTestAPIView.as_view(), name='evaluation-test-list'),
    re_path(r'^e_tests/<id:int>', EvaluationTestAPIView.as_view(), name='evaluation-test-detail'),
    re_path(r'^lectures/', LectureAPIView.as_view(), name='lecture-list'),
    re_path(r'^lectures/<id:int>', LectureAPIView.as_view(), name='lecture-detail'),
    re_path(r'^questions/', QuestionSectionAPIView.as_view(), name='question-section-list'),
    re_path(r'^questions/<id:int>', QuestionSectionAPIView.as_view(), name='question-section-detail'),
    re_path(r'^answers/', QuestionAnswersAPIView.as_view(), name='question-answer-list'),
    re_path(r'^answers/<id:int>', QuestionAnswersAPIView.as_view(), name='question-answer-detail')
]
