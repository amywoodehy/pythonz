from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from simple_history.admin import SimpleHistoryAdmin

from admirarchy.toolbox import HierarchicalModelAdmin

from .models import Book, Video, Event, User, Article, Place, Community, Discussion, Reference, Version


##################################################################################
# Делаем возможным редактировение пользователей (модель изменена нами) в административной части.
# Пользователи отобразятся в разделе текущего приложения.
# Взято из http://stackoverflow.com/a/17496836/308265


class UserChangeForm(BaseUserChangeForm):

    class Meta(BaseUserChangeForm.Meta):
        model = User


class UserCreationForm(BaseUserCreationForm):

    class Meta(BaseUserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


class UserAdmin(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = BaseUserAdmin.fieldsets + ((None, {'fields': (
            'comments_enabled',
            'digest_enabled',
            'disqus_shortname',
            'disqus_category_id',
            'timezone',
            'url',
            'email_public'
    )}),)

admin.site.register(User, UserAdmin)

##################################################################################


class PlaceAdmin(admin.ModelAdmin):

    list_display = ('geo_title', 'title', 'status', 'time_created')
    search_fields = ['title', 'geo_title']
    list_filter = ['time_created', 'status', 'geo_type']
    ordering = ['geo_title']

admin.site.register(Place, PlaceAdmin)


class EntityBaseAdmin(SimpleHistoryAdmin):

    list_display = ('time_created', 'title', 'submitter',)
    raw_id_fields = ('submitter',)
    search_fields = ['title', 'description']
    list_filter = ['time_created', 'status']
    ordering = ['-time_created']


class ArticleAdmin(EntityBaseAdmin):

    pass

admin.site.register(Article, ArticleAdmin)


class BookAdmin(EntityBaseAdmin):

    list_display = ('time_created', 'title', 'submitter', 'isbn')
    search_fields = ['title', 'isbn']

admin.site.register(Book, BookAdmin)


class CommunityAdmin(EntityBaseAdmin):

    search_fields = ['title', 'description', 'text']

admin.site.register(Community, CommunityAdmin)


class DiscussionAdmin(EntityBaseAdmin):

    search_fields = ['title', 'description', 'text']

admin.site.register(Discussion, DiscussionAdmin)


class EventAdmin(EntityBaseAdmin):

    list_display = ('time_created', 'title', 'submitter', 'type', 'specialization')
    search_fields = ['title', 'description', 'text']
    list_filter = ['time_created', 'status', 'type', 'specialization']

admin.site.register(Event, EventAdmin)


class VideoAdmin(EntityBaseAdmin):

    pass

admin.site.register(Video, VideoAdmin)


class ReferenceAdmin(HierarchicalModelAdmin, EntityBaseAdmin):

    hierarchy = True
    list_display = ('title', 'submitter', 'type')
    list_filter = ['time_created', 'status', 'type', 'version_added', 'version_deprecated']

admin.site.register(Reference, ReferenceAdmin)


class VersionAdmin(EntityBaseAdmin):

    list_display = ('title', 'current')

admin.site.register(Version, VersionAdmin)
