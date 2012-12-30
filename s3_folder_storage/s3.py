from django.core.files.storage import get_storage_class
from django.conf import settings

from storages.backends.s3boto import S3BotoStorage


class CachedS3BotoStorage(S3BotoStorage): 
        """ 
        django-compressor uses this class to gzip the compressed files and send them to s3 
        these files are then saved locally, which ensures that they only create fresh copies 
        when they need to 
        """ 
        def __init__(self, *args, **kwargs): 
            super(CachedS3BotoStorage, self).__init__(*args, **kwargs) 
            self.local_storage = get_storage_class('compressor.storage.CompressorFileStorage')() 


        def save(self, filename, content): 
            filename = super(CachedS3BotoStorage, self).save(filename, content) 
            self.local_storage._save(filename, content) 
            return filename 


class StaticStorage(CachedS3BotoStorage):
    """
    Storage for static files.
    The folder is defined in settings.STATIC_S3_PATH
    """

    def __init__(self, *args, **kwargs):
        kwargs['location'] = settings.STATIC_S3_PATH
        super(StaticStorage, self).__init__(*args, **kwargs)


class DefaultStorage(CachedS3BotoStorage):
    """
    Storage for uploaded media files.
    The folder is defined in settings.DEFAULT_S3_PATH
    """

    def __init__(self, *args, **kwargs):
        kwargs['location'] = settings.DEFAULT_S3_PATH
        super(DefaultStorage, self).__init__(*args, **kwargs)
