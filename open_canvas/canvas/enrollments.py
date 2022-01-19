from .enroll import find_user_by_email

ACCOUNT = 1
UNENROLL_TASKS = {"conclude", "delete", "deactivate", "inactivate"}
COURSES_CACHE = {}


def get_canvas_section_or_course(canvas, canvas_id, section):
    if canvas_id in COURSES_CACHE and "section" in COURSES_CACHE[canvas_id]:
        return COURSES_CACHE[canvas_id]["section"]
    else:
        try:
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


def get_enrollment_login(enrollment):
    user = CANVAS.get_user(enrollment.user["id"])
    return {
        "enrollment": enrollment,
        "login_id": user.login_id.lower() if user.login_id else "",
        "email": user.email.lower() if user.email else "",
    }


def get_enrollments(canvas, canvas_id, canvas_section):
    if canvas_id in COURSES_CACHE and "enrollments" in COURSES_CACHE[canvas_id]:
        return COURSES_CACHE[canvas_id]["enrollments"]
    else:
        try:
            enrollments = [
                enrollment for enrollment in canvas_section.get_enrollments()
            ]
            enrollments = [
                get_enrollment_login(enrollment) for enrollment in enrollments
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


def enroll_user(canvas, email, canvas_id, section, notify):
    user = find_user_by_email(canvas.get_account(ACCOUNT), email)
    canvas_section = get_canvas_section_or_course(canvas, canvas_id, section)
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


def unenroll_user(canvas, email, canvas_id, section, task="conclude"):
    task = task.lower() if task in UNENROLL_TASKS else "conclude"
    canvas_section = get_canvas_section_or_course(canvas, canvas_id, section)
    if not canvas_section or canvas_section == "course not found":
        return canvas_section, canvas_id
    try:
        enrollments = get_enrollments(canvas, canvas_id, canvas_section)
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
