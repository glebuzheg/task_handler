from rest_framework.routers import DefaultRouter

from src.api.v1.tasks.views.views import TaskViewSet

router = DefaultRouter()
router.register("task", TaskViewSet, basename="task")
urlpatterns = router.urls
