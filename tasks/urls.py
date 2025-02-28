from rest_framework import routers
from tasks.views import TaskViewset

router = routers.DefaultRouter()

router.register(r'tasks', TaskViewset, basename="task")

urlpatterns = router.urls
