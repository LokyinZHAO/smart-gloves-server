import multiprocessing
from multiprocessing import Process
import os


def func(item):
    print(item)
    return "{" + item + "}"


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=4)
    results = []
    length = 5000
    for i in range(0, 4):
        results.append(pool.apply_async(func, (str(i),)))
    pool.close()  # 关闭进程池，表示不能再往进程池中添加进程，需要在join之前调用
    pool.join()  # 等待进程池中的所有进程执行完毕
    print("Sub-process(es) done.")
    k = 0
    for res in results:
        k += int(res.get())
    print(k)