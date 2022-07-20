from typing import Optional, List
from pydantic import BaseModel
from homeassistant.backports.enum import StrEnum


"""Mealie API objects"""


class EntryTypes(StrEnum):
    """Enum to represent the entry types."""

    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SIDE = "side"


class Recipe(BaseModel):
    """Recipe model."""

    name: str
    slug: str


class MealPlan(BaseModel):
    """Meal plan model."""

    date: str
    entryType: str
    title: Optional[str]
    text: Optional[str]
    recipeId: Optional[str]
    recipe: Optional[Recipe]


class About(BaseModel):
    """About model."""

    version: str
    versionLatest: str
    # TODO: add configuration URL here?


class MealieData:
    """Mealie API data."""

    def __init__(self):
        self.mealPlans = []

    mealPlans: list[MealPlan]
    about: About
