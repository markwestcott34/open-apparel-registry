import json

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from simple_history.admin import SimpleHistoryAdmin

from api import models


class OarUserAdmin(UserAdmin):
    exclude = ('last_name', 'date_joined', 'first_name')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'is_staff', 'is_active',
                           'should_receive_newsletter',
                           'has_agreed_to_terms_of_service')}),
    )


class FacilityHistoryAdmin(SimpleHistoryAdmin):
    history_list_display = ('name', 'address', 'location')

    readonly_fields = ('created_from',)


class FacilityListItemAdmin(admin.ModelAdmin):
    exclude = ('processing_results',)
    readonly_fields = ('facility_list', 'facility',
                       'pretty_processing_results')

    def pretty_processing_results(self, instance):
        # The processing_results field is populated exclusively from processing
        # code so we are not in danger of rendering potentially unsafe user
        # submitted content
        return mark_safe('<pre>{}</pre>'.format(
            json.dumps(instance.processing_results, indent=2)))

    pretty_processing_results.short_description = 'Processing results'


class FacilityMatchAdmin(admin.ModelAdmin):
    exclude = ('results',)
    readonly_fields = ('facility_list_item', 'facility',
                       'confidence', 'status', 'pretty_results')

    def pretty_results(self, instance):
        # The status field is populated exclusively from processing code so we
        # are not in danger of rendering potentially unsafe user submitted
        # content
        return mark_safe('<pre>{}</pre>'.format(
            json.dumps(instance.results, indent=2)))

    pretty_results.short_description = 'Results'


class ContributorAdmin(SimpleHistoryAdmin):
    history_list_display = ('is_verified', 'verification_notes')


admin.site.register(models.User, OarUserAdmin)
admin.site.register(models.Contributor, ContributorAdmin)
admin.site.register(models.FacilityList)
admin.site.register(models.FacilityListItem, FacilityListItemAdmin)
admin.site.register(models.Facility, FacilityHistoryAdmin)
admin.site.register(models.FacilityMatch, FacilityMatchAdmin)
