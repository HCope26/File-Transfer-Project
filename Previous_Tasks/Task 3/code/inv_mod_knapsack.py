def getInvMod(n,m):
    inv_n = 1
    test = 0
    while(True):
        test = (n*inv_n)%m
        if(test==1):
            break
        else:
            inv_n = inv_n + 1
    return inv_n

def pub_key(n,m,seq):
    public_key = []
    for value in seq:
        key_seq = (value*n)%m
        public_key.append(key_seq)

    return(public_key)
    
