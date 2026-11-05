import sys
import heapq

def solve():
    input_data = sys.stdin.buffer.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    Q = int(next(iterator))
    
    MAX_ID = 2000005
    version = [0] * MAX_ID
    prio = [0] * MAX_ID
    is_active = [False] * MAX_ID
    
    heap = []
    out = []
    
    for _ in range(Q):
        cmd = next(iterator).decode('ascii')
        if cmd == 'ADD':
            jid = int(next(iterator))
            p = int(next(iterator))
            version[jid] += 1
            prio[jid] = p
            is_active[jid] = True
            heapq.heappush(heap, (-p, jid, version[jid]))
        elif cmd == 'BOOST':
            jid = int(next(iterator))
            x = int(next(iterator))
            if is_active[jid]:
                prio[jid] += x
                version[jid] += 1
                is_active[jid] = True
                heapq.heappush(heap, (-prio[jid], jid, version[jid]))
                out.append(b"OK")
            else:
                out.append(b"NO")
        elif cmd == 'CANCEL':
            jid = int(next(iterator))
            if is_active[jid]:
                is_active[jid] = False
                out.append(b"OK")
            else:
                out.append(b"NO")
        elif cmd == 'PRINT':
            k = int(next(iterator))
            printed = []
            while heap and len(printed) < k:
                neg_p, jid, ver = heapq.heappop(heap)
                if is_active[jid] and version[jid] == ver and prio[jid] == -neg_p:
                    is_active[jid] = False
                    printed.append(str(jid).encode('ascii'))
            if not printed:
                out.append(b"VACIA")
            else:
                out.append(b" ".join(printed))
                
    sys.stdout.write("\n".join(res.decode('ascii') if isinstance(res, bytes) else res for res in out) + "\n")

if __name__ == '__main__':
    solve()
