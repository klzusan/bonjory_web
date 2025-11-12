from django.apps import AppConfig


class DlPackageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dl_package'
    
    def ready(self):
        import dl_package.signals