from django import forms

from .opdb import create_strutura

class ProjectoAdminForm(forms.ModelForm):
    def save(self, commit=True):
        project = super(ProjectoAdminForm, self).save(commit)  
        create_strutura(project)
        return project

