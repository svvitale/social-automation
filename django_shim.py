""" Module to do the necessary django configuration giving standalone scripts access to the Django environment. We do
this in a separate module so we can avoid PEP8 errors.  The two code lines MUST be executed before any other Django
imports are performed."""
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_automation.settings")
django.setup()
