from django import forms

class ReportForm(forms.Form):
    name = forms.CharField(max_length=100)
    report_type = forms.CharField(max_length=200)
    email = forms.CharField(max_length=15)
    email = forms.EmailField()
    description = forms.CharField(max_length=500, widget=forms.Textarea())

