def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['json']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def validate_lecture_materials_file(value):
    import json
    from django.core.exceptions import ValidationError

    lecture_materials: dict = json.loads(value.file.open('r').read())

    for key in lecture_materials.keys():
        if key not in ['text', 'files', 'links']:
            raise ValidationError(f'Unexpected key \'{key}\', must be \'text\', \'files\', \'links\'.')


def validate_eval_criteria_file(value):
    import json
    from django.core.exceptions import ValidationError

    eval_criteria: dict = json.loads(value.file.open('r').read())

    for key in eval_criteria.keys():
        if key not in ['credit', 'grades']:
            raise ValidationError(f'Unexpected key \'{key}\', must be \'credit\', \'grades\'.')

    for grade_key in eval_criteria['grades'].keys():
        if grade_key not in ['grade_2', 'grade_3', 'grade_4', 'grade_5']:
            raise ValidationError(f'Unexpected key \'{grade_key}\', must be from \'grade_2\' to \'grade_5\'')


def validate_question_file(value):
    import json
    from django.core.exceptions import ValidationError

    question: dict = json.loads(value.file.open('r').read())

    for key in question.keys():
        if key not in ['question', 'answers', 'correct_answers']:
            raise ValidationError(f'Unexpected key \'{key}\', must be \'question\', \'answers\', \'correct_answers\'.')


def validate_deadline_date(value):
    import datetime
    from django.utils import timezone, dateparse
    from django.core.exceptions import ValidationError

    if value < timezone.now().date():
        raise ValidationError('Deadline date cannot be in the past.')

    if value == timezone.now().date():
        raise ValidationError('Deadline date cannot be equal to now.')


def validate_positive_score(value):
    from django.core.exceptions import ValidationError

    if value < 0:
        raise ValidationError('Positive score must be greater than or equal to 0.')

