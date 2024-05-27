def course_dir_path(instance, filename) -> str:
    module = instance.module
    course = module.course_modules.all()[0]
    return f'courses/{course}/module_{module}/lecture_{instance}/{filename}'


def answer_file_path(instance, filename) -> str:
    return f'practices/{instance}/{filename}'


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
