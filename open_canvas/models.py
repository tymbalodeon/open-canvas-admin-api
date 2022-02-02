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
    OneToOneField,
)

from open_canvas.canvas.api import get_canvas
from open_canvas.canvas.users import get_user_by_email

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
    course_code = CharField(max_length=50, blank=True, null=True)
    workflow_state = CharField(max_length=11, choices=WORKFLOW_STATES)

    def __str__(self):
        course_code = f"{self.course_code} " if self.course_code else ""
        return f'{course_code}"{self.name}" ({self.canvas_id})'


class Section(Model):
    canvas_id = IntegerField(primary_key=True)
    name = CharField(max_length=255)
    course = ForeignKey(Course, on_delete=CASCADE, related_name="sections")
    workflow_state = CharField(max_length=11, choices=WORKFLOW_STATES)


class Enrollment(Model):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    TA = "TA"
    DESIGNER = "DESIGNER"
    OBSERVER = "OBSERVER"
    ROLES = [
        (STUDENT, "StudentEnrollment"),
        (TEACHER, "TeacherEnrollment"),
        (TA, "TaEnrollment"),
        (DESIGNER, "DesignerEnrollment"),
        (OBSERVER, "ObserverEnrollment"),
    ]
    course = OneToOneField(Course, on_delete=CASCADE)
    section = OneToOneField(Section, on_delete=CASCADE)
    user = OneToOneField("CanvasUser", on_delete=CASCADE)
    role = CharField(max_length=18, choices=ROLES)


class CanvasUser(Model):
    PENN_PATH = "PENNPATH"
    EMAIL = "EMAIL"
    LOGIN_TYPES = [(PENN_PATH, "PennPath"), (EMAIL, "email")]
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    email = EmailField(primary_key=True)
    penn_id = IntegerField(unique=True, blank=True, null=True)
    penn_key = CharField(max_length=10, unique=True, blank=True, null=True)
    canvas_id = IntegerField(unique=True)
    enrollments = ManyToManyField(Enrollment, related_name="users", blank=True)
    login_type = CharField(max_length=8, choices=LOGIN_TYPES)

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
        canvas_user = get_canvas().get_user(get_user_by_email(self.email))
        canvas_id, name, login_id = attrgetter("id", "name", "login_id")(canvas_user)
        self.canvas_id = canvas_id
        if name != self.full_name:
            first_name, last_name = name.split()
            self.first_name = first_name
            self.last_name = last_name
        try:
            validate_email(login_id)
            login_type = self.EMAIL
        except ValidationError:
            login_type = self.PENN_PATH
        self.login_type = login_type
        self.save()
