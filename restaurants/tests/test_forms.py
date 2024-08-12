from django import forms
from django.test import TestCase
from restaurants.forms import ReviewForm
from restaurants.models import Review

class ReviewFormTest(TestCase):
    def test_form_valid_data(self):
        form_data = {
            'rating': 4,
            'comment': 'Great restaurant!',
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())
        review = form.save(commit=False)
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, 'Great restaurant!')

    def test_form_missing_rating(self):
        form_data = {
            'comment': 'Delicious food!',
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_form_missing_comment(self):
        form_data = {
            'rating': 3,
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('comment', form.errors)

    def test_form_rating_choices(self):
        form = ReviewForm()
        rating_field_widget = form.fields['rating'].widget
        self.assertEqual(rating_field_widget.choices, [(i, i) for i in range(1, 6)])
        self.assertIsInstance(rating_field_widget, forms.Select)


    def test_form_comment_widget(self):
        form = ReviewForm()
        comment_field = form.fields['comment']
        self.assertEqual(comment_field.widget.attrs['rows'], 4)
        self.assertIsInstance(comment_field.widget, forms.Textarea)
