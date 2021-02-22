"""
A platform that provides information about your posts, followers, who you follow.

For more details on this component, refer to the documentation at
https://github.com/hudsonbrendon/sensor.instagram
"""
import logging

import async_timeout
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.entity import Entity

CONF_ACCOUNT = "account"

ICON = "mdi:instagram"

BASE_URL = "https://www.instagram.com/{}/?__a=1"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_ACCOUNT): cv.string,
    }
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup sensor platform."""
    account = config["account"]
    session = async_create_clientsession(hass)
    try:
        url = BASE_URL.format(account)
        async with async_timeout.timeout(10, loop=hass.loop):
            response = await session.get(url)
            info = await response.json()
        name = info["graphql"]["user"]["full_name"]
    except Exception:

        name = None

    if name is not None:
        async_add_entities([InstagramSensor(account, name, session)], True)


class InstagramSensor(Entity):
    """Instagram Sensor class"""

    def __init__(self, account, name, session):
        self._state = account
        self.session = session
        self._name = name
        self._posts = 0
        self._followers = 0
        self._following = 0
        self.account = account

    async def async_update(self):
        """Update sensor."""
        _LOGGER.debug("%s - Running update", self._name)
        try:
            url = BASE_URL.format(self.account)
            async with async_timeout.timeout(10, loop=self.hass.loop):
                response = await self.session.get(url)
                info = await response.json()
            self._posts = info["graphql"]["user"]["edge_owner_to_timeline_media"][
                "count"
            ]
            self._followers = info["graphql"]["user"]["edge_followed_by"]["count"]
            self._following = info["graphql"]["user"]["edge_follow"]["count"]
        except Exception as error:
            _LOGGER.debug("%s - Could not update - %s", self._name, error)

    @property
    def name(self):
        """Name."""
        return self._name

    @property
    def state(self):
        """State."""
        return self._state

    @property
    def posts(self):
        """Count posts."""
        return self._posts

    @property
    def followers(self):
        """Count followers."""
        return self._followers

    @property
    def following(self):
        """Count following."""
        return self._following

    @property
    def icon(self):
        """Icon."""
        return ICON

    @property
    def device_state_attributes(self):
        """Attributes."""
        return {
            "name": self.name,
            "posts": self.posts,
            "followers": self.followers,
            "following": self.following,
        }
