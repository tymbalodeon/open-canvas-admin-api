from django.contrib.auth.models import User
from django.db.models import CASCADE, CharField, ManyToManyField, Model, OneToOneField


class CanvasUser(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    penn_id = CharField(max_length=10, unique=True)
    canvas_id = CharField(max_length=10, unique=True, null=True)


class CanvasSection(Model):
    canvas_id = CharField(max_length=10, blank=False, default=None, primary_key=True)
    name = CharField(max_length=50, blank=False, default=None)
    section_id = CharField(max_length=50, blank=True, default=None, null=True)
    workflow_state = CharField(max_length=15, blank=False, default=None)


class CanvasSite(Model):
    canvas_id = CharField(max_length=10, blank=False, default=None, primary_key=True)
    name = CharField(max_length=50, blank=False, default=None)
    course_id = CharField(max_length=50, blank=True, default=None, null=True)
    workflow_state = CharField(max_length=15, blank=False, default=None)
    sections = ManyToManyField(CanvasSection, related_name="sections", blank=True)
