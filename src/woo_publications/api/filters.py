from django import forms

from django_filters.rest_framework import filters


class URLFilter(filters.Filter):
    field_class = forms.URLField
