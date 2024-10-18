from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from django.core.exceptions import SuspiciousFileOperation

class IgnoreStaticFilesStorage(ManifestStaticFilesStorage):
    def path(self, name):
        blocked_files = ["owl.video.play.html", "nouislider.css"]
        if any(file in name for file in blocked_files):
            raise SuspiciousFileOperation(f"Access to static file '{name}' is blocked.")
        return super().path(name)
