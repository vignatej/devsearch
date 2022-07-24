from django.forms import ModelForm,widgets
from django import forms
from .models import Project,Review

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title','featured_imge','description','demo_link','source_link']
        widgets={
            'tag':forms.CheckboxSelectMultiple(),
        }
    def __init__(self,*args,**kwargs):
        super(ProjectForm, self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
        
        # self.fields['title'].widget.attrs.update({'class':'input','placeholder':'add title'})
        # self.fields['description'].widget.attrs.update({'class':'input','placeholder':'add title'})
    



class ReviewForm(ModelForm):
    class Meta:
        model=Review
        fields=['value','body']
        labels={
            'value':'palce your vote',
            'body': "add your comment with a vote"
        }
    def __init__(self,*args,**kwargs):
        super(ReviewForm, self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
        