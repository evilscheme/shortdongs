#!/usr/bin/env python
import math

balls = [u'8',
 u'B',
 u'3',
 u'\u03d6',
 u'\u2051',
 u'\u03b2',
 u'\u0299',
 u'\u2180',
 u'\u0bf0',
 u'\u2107',
 u'\u2375',
 u'\u03b5',
 u'\u03c9',
 u'\u1ff6',
 u'\u1f63',
 u'\u1f64',
 u'\u1f65',
 u'\u1f66',
 u'\u1f67',
 u'\u03d0',
 u'\u0417',
 u'\u10ea',
 u'\u10d5',
 u'\xdf',
 u'\ua4a7',
 u'\ua458',
 u'\U00010402',
 u'\U00010401',
 u'\U00010417',
 u'\U0001041a',
 u'\U00010301',
 u'\U0001031a']

shafts = [u'\u2261',
 u'\u2263',
 u'\U0001015e',
 u'\u30cb',
 u'\u1196',
 u'\u3193',
 u'\U00010112',
 u'\U00010115',
 u'\U00010117',
 u'\U00010118',
 u'\U0001011c',
 u'\U0001d36b',
 u'\U0001d36c',
 u'\u268c',
 u'\u268d',
 u'\u268e']

heads = [u'D',
 u'B',
 u'>',
 u'\u276f',
 u'\u276d',
 u'\u2771',
 u'\u204d',
 u'\u2e27',
 u'\u226b',
 u'\u2283',
 u'\u22d1',
 u'\u2ad0',
 u'\u2988',
 u'\u2183',
 u'\u2108',
 u'\u03f7',
 u'\u03f8',
 u'\u03f6',
 u'\u042d',
 u'\u044d',
 u'\U00010447',
 u'\U0001042a',
 u'\U00010303',
 u'\u029a']

jizz = [u'~', u'\u301c', u'\u3030', u'\u2053', u'\u223f', u'\U0001017c,']

def calc_bits(i):
    return int(math.log(i, 2))

balls_nbits = calc_bits(len(balls))
shafts_nbits = calc_bits(len(shafts))
heads_nbits = calc_bits(len(heads))
jizz_nbits = calc_bits(len(jizz))
total_bits = balls_nbits + shafts_nbits + heads_nbits

def _unisplit(u):
    i = 0
    chars = []
    while i < len(u):
        c = u[i]
        if u'\ud800' <= c <= u'\udbff':  # surrogate pair
            chars.append(u[i:i+2])
            i+=2
        else:
            chars.append(c)
            i+=1
    
    return chars


def int_to_dong(i):
    nbits = calc_bits(i)

    extra_bits = nbits - total_bits

    if extra_bits > (2 + jizz_nbits * 4):
        raise ValueError("integer too large")

    dong = []
    dong.append(balls[i & (2 ** balls_nbits - 1)])
    i >>= balls_nbits

    dong.append(shafts[i & (2 ** shafts_nbits -1)])
    i >>= shafts_nbits

    dong.append(heads[i & (2 ** heads_nbits -1)])
    i >>= heads_nbits

    shaft_len = [2,3,4,5][i & 0x3]
    i >>= 2
    dong[1] = dong[1]*shaft_len

    while extra_bits > 0:
        dong.append(jizz[i & (2 ** jizz_nbits -1)])
        extra_bits -= jizz_nbits
        i >>= jizz_nbits

    return ''.join(dong)

def dong_to_int(d):
    chars = _unisplit(d)
    v = 0
    v += balls.index(chars.pop(0))

    s = chars.pop(0)
    v += shafts.index(s) << balls_nbits
    
    nshaft = 1
    h = chars.pop(0)
    while h == s:
        nshaft += 1
        h = chars.pop(0)
    
    v += heads.index(h) << (balls_nbits + shafts_nbits)

    v += [2,3,4,5].index(nshaft) << (balls_nbits + shafts_nbits + heads_nbits)

    shift = balls_nbits + shafts_nbits + heads_nbits + 2
    for c in chars:
        v += jizz.index(c) << shift
        shift += jizz_nbits

    return v

def main():
    import sys
    i = int(sys.argv[1])
    d = int_to_dong(i)
    print d
    x = dong_to_int(d)
    print x

if __name__ == '__main__':
    main()
