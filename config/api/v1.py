from rest_framework.routers import DefaultRouter

from apps.cores.viewsets import (
    AcademyLevelViewSet,
    AcademicGroupViewSet,
    TypeInvestigationViewSet,
)
from apps.prototypes.viewsets import (
    PrototypeDownloadReporterViewsets,
    PrototypeViewSet,
    UploadPrototypeViewSets,
)
from apps.school.viewsets import StudentViewSet, TeacherViewSet, UploadStudentViewSets
from apps.users.viewsets import UserViewSet
from apps.prototypes.viewsets import (
    PrototypeTemplateExcelDownload,
    StudentTemplateExcelDownload,
    TeacherTemplateExcelDownload,
)

# Configuración de routers para las apps
router = DefaultRouter()


router.register("cores/groups", AcademicGroupViewSet, basename="group")
router.register(
    "cores/type-investigation", TypeInvestigationViewSet, basename="type-investigation"
)
router.register("cores/academy-level", AcademyLevelViewSet, basename="academy-level")

router.register("school/students", StudentViewSet, basename="student")
router.register("school/teachers", TeacherViewSet, basename="teacher")
router.register("school/users", UserViewSet, basename="user")
router.register(
    "school/upload-students", UploadStudentViewSets, basename="upload-students"
)

router.register("prototype-control/prototypes", PrototypeViewSet, basename="prototype")
router.register(
    "prototype-control/prototypes-reports",
    PrototypeDownloadReporterViewsets,
    basename="prototype-control/prototypes-reports",
)
router.register(
    "prototype-control/upload-prototypes",
    UploadPrototypeViewSets,
    basename="upload-prototypes",
)

router.register(
    "template/prototype-templates",
    PrototypeTemplateExcelDownload,
    basename="template/prototype-template-download",
)
router.register(
    "template/student-templates",
    StudentTemplateExcelDownload,
    basename="template/student-template-download",
)
router.register(
    "template/teacher-templates",
    TeacherTemplateExcelDownload,
    basename="teacher-template-download",
)

urlpatterns = router.urls
