from django import forms


class RowForm(forms.Form):
    value = forms.CharField(label='Значение')


class EmptyForm(forms.Form):
    pass
