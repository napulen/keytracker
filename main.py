"""keytracker

Creates the parameters for a Hidden Markov Model that finds the key of a sequence of notes

Nestor Napoles (napulen@gmail.com)
"""

import key_transitions as kt
import key_profiles as kp
import collections
import pprint as pp
import music21
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

def create_transition_probabilities(transitions="key_transitions_exponential"):
    """Returns the transition probabilities

    The 'distance' between two keys is determined
    by a matrix of the form:
    D   d   F   f   Ab  ab  Cb  cb  Ebb     
    A   a   C   c   Eb  eb  Gb  gb  Bbb     
    E   e   G   g   Bb  bb  Db  db  Fb
    B   b   D   d   F   f   Ab  ab  Cb
    F#  f#  A   a   C   c   Eb  eb  Gb
    C#  c#  E   e   G   g   Bb  bb  Db
    G#  g#  B   b   D   d   F   f   Ab
    D#  d#  F#  f#  A   a   C   c   Eb
    A#  a#  C#  c#  E   e   G   g   Bb

    This matrix is difficult to characterize by
    a single vector, this function attempts to
    do that and transpose it to all keys
    """
    d = dict()
    key_transitions = getattr(kt, transitions)    
    for idx,key in enumerate(states):
        if idx < 12:    # major keys
            pat1 = key_transitions[:12]
            pat2 = key_transitions[12:]
            shift1 = idx
            shift2 = idx
        else:   # minor keys
            pat1 = key_transitions[12:]
            pat2 = key_transitions[:12]
            shift1 = (idx + 3) % 12
            shift2 = idx % 12
        probs1 = collections.deque(pat1)
        probs2 = collections.deque(pat2)
        probs1.rotate(shift1)
        probs2.rotate(shift2)
        key_transitions = np.array(list(probs1) + list(probs2), dtype='float64')         
        d[key] = {key:key_transitions[idx] for idx,key in enumerate(states)}
    return d

def create_emission_probabilities(profiles="krumhansl_kessler"):
    """Returns the emission probabilities"""
    d = dict()
    for idx,key in enumerate(states):
        if idx < 12:    # major keys
            profile = profiles + "_major"
        else:
            profile = profiles + "_minor"
        key_profiles = getattr(kp, profile)
        key_profiles = collections.deque(key_profiles)
        key_profiles.rotate(idx % 12)
        key_profiles = np.array(list(key_profiles), dtype='float64')
        d[key] = {pc:key_profiles[pc] for pc in range(12)}
    return d

def create_observation_list(midi_file):
	s = music21.converter.parse(midi_file)
	obs = list()
	for note in s.flat.notes:
		if type(note) is music21.chord.Chord:
			obs.extend(note.orderedPitchClasses)
		else:
			obs.append(note.pitch.pitchClass)
	return obs

def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    for st in states:
        V[0][st] = {"prob": np.log(start_p[st]) + np.log(emit_p[st][obs[0]]), "prev": None}
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
    #for line in dptable(V):
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

    print('The steps of states are ' + ' '.join(opt) + ' with highest probability of %s' % max_prob)
    return opt, max_prob

def dptable(V):
    # Print a table of steps from dictionary
    yield " ".join(("%12d" % i) for i in range(len(V)))
    for state in V[0]:
        yield "%.7s: " % state + " ".join("%.7s" % ("%f" % v[state]["prob"]) for v in V)


trans_p = create_transition_probabilities(transitions='neighbour_level')
emit_p = create_emission_probabilities(profiles='krumhansl_kessler')

obs = create_observation_list('midi/wtc1/C.mid')[:10]

#obs = [0, 2, 4, 5, 7, 9, 11, 0]

#print(obs)
#pp.pprint(trans_p)

#state_list, max_prob = viterbi(obs, states, start_p, trans_p, emit_p)

pp.pprint(trans_p)

'''
obs = state_list # the keys become the observations
states # remain the same
emit_p = trans_p # the transition probabilities become the observation probabilities
trans_p = create_transition_probabilities(transitions='neighbour_level') # no modulations
start_p #remains the same

pp.pprint(trans_p)

key, max_prob = viterbi(obs, states, start_p, trans_p, emit_p)

'''
