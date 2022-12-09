# import sys,pathlib
# p = pathlib.Path(__file__).parent.absolute().parent.absolute()
# sys.path.insert(0, str(p) + "/saved")
# print(str(p))


import concurrent.futures

a = 0

def thread(val):
    return [1,2]

with concurrent.futures.ThreadPoolExecutor() as executor:
    a = executor.submit(thread, 1)
    print(a.result())
    


