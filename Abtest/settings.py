from MIDI import * # import MIDI status codes

""" settings which MIDI-notes and CCs trigger which functionality """


# debug_mode: whether the log-function should output to logfile
debug_mode = False

"""
	"<setting>": Note (<MIDI note#> [, <MIDI channel>])
	"<setting>": CC (<MIDI CC#> [, <mapping mode> [, <MIDI channel>]])
	
	if <mapping mode> is ommitted, it is assumed MIDI.RELATIVE_TWO_COMPLIMENT
		other modes are: ABSOLUTE, RELATIVE_BINARY_OFFSET, RELATIVE_SIGNED_BIT, RELATIVE_SIGNED_BIT2 
		see the documentation of your device which type MIDI CC it sends
	
	if <MIDI channel> is ommitted, it is assumed MIDI.DEFAULT_CHANNEL
		the DEFAULT_CHANNEL channel is set to 0 (ie. channel 1 if you count from 1-16)
		MIDI channels are zero-indexed, ie. you count from 0 to 15
		you can change DEFAULT_CHANNEL in MIDI.py
	
	
	
	
	Some examples for setting up your own mappings:
	
	
	- Mapping "arm" to Note #64 on MIDI channel 4 (if you count channels 1-16):
		
		"arm": Note(64, 3),
	
	
	- Mapping "pan" to an encoder with CC #23 on MIDI channel 8 (if you count channels 1-16):
	  Note: encoders usually send RELATIVE values - in this example in RELATIVE_TWO_COMPLIMENT format

		"pan": CC(23, RELATIVE_TWO_COMPLIMENT, 7),
	
	
	- Mapping "volume" to a fader with CC #7 on MIDI channel 2 (if you count channels 1-16):
	  Note: faders usually send ABSOLUTE values

		"arm": CC(7, ABSOLUTE, 1),
	
	
	- Mapping sends
	  Sends are mapped the same way as other controls, only that you can provide multiple CC()-defintions
	  in a so called "tuple" (that is basically a list). The first CC maps to "Send 1", the second CC 
	  to "Send 2", etc.
	  
	  A tuple is defined like so:
	  
	  (<element>, <element>, <element>)
	  
	  A basic example, mapping knobs with CC #12-19 on MIDI channel 16 (if you count channels 1-16):
	  Note: knobs usually send ABSOLUTE values
	  
		"sends": (
			CC(12, ABSOLUTE, 15),
			CC(13, ABSOLUTE, 15),
			CC(14, ABSOLUTE, 15),
			CC(15, ABSOLUTE, 15),
			CC(16, ABSOLUTE, 15),
			CC(17, ABSOLUTE, 15),
			CC(18, ABSOLUTE, 15),
			CC(19, ABSOLUTE, 15),
		),
	
	
	
	
	
	
	- ADVANCED FEATURE: binding multiple MIDI messages to the same control
	  
	  This is mainly useful to support multiple MIDI bindings in STC by default.
	  Note that e.g. volume is mapped by default to MIDI CC #22 as RELATIVE_TWO_COMPLIMENT and at the 
	  same time to MIDI CC #7 as ABSOLUTE.
	  See documentation here: http://stc.wiffbi.com/midi-implementation-chart/
	  
	  Binding multiple MIDI messages to one control is done by using a tuple of CC/Note-commands. 
	  It is actually the same as defining controls for sends. Looking at the default defintion
	  for "volume"
	
		"volume": (CC(22), CC(7, ABSOLUTE)),
	
	  and adding some white-space/newlines
	
		"volume": (
			CC(22),
			CC(7, ABSOLUTE)
		),
	  
	  reveals, that is looks similar to the definition of sends described earlier.
	  
	  BONUS: even a single send-control can be mapped to multiple MIDI-commands. As sends are defined as 
	  a tuple of CC-commands, we can instead of a single CC-command use a tuple of CC-commands. This 
	  results in a tuple of tuples of CC-commands.
	  
	  The default definition of sends are such a construct:
	
		"sends": (
			(CC(24), CC(12, ABSOLUTE)),
			(CC(25), CC(13, ABSOLUTE)),
			(CC(26), CC(14, ABSOLUTE)),
			(CC(27), CC(15, ABSOLUTE)),
			(CC(28), CC(16, ABSOLUTE)),
			(CC(29), CC(17, ABSOLUTE)),
			(CC(30), CC(18, ABSOLUTE)),
			(CC(31), CC(19, ABSOLUTE)),
		),
	  
	  "Send 1" is mapped to CC #24 in RELATIVE_TWO_COMPLIMENT on the DEFAULT_CHANNEL as well as to 
	           CC #12 in ABSOLUTE on the DEFAULT_CHANNEL
	  "Send 2" is mapped to CC #25 in RELATIVE_TWO_COMPLIMENT on the DEFAULT_CHANNEL as well as to 
	           CC #14 in ABSOLUTE on the DEFAULT_CHANNEL
	  ...
"""

# these values are only used if you map tempo-control to an absolute controller
tempo_min = 60
tempo_max = 187

volume_default = 0.55 # this value is -12db (trial-and-error to set as there is no mapping function available)

scrub_increment = 4 # scrubs by ticks

auto_select_playing_clip = False

# this feature is currently only planned
#reset_device_bank = False # Reset device-bank to 0 when selecting another device

auto_arm = False # default behaviour for auto-arming a track on selection, either False or True
has_midi_loopback = False # auto-arm on selection (including when selecting via mouse) usually only works with the STC.app on Mac, which provides MIDI-loopback-functionality. If you use STC.app, set has_midi_loopback = True, else set has_midi_loopback = False. If set to False, auto-arm on selection works even without STC.app, but only if you use STC-MIDI Remote Script and MIDI to select a track (so if you select a track via mouse, it will not be automatically armed)

# either dict or False
device_bestof = False
#device_bestof = {
#	"Impulse": (4,3,2,1,8,7,6,5),
#	"Looper": (2,1,0),
#}

# either a list of Device-names or False
# automatically selects the device if available when switched to the track
auto_select_device = False
#auto_select_device = ["Looper", "Impulse", "Simpler"]


# clip_trigger_quantization_steps reflects the quantization setting in the transport bar. 
# 0: None 
# 1: 8 Bars 
# 2: 4 Bars 
# 3: 2 Bars 
# 4: 1 Bar 
# 5: 1/2 
# 6: 1/2T 
# 7: 1/4 
# 8: 1/4T 
# 9: 1/8 
# 10: 1/8T 
# 11: 1/16 
# 12: 1/16T 
# 13: 1/32

# define which quantization steps should be stepped through - use range(14) to step through all available
clip_trigger_quantization_steps = [0, 1, 2, 3, 4, 5, 7, 9, 11, 13]

# to use all quantization steps, remove the # at the beginning of the following line
#clip_trigger_quantization_steps = range(14)



# midi_recording_quantization_steps reflects the current selection of the Edit->Record Quantization menu. 
# 0: None 
# 1: 1/4 
# 2: 1/8 
# 3: 1/8T 
# 4: 1/8 + 1/8T 
# 5: 1/16 
# 6: 1/16T 
# 7: 1/16 + 1/16T 
# 8: 1/32

# define which quantization steps should be stepped through - use range(9) to step through all available
midi_recording_quantization_steps = [0, 1, 2, 5, 8]

# to use all quantization steps, remove the # at the beginning of the following line
#midi_recording_quantization_steps = range(9)



midi_mapping = {
	
	
	# device control
	
	"prev_device_bank": CC(105),
	"next_device_bank": CC(104),
	
	
	
}