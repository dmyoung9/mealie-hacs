from dataclasses import dataclass

from pydantic import BaseModel
from typing import Any, Optional
from homeassistant.backports.enum import StrEnum


"""Mealie API objects"""


class Recipe(BaseModel):
    """Recipe model."""

    name: str
    slug: str
    id: str

    recipeIngredient: list[Any]  #  TODO: we can type this
    tools: list[Any]  # TODO: we can type this
    tags: list[Any]  # TODO: we can type this
    recipeCategory: list[Any]  # TODO: We can type this

    recipeYield: Optional[str]
    totalTime: Optional[str]
    prepTime: Optional[str]
    cookTime: Optional[str]
    performTime: Optional[str]
    rating: Optional[str]
    description: Optional[str]
    orgURL: Optional[str]

    # TODO: This isn't included in the API request
    # recipeInstructions: Any
    # nutrition: Any
    # comments: Any
    # assets: list[Any]  # TODO: we can type this
    # notes: list[Any]  # TODO: we can type this
    # extras: list[Any]  # TODO: we can type this


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
    # versionLatest: str
    # TODO: add configuration URL here?


class MealieData:
    """Mealie API data."""

    def __init__(self):
        self.mealPlans = []

    mealPlans: list[MealPlan]
    about: Optional[About]
