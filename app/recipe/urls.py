"""
URL mapping for Recipe
"""
from django.urls import include, path
from recipe import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("recipe", views.RecipeViewSets)

app_name = "recipe"

urlpatterns = [
    path("", include(router.urls)),
]
