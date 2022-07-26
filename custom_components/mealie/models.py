from dataclasses import dataclass
from typing import Any, Optional

from pydantic import BaseModel

from homeassistant.backports.enum import StrEnum

"""Mealie API objects"""


class Recipe(BaseModel):
    """Recipe model."""

    name: str
    slug: str
    id: str

    image: Optional[str]

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
    recipeInstructions: Optional[Any]
    nutrition: Optional[Any] = None
    comments: Optional[list[Any]]
    assets: Optional[list[Any]]  # TODO: we can type this
    notes: Optional[list[Any]]  # TODO: we can type this
    extras: Optional[dict[str, Any]]  # TODO: we can type this


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

    mealPlans: list[MealPlan] = []
    about: Optional[About] = None
