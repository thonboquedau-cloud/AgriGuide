from django.contrib import admin

from .models import (
    CropAdvisory,
    PestDisease,
    FarmingTip,
    LivestockAdvisory,
    Feedback,
)


@admin.register(CropAdvisory)
class CropAdvisoryAdmin(admin.ModelAdmin):

    list_display = (
        'crop_name',
        'crop_category',
        'planting_season',
        'soil_type',
        'created_at',
    )

    search_fields = (
        'crop_name',
        'crop_category',
    )


@admin.register(PestDisease)
class PestDiseaseAdmin(admin.ModelAdmin):

    list_display = (
        'crop_name',
        'problem_name',
        'problem_type',
        'created_at',
    )

    search_fields = (
        'crop_name',
        'problem_name',
        'problem_type',
    )


@admin.register(FarmingTip)
class FarmingTipAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'category',
        'season',
        'created_at',
    )

    search_fields = (
        'title',
        'category',
        'season',
    )


@admin.register(LivestockAdvisory)
class LivestockAdvisoryAdmin(admin.ModelAdmin):

    list_display = (
        'animal_name',
        'animal_category',
        'created_at',
    )

    search_fields = (
        'animal_name',
        'animal_category',
    )


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'email',
        'subject',
        'created_at',
    )

    search_fields = (
        'name',
        'email',
        'subject',
        'message',
    )

    list_filter = (
        'created_at',
    )

    readonly_fields = (
        'created_at',
    )
