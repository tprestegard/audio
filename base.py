import numpy as np
import re

from constants import (
    NOTE_NAMES, DEFAULT_A4, DEFAULT_SAMPLING_RATE, MAX_16BIT
)


class Note(object):
    note_regex = re.compile(r'^({notes})(\d+)$'.format(
        notes="|".join(NOTE_NAMES)))
    max_amplitude = 10

    def __init__(self, length, frequency=None, note=None,
        sampling_rate=DEFAULT_SAMPLING_RATE, amplitude=5, A4=DEFAULT_A4):

        # Check args - need exclusively frequency or note
        if (frequency and note) or not (frequency or note):
            raise ValueError('Provide only one of either frequency or note')
        if frequency and not isinstance(frequency, (int, float)):
            raise TypeError('Frequency must be an int, or float')
        if (amplitude > self.max_amplitude or amplitude < 0):
            raise ValueError('Amplitude must be in [0, {ma}]'.format(
                ma=self.max_amplitude))

        # Store some information
        self.A4_frequency = A4 # tuning - A4 frequency in Hz
        self.length = length # length in seconds
        self.amplitude = amplitude # unitless amplitude
        self.sampling_rate = sampling_rate
        
        # If note is provided, check it and parse it into a frequency
        if note:
            self.note = note
            self.frequency = self.convert_note_to_frequency(note)
        else:
            self.note = None
            self.frequency = frequency

        # Create output audio data
        self.audio_data = self.process_input()

    def convert_note_to_frequency(self, input_note):
        # Parse input note into note and octave
        m = self.note_regex.search(input_note)
        if m is None:
            raise ValueError(('{note} does not match the expected format. '
                'Example: G#10').format(note=input_note))
        note, octave = m.groups()
        octave = int(octave)

        # Number of half-steps from A4 to our note
        A_index = NOTE_NAMES.index('A')
        note_index = NOTE_NAMES.index(note)
        half_steps = (octave-4)*12 + (note_index - A_index)

        return self.A4_frequency*np.power(2, half_steps/12)

    def process_input(self):
        t_array = np.arange(0, self.length, 1/self.sampling_rate)
        data = self.amplitude * np.sin(2 * np.pi * self.frequency * t_array)

        # Convert to 16-bit range and normalize based on max_amplitude
        data *= MAX_16BIT / self.max_amplitude

        return data.astype(np.int16)
