from django import forms
from .models import Review, Visit, Bookmark

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = []

class BookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = []