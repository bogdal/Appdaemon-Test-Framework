from apps.smart_bathroom import SmartBathroom
from appdaemon.plugins.hass.hassapi import Hass
from mock import patch, MagicMock
import pytest
from datetime import time
from apps.entity_ids import ID

"""
TODO: Add fixture to 'set_state' (will actually patch the 'get_state' method)
"""

@pytest.fixture
def smart_bathroom(hass_functions):
    smart_bathroom = SmartBathroom(
        None, None, None, None, None, None, None, None)
    # Set initial time to 3PM
    hass_functions['time'].return_value = time(hour=15)
    smart_bathroom.initialize()
    return smart_bathroom


@pytest.fixture
def smart_bathroom_trigger_new(smart_bathroom):
    class TriggerNew:
        def __init__(self, smart_bathroom):
            self.smart_bathroom = smart_bathroom

        def time(self, hour=None):
            self.smart_bathroom._time_triggered(hour=hour)

        def motion_bathroom(self):
            self.smart_bathroom._new_motion_bathroom(None, None, None)

        def motion_kitchen(self):
            self.smart_bathroom._new_motion_kitchen(None, None, None)

        def motion_living_room(self):
            self.smart_bathroom._new_motion_living_room(None, None, None)
        
        def debug(self):
            self.smart_bathroom.debug(None, {'click_type': 'single'}, None)
    return TriggerNew(smart_bathroom)


## Fake Tests #######################################################################################
def test_turn_on_bathroom_light_on_motion(smart_bathroom_trigger_new, assert_that):
    smart_bathroom_trigger_new.motion_bathroom()
    assert_that(ID['bathroom']['led_light']).was_turned_on(color_name='red')

def test_debug(smart_bathroom_trigger_new, assert_that):
    smart_bathroom_trigger_new.debug()
    assert_that('xiaomi_aqara/play_ringtone').was_called_with(ringtone_id=10001, ringtone_vol=20)
#####################################################################################################