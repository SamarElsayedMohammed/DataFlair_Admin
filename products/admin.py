from django.contrib import admin
from .models import Grade,Product,Person,Course,Grade
from django.contrib.auth.models import Group
from django.db.models import Avg
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
from django import forms

# Admin Action Functions
def change_rating(modeladmin, request, queryset):
    queryset.update(rating = 'e')
# Action description
change_rating.short_description = "Mark Selected Products as Excellent"

class ProductA(admin.ModelAdmin):
    # exclude = ('description', )
    list_display = ('name', 'description')
    list_filter = ('mfg_date', )
    actions = [change_rating]



class PersonAdminForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"

    def clean_first_name(self):
        if self.cleaned_data["first_name"] == "Spike":
            raise forms.ValidationError("No Vampires")

        return self.cleaned_data["first_name"]


class PersonAdmin(admin.ModelAdmin):
    fields = ("first_name", "last_name", "courses")
    list_display = ('first_name', 'last_name','show_average')
    search_fields = ("first_name__startswith", )
    form = PersonAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["first_name"].label = "First Name (Humans only!):"
        return form

    def show_average(self, obj):
        result = Grade.objects.filter(person=obj).aggregate(Avg("grade"))
        return format_html("<b><i>{}</i></b>", result["grade__avg"])
        # return result["grade__avg"]

    show_average.short_description = "Average"


class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "year",)
    list_filter = ("year","name" )

    # def view_students_link(self, obj):
    #     count = obj.person_set.count()
    #     url = (
    #         reverse("admin:core_person_changelist")
    #         + "?"
    #         + urlencode({"courses__id": f"{obj.id}"})
    #     )
    #     return format_html('<a href="{}">{} Students</a>', url, count)

    # view_students_link.short_description = "Students"


class GradeAdmin(admin.ModelAdmin):
    pass
    # list_display = ('person', 'grade','course.name')

admin.site.register(Product,ProductA)
admin.site.register(Course,CourseAdmin)
admin.site.register(Person,PersonAdmin)
admin.site.register(Grade,GradeAdmin)
admin.site.unregister(Group)
# admin.site.unregister(Recent_actions)
admin.site.site_header = "DashBoard"
admin.site.site_header = 'Ecomm admin'
admin.site.site_title = 'Ecomm admin'
