"""keytracker

Creates the parameters for a Hidden Markov Model
that finds the key of a sequence of notes

Nestor Napoles (napulen@gmail.com)
"""

import key_transitions as kt
import key_profiles as kp
import pprint as pp
import mido
import numpy as np

states = (
    'C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B',
    'c', 'c#', 'd', 'eb', 'e', 'f', 'f#', 'g', 'ab', 'a', 'bb', 'b',
)

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
    return [note % 12 for note in notes]


def create_observation_list(midi_file):
    """Returns a list of pitch classes from the notes on a MIDI file"""
    notes = get_notes_from_midi(midi_file)
    return get_pc_from_midi_notes(notes)


def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    for st in states:
        V[0][st] = {
            "prob": np.log(start_p[st])
            + np.log(emit_p[st][obs[0]]), "prev": None
            }
    # Run Viterbi when t > 0
    for t in range(1, len(obs)):
        V.append({})
        for st in states:
            max_tr_prob = max(V[t-1][prev_st]["prob"] + np.log(trans_p[prev_st][st]) for prev_st in states)
            for prev_st in states:
                if V[t-1][prev_st]["prob"] + np.log(trans_p[prev_st][st]) == max_tr_prob:
                    max_prob = max_tr_prob + np.log(emit_p[st][obs[t]])
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

    print('The steps of states are '
          + ' '.join(opt)
          + ' with highest probability of %s' % max_prob)
    return opt, max_prob


if __name__ == '__main__':
    key_transitions = kt.key_transitions_exponential_10
    trans_p = create_transition_probabilities(key_transitions)
    major = kp.krumhansl_kessler_major
    minor = kp.krumhansl_kessler_minor
    emit_p = create_emission_probabilities(major, minor)
    obs = create_observation_list('midi/wtc1/02_c.mid')

    # obs = [0, 1, 4, 5, 7, 8, 10, 0]

    # print(obs)
    # pp.pprint(emit_p)

    state_list, max_prob = viterbi(obs, states, start_p, trans_p, emit_p)

    # pp.pprint(trans_p)

    obs = state_list  # the keys become the observations
    # states, remains the same
    emit_p = trans_p  # the transition probs become the observation probs
    # No modulations
    key_transitions = kt.key_transitions_null
    trans_p = create_transition_probabilities(key_transitions)
    # start_p, remains the same

    # pp.pprint(trans_p)

    key, max_prob = viterbi(obs, states, start_p, trans_p, emit_p)
