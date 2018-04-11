from django import forms
from django.core import validators

# custom validator, def before class
def check_for_z(value):
    if value[0].lower() != 'z':
        raise forms.ValidationError("needs to start with z")
class FormName(forms.Form):
    name = forms.CharField(validators=[check_for_z])#use the validator
    email = forms.EmailField()
    verify_email = forms.EmailField(label="enter email again")
    text = forms.CharField(widget=forms.Textarea)
    # This would specify a form with a comment that
    # uses a larger Textarea widget,
    # rather than the default TextInput widget.
    botcatcher = forms.CharField(required=False,widget=forms.HiddenInput,validators=[validators.MaxLengthValidator(0)])
# field in not required and is HiddenInput
# "robot" visitor will fill in this HiddenInput, but real user won't
#  MaxLengthValidator(max_length, message=None) is the build in validator
# if length of value>max_length, raise  validation error
# i.e. robot will fill sth in botcatcher, once botcatcher length > 0, nothing will be posted
# an error will also shown on the page

    # clean the entire form
    def clean(self):
        all_clean_data = super().clean()
# The call to super().clean() in the example code ensures that
# any validation logic in parent classes is maintained

# Cleaning and validating fields that depend on each other
# get email and verify_email contents, compare them
        email = all_clean_data['email']
        vmail = all_clean_data['verify_email']
        if email != vmail:
            raise forms.ValidationError("Make sure emails match")
