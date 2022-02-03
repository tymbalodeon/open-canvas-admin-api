from open_canvas.canvas.api import get_account, get_canvas

from .constants import UNENROLL_TASKS
from .users import get_user_by_email

COURSES_CACHE = {}


def get_canvas_section_or_course(canvas_id, section, test=False):
    if canvas_id in COURSES_CACHE and "section" in COURSES_CACHE[canvas_id]:
        return COURSES_CACHE[canvas_id]["section"]
    else:
        try:
            canvas = get_canvas(test)
            canvas_section = (
                canvas.get_section(canvas_id)
                if section
                else canvas.get_course(canvas_id)
            )
        except Exception:
            canvas_section = "course not found"
        COURSES_CACHE[canvas_id] = dict()
        COURSES_CACHE[canvas_id]["section"] = canvas_section
        return canvas_section


def get_enrollment_login(enrollment, test=False):
    canvas = get_canvas(test)
    user = canvas.get_user(enrollment.user["id"])
    return {
        "enrollment": enrollment,
        "login_id": user.login_id.lower() if user.login_id else "",
        "email": user.email.lower() if user.email else "",
    }


def get_enrollments(canvas_id, canvas_section, test=False):
    if canvas_id in COURSES_CACHE and "enrollments" in COURSES_CACHE[canvas_id]:
        return COURSES_CACHE[canvas_id]["enrollments"]
    else:
        try:
            enrollments = [
                enrollment for enrollment in canvas_section.get_enrollments()
            ]
            enrollments = [
                get_enrollment_login(enrollment, test) for enrollment in enrollments
            ]
        except Exception:
            enrollments = []
        COURSES_CACHE[canvas_id]["enrollments"] = enrollments
        return enrollments


def get_enrollment_by_email(email, enrollments):
    email = email.lower()
    return next(
        (
            enrollment
            for enrollment in enrollments
            if enrollment["login_id"].lower() == email
            or enrollment["email"].lower() == email
        ),
        None,
    )


def enroll_user(email, canvas_id, section, notify, test=False):
    user = get_user_by_email(get_account(test), email)
    canvas_section = get_canvas_section_or_course(canvas_id, section, test)
    if canvas_section == "course not found":
        return canvas_section, canvas_id, ""
    try:
        enrollment = canvas_section.enroll_user(user, enrollment={"notify": notify})
        return "enrolled", enrollment, ""
    except Exception as error:
        try:
            error_message = error.message
        except Exception:
            error_message = error
        return "failed to enroll", canvas_section, error_message


def unenroll_user(email, canvas_id, section, task="conclude", test=False):
    task = task.lower() if task in UNENROLL_TASKS else "conclude"
    canvas_section = get_canvas_section_or_course(canvas_id, section, test)
    if not canvas_section or canvas_section == "course not found":
        return canvas_section, canvas_id
    try:
        enrollments = get_enrollments(canvas_id, canvas_section, test)
        enrollment = get_enrollment_by_email(email, enrollments)
    except Exception:
        enrollment = None
    if not enrollment:
        return "enrollment not found", canvas_section
    else:
        try:
            unenrollment = enrollment["enrollment"].deactivate(task)
            return "unenrolled", unenrollment
        except Exception:
            return "failed to unenroll", enrollment
