# compatibility for Live 9, need to be written at the first line of the script
from __future__ import with_statement
import Live  # you import Live, in order to be able to use its components
# importthe Controle surface module
from _Framework.ControlSurface import ControlSurface
from _Framework.ButtonElement import ButtonElement
from _Framework.Layer import Layer
from _Framework.EncoderElement import EncoderElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.InputControlElement import MIDI_CC_TYPE
from .DeviceComponent import DeviceComponent
import MIDI
import time


class Abtest(ControlSurface):

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        self.sebukyChannel = 15
        with self.component_guard():
            self._left_button = ButtonElement(True, MIDI_CC_TYPE, self.sebukyChannel, 21)
            self._right_button = ButtonElement(True, MIDI_CC_TYPE, self.sebukyChannel, 22)
            self.lockBtn = ButtonElement(True, MIDI_CC_TYPE, self.sebukyChannel, 23)            
            self.onOffBtn = ButtonElement(True, MIDI_CC_TYPE, self.sebukyChannel, 24)
            encoders = ButtonMatrixElement(rows=[[ EncoderElement(MIDI_CC_TYPE, 0, identifier + 70, Live.MidiMap.MapMode.absolute, name='Encoder_%d' % identifier) for identifier in xrange(4) ]])
            device = DeviceComponent(name='Device', is_enabled=False, layer=Layer(parameter_controls=encoders,prev_device_button=self._left_button, next_device_button=self._right_button))
            device.set_enabled(True)
            device.set_lock_button(self.lockBtn)
            device.set_on_off_button(self.onOffBtn)
            self.set_device_component(device)
            self._device_selection_follows_track_selection = True
            self._long_press = 500
            self.__c_instance = c_instance
            self.c_instance = c_instance
            self.log_message('sebas initiated')
            self.conter = 0
            Pad1 = ButtonElement(True, MIDI_CC_TYPE, 0, 64)
            Pad1.add_value_listener(
                self._session_record_value, identify_sender=False)

            #self.backBtn = ButtonElement(True, MIDI_CC_TYPE, 0, 105)
            #self.backBtn.add_value_listener(self.goBack, identify_sender=False)
            #self.forwardBtn = ButtonElement(True, MIDI_CC_TYPE, 0, 104)
            #self.forwardBtn.add_value_listener(
                #self.goFront, identify_sender=False)
            # mappings for registered MIDI notes/CCs
            self.midi_callbacks = {}
            
            # lookup object for fast lookup of cc to mode
            self.midi_cc_to_mode = {}
            # parse midi_mapping recursive for MIDI.CC
            #self.mapping_parse_recursive(settings.midi_mapping.values())

            #self._device_control = DeviceControl(c_instance, self)

            #self.components = (self._device_control,)
            
        
    
    def disconnect(self):
        self._device_control.disconnect()

    # called from Live to build the MIDI bindings
    def O______________________________________________build_midi_map(self, midi_map_handle):
        #log("SelectedTrackControl::build_midi_map")
        script_handle = self.c_instance.handle()
        
        for channel in range(16):
            callbacks = self.midi_callbacks.get(channel, {})
            
            for note in callbacks.get(MIDI.NOTEON_STATUS,{}).keys():
                Live.MidiMap.forward_midi_note(script_handle, midi_map_handle, channel, note)
            
            for cc in callbacks.get(MIDI.CC_STATUS,{}).keys():
                Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, channel, cc)
    
    
    # internal method to register callbacks from different controls
    def O_________________________________________________register_midi_callback(self, callback, key, mode, status, channel):
        if not channel in self.midi_callbacks:
            self.midi_callbacks[channel] = {}
        
        if not status in self.midi_callbacks[channel]:
            self.midi_callbacks[channel][status] = {
                key: [callback,]
            }
        else:
            if key in self.midi_callbacks[channel][status]:
                self.midi_callbacks[channel][status][key].append(callback)
            else:
                self.midi_callbacks[channel][status][key] = [callback, ]
    
    def suggest_map_mode(self, cc_no):
        #log("suggest_map_mode")
        if cc_no in self.midi_cc_to_mode:
            return self.midi_cc_to_mode[cc_no]
        return MIDI.ABSOLUTE # see MIDI.py for definitions of modes

    # called from Live when MIDI messages are received
    def O_______________________________________________________________receive_midi(self, midi_bytes):
        channel = (midi_bytes[0] & MIDI.CHAN_MASK)
        status = (midi_bytes[0] & MIDI.STATUS_MASK)
        key = midi_bytes[1]
        value = midi_bytes[2]
        
        #log("receive_midi on channel %d, status %d, key %d, value %d" % (channel, status, key, value))
        
        # execute callbacks that are registered for this event
        callbacks = self.midi_callbacks.get(channel,{}).get(status,{}).get(key,[])
        mode = MIDI.ABSOLUTE
        if status == MIDI.CC_STATUS:
            # get mode and calculate signed int for MIDI value
            mode = self.suggest_map_mode(key)
            value = MIDI.relative_to_signed_int[mode](value)
        
        for callback in callbacks:
            callback(value, mode, status)

    def mapping_parse_recursive(self, mapping):
        tuple_type = type((1,2));
        for command in mapping:
            if type(command) == tuple_type:
                self.mapping_parse_recursive(command)
            elif isinstance(command, MIDI.CC):
                #log("MIDI CC %d is %s" % (command.key, command.mode))
                self.midi_cc_to_mode[command.key] = command.mode
                
    def goBack(self, value):
        self.log_message('sebas back' + str(value))

        if(value > 0):
            self.conter -= 1
            if(self.conter < 0):
                self.conter = 99

            self.changeBank()

    def changeBank(self):

        if self.selectedTrack != None:
            device = self.selectedTrack.view.selected_device
            if not device:
                return

            device.store_chosen_bank(0, self.conter)

    def goFront(self, value):
        self.log_message('sebas front' + str(value))

        if(value > 0):
            self.conter += 1
            if(self.conter > 99):
                self.conter = 0

            self.changeBank()

    def _session_record_value(self, value):
        now = int(round(time.time() * 1000))
        if(self.selected_scene != None):
            if(value != 0):
                self._last_stop_button_press = now
            else:
                if now - self._last_stop_button_press > self._long_press:

                    slot = self.selected_scene.clip_slots[
                        self.selected_track_idx]
                    if slot and slot.has_clip:
                        slot.delete_clip()
                else:
                    slot = self.selected_scene.clip_slots[
                        self.selected_track_idx]
                    slot.fire()

    @property
    def selectedTrack(self):
        return self.song().view.selected_track

    @property
    def selected_scene(self):
        return self.song().view.selected_scene

    @property
    def selected_track_idx(self):
        return self.tuple_idx(self.song().tracks, self.song().view.selected_track)

    def tuple_idx(self, tuple, obj):
        for i in xrange(0, len(tuple)):
            if (tuple[i] == obj):
                return i
        return(False)
