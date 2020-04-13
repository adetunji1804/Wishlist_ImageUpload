from django import forms
from django.forms import FileInput, DateInput
from .models import Place


class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'visited')


# create a custom day input field, otherwise would get a plain text field.
class DateInput(forms.DateInput):
    input_type = 'date'  # overide the default input type, which is 'text'.


class TripReviewForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('notes', 'date_visited', 'photo')
        # uses HTML date element instead
        widgets = {'date_visited': DateInput()}

