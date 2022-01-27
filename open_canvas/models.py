from django.db.models import (
    CharField,
    EmailField,
    IntegerField,
    ManyToManyField,
    Model,
    ForeignKey,
    CASCADE,
)

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


class CanvasSite(Model):
    canvas_id = IntegerField(primary_key=True)
    name = CharField(max_length=255)
    course_code = CharField(max_length=50, blank=True)
    workflow_state = CharField(max_length=11, choices=WORKFLOW_STATES)

    def __str__(self):
        return f'{self.course_code} "{self.name}" ({self.canvas_id})'


class CanvasSection(Model):
    canvas_id = IntegerField(primary_key=True)
    name = CharField(max_length=255)
    course = ForeignKey(CanvasSite, on_delete=CASCADE, related_name="sections")
    workflow_state = CharField(max_length=11, choices=WORKFLOW_STATES)


class CanvasUser(Model):
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    email = EmailField(primary_key=True)
    penn_id = IntegerField(unique=True, blank=True, null=True)
    penn_key = CharField(max_length=10, unique=True, blank=True, null=True)
    canvas_id = IntegerField(unique=True, blank=True, null=True)
    courses = ManyToManyField(CanvasSite, related_name="users", blank=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_sortable_name(self):
        return f"{self.last_name}, {self.first_name}"
