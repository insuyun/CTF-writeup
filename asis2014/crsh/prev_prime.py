from gmpy import next_prime
from random import randint

def find_low(p):
    low = p // 2
    while(next_prime(low) == p):
        low //= 2
    return low

def prev_prime(p):
    lo = find_low(p)
    pp = next_prime(lo)
    hi = p

    while lo < hi:
        mid = (lo + hi) // 2
        print mid
        mid_p = next_prime(mid)
        if(mid_p == p):
            hi = mid
        else:
            pp = mid_p
            lo = mid + 1

    return pp

print prev_prime(71445390607919938548377475361074566973666877698962004381686815881759650363064790907205389724727052137547259275540047248324480810969042982358139755944485006293081693292128510719329497724780095449564775706193685016091515868306878669276650004788889866268563082218902602391430478108176895385536441463628368479691L)
