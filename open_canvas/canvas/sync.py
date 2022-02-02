from open_canvas.canvas.users import get_first_and_last_names
from open_canvas.models import CanvasUser, Course, Enrollment, get_login_type
from open_canvas.utils import print_item

from .api import get_canvas
from .constants import ACCOUNT


def sync_courses(test=False, account=ACCOUNT):
    canvas = get_canvas(test)
    account = canvas.get_account(account)
    print(") Getting courses...")
    courses = [course for course in account.get_courses()]
    total = len(courses)
    for index, course in enumerate(courses):
        try:
            course_object, created = Course.objects.update_or_create(
                canvas_id=course.id,
                defaults={
                    "name": course.name,
                    "course_code": course.sis_course_id,
                    "workflow_state": course.workflow_state,
                },
            )
            message = f'{"CREATED" if created else "FOUND"} course {course_object}'
            print_item(index, total, message)
        except Exception as error:
            message = f'ERROR: failed to create course "{course}" ({error})'
            print_item(index, total, message)
            continue
        print(") Getting sections...")
        sections = [section for section in course.get_sections()]
        section_total = len(sections)
        for section_index, section in enumerate(sections):
            try:
                section_object, created = Course.objects.update_or_create(
                    canvas_id=section.id,
                    defaults={
                        "name": section.name,
                        "course_code": course.sis_course_id,
                    },
                )
                message = (
                    f'{"CREATED" if created else "FOUND"} section {section_object}'
                )
                print_item(section_index, section_total, message, prefix="\t*")
            except Exception as error:
                message = f'ERROR: failed to create section "{section}" ({error})'
                print_item(section_index, section_total, message, prefix="\t*")
        print(") Getting enrollments...")
        enrollments = [enrollment for enrollment in course.get_enrollments()]
        enrollment_total = len(enrollments)
        for enrollment_index, enrollment in enumerate(enrollments):
            user_object = None
            user = canvas.get_user(enrollment.user_id)
            try:
                user_object = CanvasUser.objects.get(email=user.email)
                message = f'FOUND user "{user_object}"'
                print_item(enrollment_index, enrollment_total, message, prefix="\t*")
            except CanvasUser.DoesNotExist:
                if not user.email:
                    continue
                try:
                    first_name = user.first_name
                    last_name = user.last_name
                except Exception:
                    first_name, last_name = get_first_and_last_names(user.name)
                login_id = user.login_id
                login_type = get_login_type(login_id)
                user_data = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": user.email,
                    "canvas_id": user.id,
                    "login_type": login_type,
                }
                if login_type == CanvasUser.PENN_PATH:
                    user_data["penn_key"] = login_id
                try:
                    user_object = CanvasUser.objects.create(**user_data)
                    message = f'CREATED user "{user_object}"'
                    print_item(
                        enrollment_index, enrollment_total, message, prefix="\t*"
                    )
                except Exception as error:
                    message = f'ERROR: failed to create user "{user}" ({error})'
                    print_item(
                        enrollment_index, enrollment_total, message, prefix="\t*"
                    )
            if user_object:
                enrollment_data = {"user": user_object}
                section_object = Course.objects.filter(
                    canvas_id=enrollment.course_section_id
                ).first()
                if section_object:
                    enrollment_data["course_section"] = section_object
                enrollment_object = None
                try:
                    enrollment_object, created = Enrollment.objects.update_or_create(
                        defaults={"role": enrollment.type}, **enrollment_data
                    )
                    enrollment_object.course.add(course_object)
                except Exception as error:
                    section_message = (
                        f" and section {section_object}" if section_object else ""
                    )
                    message = (
                        f'ERROR: failed to create enrollment for user "{user_object}"'
                        f' in course "{course_object}"{section_message} ({error})'
                    )
                    print_item(
                        enrollment_index, enrollment_total, message, prefix="\t*"
                    )
                message = (
                    f'{"CREATED" if created else "FOUND"} enrollment'
                    f' {enrollment_object}"'
                )
                print_item(enrollment_index, enrollment_total, message, prefix="\t*")
