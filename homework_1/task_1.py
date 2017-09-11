def fibonacci(n):
    if not isinstance(n,int):
        return 'n must be int'
    if n < 0:
        return 'n must be >= 0'
    if n == 0:
        return 0
    a = 1
    b = 1
    for i in range(2,n):
        a, b = b, a+b
    return b
