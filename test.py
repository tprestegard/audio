import numpy as np
import re

import simpleaudio as sa

from base import Note


def create_chord(note_list, length, amplitude=5):
    notes = [Note(length, note=n, amplitude=amplitude).audio_data
        for n in note_list]
    return np.sum(np.array(notes), axis=0, dtype=np.int16)

# Make data arrays ------------------------------------------------------------
RH_LENGTH = 0.5

# Left-hand chords
lh_chords = [
    ['A2', 'C3', 'E3'],
    ['G2', 'B2', 'E3'],
    ['F2', 'A2', 'B2'],
    ['G2', 'B2', 'D3'],
]
chord_sequence = [create_chord(chord, length=RH_LENGTH*6, amplitude=2)
    for chord in lh_chords]
left_hand_full = np.concatenate(chord_sequence, axis=0)

# Right-hand notes
rh_notes = [
    'A3', 'C4', 'E4',
    'A3', 'C4', 'E4',
    'A3', 'C4', 'E4',
    'A3', 'C4', 'E4',
    'A3', 'C4', 'E4',
    'A3', 'C4', 'E4',
    'A3', 'C4', 'E4',
    'F4', 'E4', 'C4',
]
note_sequence = [Note(RH_LENGTH, note=n, amplitude=2).audio_data
    for n in rh_notes]
right_hand_full = np.concatenate(note_sequence, axis=0)

full_song = left_hand_full + right_hand_full

# Play sound ------------------------------------------------------------------
play_obj = sa.play_buffer(full_song, 1, 2, 44100)
play_obj.wait_done()
