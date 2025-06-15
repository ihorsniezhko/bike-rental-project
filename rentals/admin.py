from django.contrib import admin
# Import Rental model.
from .models import Rental

# Register Rental model.
# See all rental transactions that have occurred.
admin.site.register(Rental)
