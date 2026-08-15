from django import forms

class FileUploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file.name.endswith(('.csv', '.xlsx')):
            raise forms.ValidationError("Only CSV and XLSX files are allowed")
        return file
