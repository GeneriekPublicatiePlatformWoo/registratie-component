from django import forms

from django_filters.rest_framework import Filter


class URLFilter(Filter):
    field_class = forms.URLField
