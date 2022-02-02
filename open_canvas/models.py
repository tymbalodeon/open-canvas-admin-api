from operator import attrgetter

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import (
    CASCADE,
    CharField,
    EmailField,
    ForeignKey,
    IntegerField,
    ManyToManyField,
    Model,
)

from open_canvas.canvas.api import get_canvas
from open_canvas.canvas.users import get_first_and_last_names, get_user_by_email

UNPUBLISHED = "UNPUBLISHED"
AVAILABLE = "AVAILABLE"
COMPLETED = "COMPLETED"
DELETED = "DELETED"
WORKFLOW_STATES = [
    (UNPUBLISHED, "unpublished"),
    (AVAILABLE, "available"),
    (COMPLETED, "completed"),
    (DELETED, "deleted"),
]


class Course(Model):
    canvas_id = IntegerField(primary_key=True)
    name = CharField(max_length=255)
    course_code = CharField(max_length=255, blank=True, null=True)
    workflow_state = CharField(
        max_length=11, choices=WORKFLOW_STATES, blank=True, null=True
    )
    course_section = ForeignKey(
        "self", on_delete=CASCADE, blank=True, null=True, related_name="course"
    )

    def __str__(self):
        course_code = f"{self.course_code} " if self.course_code else ""
        return f'{course_code}"{self.name}" ({self.canvas_id})'


class Enrollment(Model):
    STUDENT = "STUDENT"
    STUDENT_VIEW = "STUDENT_VIEW"
    TEACHER = "TEACHER"
    TA = "TA"
    DESIGNER = "DESIGNER"
    OBSERVER = "OBSERVER"
    ROLES = [
        (STUDENT, "StudentEnrollment"),
        (STUDENT_VIEW, "StudentViewEnrollment"),
        (TEACHER, "TeacherEnrollment"),
        (TA, "TaEnrollment"),
        (DESIGNER, "DesignerEnrollment"),
        (OBSERVER, "ObserverEnrollment"),
    ]
    course = ManyToManyField(Course)
    course_section = ForeignKey(
        Course, on_delete=CASCADE, blank=True, null=True, related_name="section"
    )
    user = ForeignKey("CanvasUser", on_delete=CASCADE)
    role = CharField(max_length=21, choices=ROLES)


def get_login_type(login_id):
    try:
        validate_email(login_id)
        return CanvasUser.EMAIL
    except ValidationError:
        return CanvasUser.PENN_PATH


class CanvasUser(Model):
    PENN_PATH = "PENNPATH"
    EMAIL = "EMAIL"
    LOGIN_TYPES = [(PENN_PATH, "PennPath"), (EMAIL, "email")]
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    email = EmailField(primary_key=True)
    penn_key = CharField(max_length=255, unique=True, blank=True, null=True)
    canvas_id = IntegerField(unique=True)
    enrollments = ManyToManyField(Enrollment, related_name="users", blank=True)
    login_type = CharField(max_length=8, choices=LOGIN_TYPES, default=EMAIL)

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def sortable_name(self):
        return f"{self.last_name}, {self.first_name}"

    @property
    def login_id(self):
        return self.penn_key if self.login_type == self.PENN_PATH else self.email

    def sync_with_canvas(self):
        user = get_canvas().get_user(get_user_by_email(self.email))
        canvas_id, name, login_id = attrgetter("id", "name", "login_id")(user)
        self.canvas_id = canvas_id
        if name != self.full_name:
            first_name, last_name = get_first_and_last_names(name)
            self.first_name = first_name
            self.last_name = last_name
        self.login_type = get_login_type(login_id)
        self.save()
