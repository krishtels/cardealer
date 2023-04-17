from rest_framework.mixins import DestroyModelMixin


class SafeDestroyModelMixin(DestroyModelMixin):
    def perform_destroy(self, instance, pk=None):
        instance.is_active = False
        instance.save()
