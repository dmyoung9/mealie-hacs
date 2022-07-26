"""Sensor platform for Mealie."""
from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_INCLUDE
from homeassistant.core import callback

from .const import (
    CONF_ENTRIES,
    CONST_INCLUDE_ASSETS,
    CONST_INCLUDE_CATEGORIES,
    CONST_INCLUDE_COMMENTS,
    CONST_INCLUDE_EXTRAS,
    CONST_INCLUDE_INGREDIENTS,
    CONST_INCLUDE_INSTRUCTIONS,
    CONST_INCLUDE_NOTES,
    CONST_INCLUDE_NUTRITION,
    CONST_INCLUDE_TAGS,
    CONST_INCLUDE_TOOLS,
    DOMAIN,
    LOGGER,
)
from .coordinator import MealieDataUpdateCoordinator
from .entity import MealPlanEntity


async def async_setup_entry(hass, entry: ConfigEntry, async_add_devices):
    """Setup sensor platform."""
    coordinator: MealieDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_devices(
        [
            MealPlanSensor(meal, coordinator, entry)
            for meal in entry.options[CONF_ENTRIES]
        ]
    )


class MealPlanSensor(MealPlanEntity, SensorEntity):
    """Mealie Sensor class."""

    def __init__(self, meal, coordinator, entry: ConfigEntry):

        self._attr_extra_state_attributes = {}

        self._options = entry.options

        super().__init__(meal, coordinator)
        SensorEntity.__init__(self)

    def get_attribute_from_recipe(self, prop) -> Any | None:
        """Extract an attribute from the recipe."""
        return getattr(self.recipe, prop) if self.recipe is not None else None

    def get_attribute_list_from_recipe(self, prop) -> list:
        """Extract an attribute from the recipe as a list."""
        data = self.get_attribute_from_recipe(prop)
        return data if data is not None else []

    @callback
    def _process_update(self) -> None:
        super()._process_update()

        self._attr_native_value = (
            self.recipe.name
            if self.recipe is not None
            else self.meal_plan.title
            if self.meal_plan is not None
            else None
        )

        self._attr_extra_state_attributes.update(
            {
                "mealie_url": f"{self.coordinator.config_entry.data.get(CONF_HOST)}/recipe/{self.recipe.slug}"
                if self.recipe is not None
                else None
            }
        )

        self._attr_extra_state_attributes.update(
            [
                (
                    "type",
                    "recipe"
                    if self.recipe is not None
                    else "note"
                    if self.meal_plan is not None
                    else None,
                ),
                (
                    "description",
                    self.get_attribute_from_recipe("description")
                    if self.recipe is not None
                    else self.meal_plan.text
                    if self.meal_plan is not None
                    else None,
                ),
                ("yield", self.get_attribute_from_recipe("recipeYield")),
                ("total_time", self.get_attribute_from_recipe("totalTime")),
                ("prep_time", self.get_attribute_from_recipe("prepTime")),
                ("cook_time", self.get_attribute_from_recipe("cookTime")),
                ("perform_time", self.get_attribute_from_recipe("performTime")),
                ("total_time", self.get_attribute_from_recipe("totalTime")),
                ("rating", self.get_attribute_from_recipe("rating")),
                ("original_url", self.get_attribute_from_recipe("orgURL")),
            ]
        )

        include_options = self._options.get(CONF_INCLUDE, [])

        if CONST_INCLUDE_INGREDIENTS in include_options:
            ingredients = _clean_obj(
                self.get_attribute_list_from_recipe("recipeIngredient")
            )
            self._attr_extra_state_attributes.update(
                [
                    ("ingredients", ingredients),
                    ("ingredients_md", _format_ingredients(ingredients)),
                ]
            )

        if CONST_INCLUDE_TOOLS in include_options:
            tools = _clean_obj(self.get_attribute_list_from_recipe("tools"))
            self._attr_extra_state_attributes.update(
                [
                    ("tools", tools),
                    ("tools_md", _format_tools(tools)),
                ]
            )

        if CONST_INCLUDE_TAGS in include_options:
            tags = _clean_obj(self.get_attribute_list_from_recipe("tags"))
            self._attr_extra_state_attributes.update(
                [
                    ("tags", tags),
                    ("tags_md", _format_tags(tags)),
                ]
            )

        if CONST_INCLUDE_CATEGORIES in include_options:
            categories = _clean_obj(
                self.get_attribute_list_from_recipe("recipeCategory")
            )
            self._attr_extra_state_attributes.update(
                [
                    ("categories", categories),
                    ("categories_md", _format_categories(categories)),
                ]
            )

        if CONST_INCLUDE_INSTRUCTIONS in include_options:
            instructions = _clean_obj(
                self.get_attribute_list_from_recipe("recipeInstructions")
            )
            self._attr_extra_state_attributes.update(
                [
                    ("instructions", instructions),
                    ("instructions_md", _format_instructions(instructions)),
                ]
            )

        if CONST_INCLUDE_NUTRITION in include_options:
            nutrition = _clean_obj(self.get_attribute_from_recipe("nutrition"))
            self._attr_extra_state_attributes.update(
                [
                    ("nutrition", nutrition),
                    ("nutrition_md", _format_nutrition(nutrition)),
                ]
            )

        if CONST_INCLUDE_COMMENTS in include_options:
            comments = _clean_obj(self.get_attribute_list_from_recipe("comments"))
            self._attr_extra_state_attributes.update(
                [
                    ("comments", comments),
                    ("comments_md", _format_comments(comments)),
                ]
            )

        if CONST_INCLUDE_ASSETS in include_options:
            assets = _clean_obj(self.get_attribute_list_from_recipe("assets"))
            self._attr_extra_state_attributes.update([("assets", assets)])

        if CONST_INCLUDE_NOTES in include_options:
            notes = _clean_obj(self.get_attribute_list_from_recipe("notes"))
            self._attr_extra_state_attributes.update([("notes", notes)])

        if CONST_INCLUDE_EXTRAS in include_options:
            extras = _clean_obj(self.get_attribute_from_recipe("extras"))
            self._attr_extra_state_attributes.update([("extras", extras)])


