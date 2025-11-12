import os
from django.core.files.storage import FileSystemStorage

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        """既に同名ファイルがあれば削除して上書き保存"""
        if self.exists(name):
            os.remove(os.path.join(self.location, name))
        return name
