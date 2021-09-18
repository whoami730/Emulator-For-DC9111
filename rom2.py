prime = 251

def eea(a,b): #  x*a - b*p = 1 = x1*(p%a) - x2*a = x1*(p-[p/a]*a) - x2*a = a * (-x2-x1*[p/a]) + x1*p
    if (a == 0):
        return (0,-1)
    elif (b == 0):
        return (1,0)
    (x1,y1) = eea(b%a,a)
    return (-y1-x1*(b//a)),-x1

def inv(a):
    x,_ = eea(a,prime)
    return (prime+x)%prime

# <assume r14 and r15>
# 
#
#
#
#