def _format_instructions(instructions):
    text = ""
    for idx, i in enumerate(instructions):
        if title := i.get("title"):
            text += f"\n## {title}\n"
        text += f"### Step {idx+1}\n\n{i.get('text')}\n"
    return None if text == "" else text


def _format_ingredients(ingredients):
    text = ""
    for i in ingredients:
        if title := i.get("title"):
            text += f"\n## {title}\n"
        if any(k in i for k in ["unit", "food"]):
            text += (
                f"- [ ]{' ' + str(i.get('quantity', '')) if i.get('quantity') else ''}"
            )
            for key in ["unit", "food"]:
                text += f" {i.get(key, {}).get('name', '')}" if i.get(key) else ""
            text += f"{', ' + i.get('note', '') if i.get('note', '') else ''}\n"
        else:
            text += f"- [ ] {i.get('note')}\n"
    return None if text == "" else text


def _format_tags(tags):
    text = ", ".join([t["name"] for t in tags])
    return None if text == "" else text


def _format_categories(categories):
    text = ", ".join([c["name"] for c in categories])
    return None if text == "" else text


def _format_nutrition(nutrition):
    text = ""
    if nutrition:
        text = "| Type | Amount |\n|:-----|-------:|\n"
        for n in {k.replace("Content", ""): v for k, v in nutrition.items()}:
            text += f"| {n.title()} | {nutrition[n]} |\n"
    return None if text == "" else text


def _format_tools(tools):
    text = ""
    for t in tools:
        text += f"- [ ] {t.get('name')}\n"
    return None if text == "" else text


def _format_comments(comments):
    text = ""
    for c in sorted(comments, key=lambda x: x["createdAt"]):
        text += f"* {c.get('text')} by {c.get('user', {}).get('username', 'Anonymous')} @ {c.get('createdAt')}\n"
    return None if text == "" else text


def _clean_obj(obj):
    """Returns a copy of the object with any empty values removed."""
    if isinstance(obj, dict):
        obj = {
            k: v
            for (k, v) in obj.items()
            if v not in [None, [], {}, ""] and "id" not in k.lower()
        }
    elif isinstance(obj, list):
        for idx, i in enumerate(obj):
            obj[idx] = _clean_obj(i)

    return obj
