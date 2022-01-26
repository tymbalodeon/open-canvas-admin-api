from canvas.api import get_canvas
from canvas.constants import ACCOUNT

from open_canvas.models import CanvasSite


def sync_courses(test=False, account=ACCOUNT):
    account = get_canvas(test).get_account(account)
    courses = account.get_courses()
    for course in courses:
        CanvasSite.objects.create(
            canvas_id=course.id,
            name=course.name,
            course_code=course.sis_course_id,
            workflow_state=course.workflow_state,
        )
