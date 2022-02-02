from canvas.api import get_canvas
from canvas.constants import ACCOUNT

from open_canvas.canvas.users import get_first_and_last_names
from open_canvas.models import CanvasUser, Course, Enrollment, get_login_type


def sync_courses(test=False, account=ACCOUNT):
    canvas = get_canvas(test)
    account = canvas.get_account(account)
    courses = account.get_courses()
    for course in courses:
        try:
            course_object = Course.objects.update_or_create(
                canvas_id=course.id,
                defaults={
                    "name": course.name,
                    "course_code": course.sis_course_id,
                    "workflow_state": course.workflow_state,
                },
            )[0]
        except Exception:
            print(f'- ERROR: failed to create course "{course}"')
            continue
        enrollments = [enrollment for enrollment in course.get_enrollments()]
        for enrollment in enrollments:
            try:
                user = CanvasUser.objects.get(canvas_id=enrollment.user_id)
            except CanvasUser.DoesNotExist:
                user = canvas.get_user(enrollment.user_id)
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
                    user = CanvasUser.objects.create(user_data)[0]
                except Exception:
                    print(f'- ERROR: failed to create user "{user}"')
                    continue
            Enrollment.objects.update_or_create(
                course=course_object, user=user, defaults={"role": enrollment.type}
            )
