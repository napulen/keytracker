"""keytracker

Creates the parameters for a Hidden Markov Model
that finds the key of a sequence of notes

Nestor Napoles (napulen@gmail.com)
"""

import key_transitions as kt
import key_profiles as kp
import mido
import numpy as np
import os

states = (
    'C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B',
    'c', 'c#', 'd', 'eb', 'e', 'f', 'f#', 'g', 'ab', 'a', 'bb', 'b',
)

enharmonics = list(states) + ['C#', 'D#', 'Gb', 'G#', 'A#',
                              'db', 'd#', 'gb', 'g#', 'a#']

start_p = {
    'C': 1.0/24.0, 'Db': 1.0/24.0, 'D': 1.0/24.0, 'Eb': 1.0/24.0,
    'E': 1.0/24.0, 'F': 1.0/24.0, 'F#': 1.0/24.0, 'G': 1.0/24.0,
    'Ab': 1.0/24.0, 'A': 1.0/24.0, 'Bb': 1.0/24.0, 'B': 1.0/24.0,
    'c': 1.0/24.0, 'c#': 1.0/24.0, 'd': 1.0/24.0, 'eb': 1.0/24.0,
    'e': 1.0/24.0, 'f': 1.0/24.0, 'f#': 1.0/24.0, 'g': 1.0/24.0,
    'ab': 1.0/24.0, 'a': 1.0/24.0, 'bb': 1.0/24.0, 'b': 1.0/24.0,
}


def create_transition_probabilities(key_transitions):
    """Returns the transition probabilities"""
    d = dict()
    for idx, key in enumerate(states):
        tonic = key_transitions[:12]
        relative = key_transitions[12:]
        tonic_rotation = -(idx % 12)
        relative_rotation = -(idx % 12)
        if idx >= 12:
            tonic, relative = relative, tonic
            tonic_rotation = (tonic_rotation - 3) % 12
        probs1 = tonic[tonic_rotation:] + tonic[:tonic_rotation]
        probs2 = relative[relative_rotation:] + relative[:relative_rotation]
        kt_ = probs1 + probs2
        d[key] = {key: kt_[idx] for idx, key in enumerate(states)}
    return d


def create_emission_probabilities(major, minor):
    """Returns the emission probabilities"""
    d = dict()
    for idx, key in enumerate(states):
        rotation = -(idx % 12)
        profile = major if idx < 12 else minor
        profile = profile[rotation:] + profile[:rotation]
        d[key] = {pc: profile[pc] for pc in range(12)}
    return d


def get_notes_from_midi(midi_file):
    """Returns a list of notes from the note_on events of a MIDI file"""
    mid = mido.MidiFile(midi_file)
    notes = [msg.note for msg in mid
             if msg.type == 'note_on'
             and msg.velocity > 0]
    return notes


def get_pc_from_midi_notes(notes):
    """Returns the list of pitch-classes from a list of midi notes"""
    return [note % 12 for note in notes]


def create_observation_list(midi_file):
    """Returns a list of pitch classes from the notes on a MIDI file"""
    notes = get_notes_from_midi(midi_file)
    return get_pc_from_midi_notes(notes)


def mylog(x):
    """Returns the logarithm of x (without the annoying warnings of np.log)"""
    return np.log(x) if x > 8.7565e-27 else -np.inf


def get_key_from_filename(filename):
    """Returns the key of a midi file if it is a postfix of the filename"""
    key = filename[:-4].split('_')[-1]
    return key if key in enharmonics else 'x'


def is_key_guess_correct(ground_truth, guess):
    """Returns whether a key guess is correct or not"""
    return True if ground_truth_key == guess_key else False


def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    for st in states:
        V[0][st] = {
            "prob": mylog(start_p[st])
            + mylog(emit_p[st][obs[0]]), "prev": None
            }
    # Run Viterbi when t > 0
    for t in range(1, len(obs)):
        V.append({})
        for st in states:
            max_tr_prob = max(V[t-1][prev_st]["prob"] + mylog(trans_p[prev_st][st]) for prev_st in states)
            for prev_st in states:
                if V[t-1][prev_st]["prob"] + mylog(trans_p[prev_st][st]) == max_tr_prob:
                    max_prob = max_tr_prob + mylog(emit_p[st][obs[t]])
                    V[t][st] = {"prob": max_prob, "prev": prev_st}
                    break
    # for line in dptable(V):
    #    print(line)
    opt = []
    # The highest probability
    max_prob = max(value["prob"] for value in V[-1].values())
    previous = None
    # Get most probable state and its backtrack
    for st, data in V[-1].items():
        if data["prob"] == max_prob:
            opt.append(st)
            previous = st
            break
    # Follow the backtrack till the first observation
    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t + 1][previous]["prev"])
        previous = V[t + 1][previous]["prev"]

    # print('The steps of states are '
    #     + ' '.join(opt)
    #      + ' with highest probability of %s' % max_prob)
    return opt, max_prob


if __name__ == '__main__':
    for root, dirs, files in os.walk('midi'):
        for filename in files:
            filepath = os.path.join(root, filename)
            ground_truth_key = get_key_from_filename(filename)
            # Preparing the args for the first HMM
            key_transitions = kt.key_transitions_exponential_10
            trans_p = create_transition_probabilities(key_transitions)
            major = kp.sapp_major
            minor = kp.sapp_minor
            emit_p = create_emission_probabilities(major, minor)
            obs = create_observation_list(filepath)
            state_list, max_p = viterbi(obs, states, start_p, trans_p, emit_p)

            # Preparing the args for the second HMM
            obs = state_list  # the keys become the observations
            emit_p = trans_p  # the transitions become emission
            key_transitions = kt.key_transitions_null
            trans_p = create_transition_probabilities(key_transitions)
            key, max_prob = viterbi(obs, states, start_p, trans_p, emit_p)
            guess_key = key[0]
            iscorrect = is_key_guess_correct(ground_truth_key, guess_key)

            print('{}:\t{}\t{}\t{}'.format(filepath,
                                           ground_truth_key,
                                           guess_key,
                                           "Good" if iscorrect else "Wrong"))
