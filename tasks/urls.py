from rest_framework import routers
from tasks.views import TaskViewset, TaskHistoryViewset

router = routers.DefaultRouter()

router.register(r"tasks", TaskViewset, basename="task")
router.register(r"history", TaskHistoryViewset)

urlpatterns = router.urls
