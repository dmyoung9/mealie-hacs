# Mealie Integration for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]][license]

[![pre-commit][pre-commit-shield]][pre-commit]
[![Black][black-shield]][black]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

## Description
---

This is a Home Assistant integration for the wonderful [Mealie](https://github.com/hay-kot/mealie), a feature-rich and self-hosted recipe management service. Currently, it can only authenticate with one Mealie instance at a time, but it brings in data about the current day's meal plan recipes, including their ingredients, steps, pictures, and more! This data is provided primarily as sensor attributes, and is provided as both formatted text (in Markdown, to be used in the `markdown` card) and unformatted objects (to be used for more advanced operations or templating).

**This component will set up the following platforms.**

| Platform        | Description                                                               |
|:---------------:|:--------------------------------------------------------------------------|
| `camera`        | Display the meals from today's mealplan.                                  |
| `sensor`        | Show info about today's meals.                                            |
| `update`        | Shows the current version of Mealie and any available updates.            |

{% if not installed %}
## Installation with HACS
---
- Make sure that [HACS](https://hacs.xyz/) is installed
- Add the URL for this repository as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories) in HACS
- Install via `HACS -> Integrations`

## Configuration
---
- Navigate to `Settings -> Devices & Services -> Integrations`
- Click on "Add Integration"
- Search for "Mealie"
- Enter your login credentials and Mealie host address/port (in the `http[s]://{address}:{port}` form)
- Enjoy!
{% endif %}

## Contributions are welcome!
---

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Credits
---

This project is a fork from https://github.com/mealie-recipes/mealie-hacs/, and builds upon the functionality found there.

The original project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

The original project used code mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template.

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[buymecoffee]: https://www.buymeacoffee.com/dmyoung9
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/dmyoung9/mealie-hacs.svg?style=for-the-badge
[commits]: https://github.com/dmyoung9/mealie-hacs/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/dmyoung9/mealie-hacs.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-dmyoung9-blue.svg?style=for-the-badge
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/dmyoung9/mealie-hacs.svg?style=for-the-badge
[releases]: https://github.com/dmyoung9/mealie-hacs/releases
[user_profile]: https://github.com/dmyoung9
