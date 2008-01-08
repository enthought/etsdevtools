import enthought.gotcha as gotcha

def foo(n):
    a=0
    for i in range(n*10):
        a += 1

def bar(n):
    a=0
    for i in range(n):
        a += 1

gotcha.begin_profiling()
gotcha.profile(foo, 10000)
gotcha.profile(bar, 10000)
gotcha.end_profiling()
stats = gotcha.stats()
