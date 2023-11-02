from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

import catalog.models


class MainImageInline(AdminImageMixin, admin.TabularInline):
    model = catalog.models.MainImage
    fields = ("image",)


class ImagesInline(AdminImageMixin, admin.TabularInline):
    model = catalog.models.Image
    fields = ("image",)


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [
        MainImageInline,
        ImagesInline,
    ]
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.image_tmb,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)


@admin.register(catalog.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = [catalog.models.Category.normilized_name.field.name]
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)


@admin.register(catalog.models.Tag)
class TagAdmin(admin.ModelAdmin):
    readonly_fields = [catalog.models.Tag.normilized_name.field.name]
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
