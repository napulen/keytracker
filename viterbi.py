# -*- coding: utf-8 -*-
'''
HMM（隐马尔可夫模型）是用来描述隐含未知参数的统计模型
举一个经典的例子：
一个东京的朋友每天根据天气{下雨,天晴}决定当天的活动{公园散步,购物,清理房间}中的一种
我每天只能在twitter上看到她发的推“啊，我前天公园散步、昨天购物、今天清理房间了！”
那么我可以根据她发的twitter推断东京这三天的天气
在这个例子里，显状态是活动，隐状态是天气
求解最可能的隐状态序列是HMM的三个典型问题之一，通常用Viterbi算法解决
Viterbi算法就是求解HMM上的最短路径（-log(prob)，也即是最大概率）的算法
'''

# HMM描述 lambda = (states, observations, start_probability, transition_probability, emission_probability)

import time
import random

states = ('Rainy', 'Sunny')

obs_options = ['walk', 'shop', 'clean']

observations = [obs_options[random.randint(0, len(obs_options) - 1)]
                for x in range(100000)]

# observations = ('walk', 'walk', 'shop', 'clean', 'clean', 'shop', 'shop', 'clean', 'walk', 'shop')

start_probability = {'Rainy': 0.6, 'Sunny': 0.4}

transition_probability = {
    'Rainy' : {'Rainy': 0.7, 'Sunny': 0.3},
    'Sunny' : {'Rainy': 0.4, 'Sunny': 0.6},
    }

emission_probability = {
    'Rainy' : {'walk': 0.1, 'shop': 0.4, 'clean': 0.5},
    'Sunny' : {'walk': 0.6, 'shop': 0.3, 'clean': 0.1},
}


def viterbi2(states, obs, start_p, trans_p, emit_p):
    V = [{}]
    for st in states:
        V[0][st] = {"prob": start_p[st] * emit_p[st][obs[0]], "prev": None}
    # Run Viterbi when t > 0
    for t in range(1, len(obs)):
        V.append({})
        for st in states:
            max_tr_prob = max(V[t-1][prev_st]["prob"]*trans_p[prev_st][st] for prev_st in states)
            for prev_st in states:
                if V[t-1][prev_st]["prob"] * trans_p[prev_st][st] == max_tr_prob:
                    max_prob = max_tr_prob * emit_p[st][obs[t]]
                    V[t][st] = {"prob": max_prob, "prev": prev_st}
                    break
    # for line in dptable(V):
    #    print line
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

    # print 'The steps of states are ' + ' '.join(opt) + ' with highest probability of %s' % max_prob
    return opt

def viterbit(states, obs, s_pro, t_pro, e_pro):
    path = { s:[] for s in states} # init path: path[s] represents the path ends with s
    curr_pro = {}
    for s in states:
        curr_pro[s] = s_pro[s] * e_pro[s][obs[0]]
    for i in range(1, len(obs)):
        last_pro = curr_pro
        curr_pro = {}
        for curr_state in states:
            max_pro, last_sta = max(
                (
                    (last_pro[last_state] * t_pro[last_state][curr_state] * e_pro[curr_state][obs[i]], last_state)
                    for last_state in states)
                )
            curr_pro[curr_state] = max_pro
            path[curr_state].append(last_sta)

    # find the final largest probability
    max_pro = -1
    max_path = None
    for s in states:
        path[s].append(s)
        if curr_pro[s] > max_pro:
            max_path = path[s]
            max_pro = curr_pro[s]
        # print '%s: %s'%(curr_pro[s], path[s]) # different path and their probability
    return max_path


def viterbi(stas, obs, start_p, trans_p, emit_p):
    V = [{}]
    path = {}
    for y in stas:
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
        path[y] = [y]
    # print path

    for t in range(1, len(obs)):
        V.append({})
        new_path = {}
        for y in stas:
            (prob, sta) = max([(V[t - 1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in stas])
            V[t][y] = prob
            new_path[y] = path[sta] + [y]
        path = new_path
    (prob, sta) = max([(V[len(obs) - 1][y], y) for y in stas])
    return prob, path[sta]


def example(v):
    return v(
        states,
        observations,
        start_probability,
        transition_probability,
        emission_probability)


startTime = time.time()
x = example(viterbi2)
'''
y = example(viterbi2)
z = example(viterbi)
if x == y:
    print("All are the same")
else:
    print('Oh noes...')
    print(observations)
    print(x)
    print(y)
    print(z[1])
'''
print(time.time() - startTime)
