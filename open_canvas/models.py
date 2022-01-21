from django.db.models import CharField, EmailField, IntegerField, ManyToManyField, Model


class CanvasUser(Model):
    first_name = CharField()
    last_name = CharField()
    email = EmailField(primary_key=True)
    penn_id = IntegerField(max_length=10, unique=True)
    penn_key = CharField(max_length=10, unique=True)
    canvas_id = IntegerField(max_length=10, unique=True, blank=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_sortable_name(self):
        return f"{self.last_name}, {self.first_name}"


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
