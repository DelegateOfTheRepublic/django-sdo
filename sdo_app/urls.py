from django.urls import re_path

from sdo_app.views import ChairAPIView, SubjectAPIView, DepartmentAPIView, ProgramAPIView, MajorAPIView, StudentAPIView, \
    TeacherAPIView, StudyGroupAPIView

urlpatterns = [
    re_path(r'^chairs/', ChairAPIView.as_view(), name='chair-list'),
    re_path(r'^chairs/<id:int>', ChairAPIView.as_view(), name='chair-detail'),
    re_path(r'^subjects/', SubjectAPIView.as_view(), name='subject-list'),
    re_path(r'^subjects/<id:int>', SubjectAPIView.as_view(), name='subject-detail'),
    re_path(r'^departments/', DepartmentAPIView.as_view(), name='department-list'),
    re_path(r'^departments/<id:int>', DepartmentAPIView.as_view(), name='department-detail'),
    re_path(r'^programs/', ProgramAPIView.as_view(), name='program-list'),
    re_path(r'^programs/<id:int>', ProgramAPIView.as_view(), name='program-detail'),
    re_path(r'^majors/', MajorAPIView.as_view(), name='major-list'),
    re_path(r'^majors/<id:int>', MajorAPIView.as_view(), name='major-detail'),
    re_path(r'^students/', StudentAPIView.as_view(), name='student-list'),
    re_path(r'^students/<id:int>', StudentAPIView.as_view(), name='student-detail'),
    re_path(r'^teachers/', TeacherAPIView.as_view(), name='teacher-list'),
    re_path(r'^teachers/<id:int>', TeacherAPIView.as_view(), name='teacher-detail'),
    re_path(r'^study_groups/', StudyGroupAPIView.as_view(), name='study-group-list'),
    re_path(r'^study_groups/<id:int>', StudyGroupAPIView.as_view(), name='study-group-detail'),
]
