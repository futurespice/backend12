from django.contrib import admin

from apps.accounts.models import CustomUser, EmployeeSchedule, EmployeeWorkdays


class EmployeeWorkdaysInline(admin.TabularInline):
    model = EmployeeWorkdays
    extra = 1


class EmployeeScheduleAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [EmployeeWorkdaysInline]


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "phone_number",
        "branch",
        "position",
        "is_verified",
        "is_active",
        "is_staff",
        "bonus",
    )
    list_display_links = (
        "id",
        "first_name",
        "last_name",
        "phone_number",
        "branch",
        "position",
        "is_verified",
        "is_active",
        "is_staff",
        "bonus",
    )
    list_filter = ("branch", "position", "is_verified", "is_active", "is_staff")
    search_fields = (
        "first_name",
        "last_name",
        "phone_number",
        "branch",
        "position",
        "is_verified",
        "is_active",
        "is_staff",
        "bonus",
    )
    list_per_page = 25


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(EmployeeSchedule, EmployeeScheduleAdmin)
