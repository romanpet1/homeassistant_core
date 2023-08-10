"""Config flow to configure the shopping list integration."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigFlow
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN


def _get_data_schema(
    hass: HomeAssistant, config_entry: config_entries.ConfigEntry | None = None
) -> vol.Schema:
    """Get a schema with default values."""
    if config_entry is None:
        return vol.Schema(
            {
                vol.Required(CONF_NAME, default="Shopping List"): str,
            }
        )
    return vol.Schema(
        {
            vol.Required(CONF_NAME, default=config_entry.data.get(CONF_NAME)): str,
        }
    )


@callback
def configured_instances(hass: HomeAssistant) -> set[str]:
    """Return a set of configured SimpliSafe instances."""
    entries: list[str] = []
    for entry in hass.config_entries.async_entries(DOMAIN):
        entries.append(str(entry.data.get(CONF_NAME)))
    return set(entries)


def _get_data_schema(
    hass: HomeAssistant, config_entry: config_entries.ConfigEntry | None = None
) -> vol.Schema:
    """Get a schema with default values."""
    if config_entry is None:
        return vol.Schema(
            {
                vol.Required(CONF_NAME, default="Default"): str,
            }
        )
    return vol.Schema(
        {
            vol.Required(CONF_NAME, default=config_entry.data.get(CONF_NAME)): str,
        }
    )


@callback
def configured_instances(hass: HomeAssistant) -> set[str]:
    """Return a set of configured SimpliSafe instances."""
    entries: list[str] = []
    for entry in hass.config_entries.async_entries(DOMAIN):
        entries.append(str(entry.data.get(CONF_NAME)))
    return set(entries)


class ShoppingListFlowHandler(ConfigFlow, domain=DOMAIN):
    """Config flow for the shopping list integration."""

    VERSION = 1

    def __init__(self) -> None:
        """Init ShoppingListFlowHandler."""
        self._errors: dict[str, Any] = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        # Check if already configured
        self._errors = {}

        if user_input is not None:
            if user_input.get(CONF_NAME) not in configured_instances(self.hass):
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )
            self._errors[CONF_NAME] = "already_exist"

        return self.async_show_form(
            step_id="user",
            data_schema=_get_data_schema(self.hass),
            errors=self._errors,
        )

    async def async_step_onboarding(
        self, data: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by onboarding."""
        return await self.async_step_user(user_input={CONF_NAME: "Default"})

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for Met."""
        return ShopingListOptionsFlowHandler(config_entry)


class ShopingListOptionsFlowHandler(config_entries.OptionsFlow):
    """Options flow for Shoping List component."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize the Shopping List OptionsFlow."""
        self._config_entry = config_entry
        self._errors: dict[str, Any] = {}

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Configure options for Shopping List."""

        if user_input is not None:
            # Update config entry with data from user input
            self.hass.config_entries.async_update_entry(
                self._config_entry, title=user_input[CONF_NAME], data=user_input
            )
            return self.async_create_entry(
                title=self._config_entry.title, data=user_input
            )

        return self.async_show_form(
            step_id="init",
            data_schema=_get_data_schema(self.hass, config_entry=self._config_entry),
            errors=self._errors,
        )

    async_step_import = async_step_user
