from django import forms

class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=300, widget=forms.TextInput(attrs={"placeholder": "ex. Home maintenance"}))

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 4:
            raise forms.ValidationError("Name of list must be longer than 3 characters!")
        return name