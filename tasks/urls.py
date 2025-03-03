from rest_framework import routers
from tasks.views import TaskViewset, TaskHistoryViewset, UserRegisterView, UserViewset

router = routers.DefaultRouter()

router.register(r"tasks", TaskViewset, basename="task")
router.register(r"history", TaskHistoryViewset)
router.register(r'users', UserViewset)

urlpatterns = router.urls
