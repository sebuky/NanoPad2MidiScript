from __future__ import with_statement
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.ButtonElement import ButtonElement
from _Framework.Layer import Layer
from _Framework.EncoderElement import EncoderElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.InputControlElement import MIDI_CC_TYPE
from .DeviceComponent import DeviceComponent

class NanoPad2(ControlSurface):
    def __init__(self, c_instance):
    	ControlSurface.__init__(self, c_instance)
    	self.sebukyChannel = 15
    	with self.component_guard():
    		encoders = ButtonMatrixElement(rows=[[ EncoderElement(MIDI_CC_TYPE, self.sebukyChannel, identifier + 1, Live.MidiMap.MapMode.absolute, name='Encoder_%d' % identifier) for identifier in xrange(2) ]])
    		self._left_button = ButtonElement(True, MIDI_CC_TYPE, self.sebukyChannel, 88)
    		self._right_button = ButtonElement(True, MIDI_CC_TYPE, self.sebukyChannel, 89)
    		self.lockBtn = ButtonElement(True, MIDI_CC_TYPE, self.sebukyChannel, 90)
    		self.upBtn = ButtonElement(True, MIDI_CC_TYPE, self.sebukyChannel, 84)
    		self.downBtn = ButtonElement(True, MIDI_CC_TYPE, self.sebukyChannel, 85)
    		self.onOffBtn = ButtonElement(True, MIDI_CC_TYPE, self.sebukyChannel, 86)
    		device = DeviceComponent(name='Device', is_enabled=False, layer=Layer(parameter_controls=encoders,prev_device_button=self._left_button, next_device_button=self._right_button))
    		device.set_enabled(True)
    		device.set_lock_button(self.lockBtn)
    		device.set_bank_nav_buttons(self.downBtn,self.upBtn)
    		device.set_on_off_button(self.onOffBtn)
    		self.set_device_component(device)
    		self._device_selection_follows_track_selection = True