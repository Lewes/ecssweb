from django.contrib import admin

from .models import Jumpstart, Group, Fresher, Helper


class JumpstartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'start_time', 'end_time', 'helper_profile_lock_time')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'helper')
    search_fields = ('number', 'name')


    def has_module_permission(self,request):
        return True


    def helper(self, obj):
        return obj.helper.username


class HelperAdmin(admin.ModelAdmin):
    list_display = ('name', 'prefered_name', 'username', 'group', 'has_photo')
    search_fields = ('name', 'prefered_name', 'username')


    def has_module_permission(self,request):
        return True


    def has_photo(self, obj):
        return bool(obj.photo)
    has_photo.boolean = True

class FresherAdmin(admin.ModelAdmin):
    list_display = ('name', 'prefered_name', 'username', 'group', 'is_checked_in')
    search_fields = ('name', 'prefered_name', 'username')


    def has_module_permission(self,request):
        return True


admin.site.register(Jumpstart, JumpstartAdmin)

admin.site.register(Helper, HelperAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Fresher, FresherAdmin)
