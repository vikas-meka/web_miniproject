from django import forms

class student_marks(forms.Form):
    roll_no = forms.CharField(max_length=10)
    course = forms.CharField(max_length=10)
    ct1 = forms.IntegerField(required=True)
    ct2 = forms.IntegerField(required=True)
    end = forms.IntegerField(required=True)
    internals = forms.IntegerField(required=True)
    total = forms.IntegerField(required=True)
    grade = forms.IntegerField(required=True)
    score = forms.CharField(max_length=1,required=True)