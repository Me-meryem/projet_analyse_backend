# Modèle pour les files csv 
from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='csv_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.file.name