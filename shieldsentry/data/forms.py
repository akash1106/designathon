from django import forms


class UploadFileForm(forms.Form):
    """
    Simplest of forms to provide file upload
    """
    file_upload = forms.FileField()