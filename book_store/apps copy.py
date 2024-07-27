from django.apps import AppConfig
import logging


# class MyStoreConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'my_store'
       


logger = logging.getLogger(__name__)

class MyStoreConfig(AppConfig):
    name = 'my_store'

    def ready(self):
        logger.info("AppConfig ready method called")
        import my_store.signals
