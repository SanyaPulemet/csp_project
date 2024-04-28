from django import forms

class FileUploadForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'required':True,'multiple':True}))
    link_on = forms.BooleanField(widget=forms.CheckboxInput(attrs={'required':False}),required=False)
    comments_on = forms.BooleanField(widget=forms.CheckboxInput(attrs={'required':False}),required=False)
    public_on = forms.BooleanField(widget=forms.CheckboxInput(attrs={'required':False}),required=False)
    title = forms.CharField(max_length=50)
    image = forms.ImageField()
    