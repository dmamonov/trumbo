"""User models admin."""

# Django
from django.contrib import admin

# Models
from api.cms.models import *

# Admin Site
class CMSAdminSite(admin.AdminSite):
    site_header = "CMS admin"
    site_title = "CMS Admin Portal"
    index_title = "Welcome to The CMS"


post_admin_site = CMSAdminSite(name='cms_admin')


# Model Admin
class ContentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'content',
        'content_type',
    )


admin.site.register(Content, ContentAdmin)
post_admin_site.register(Content, ContentAdmin)
