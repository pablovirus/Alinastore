from django.db import models

class Csv(models.Model):
    file_name = models.FileField(max_length=255,upload_to='csvs')
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f'File id: {self.id}'

    class Meta:
        permissions = (('can_upload_csv', 'Upload CSV files to database'),)


