from django import forms

from core.models import Item

from .models import Occurrence


class OccurrenceForm(forms.ModelForm):
    class Meta:
        model = Occurrence
        fields = ("item", "occurrence_type", "location", "occurred_at", "notes")
        widgets = {
            "occurred_at": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M", attrs={"type": "datetime-local"}
            ),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["occurred_at"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["item"].queryset = Item.objects.filter(is_public=True).exclude(
            status=Item.Status.RETURNED
        )
