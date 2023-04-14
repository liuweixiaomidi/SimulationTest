import time

import Lib.function as core


def fun1():
    core.move_robot("Fork-07", "CP55")
    core.move_robot("Fork-04", "PP402")
    time.sleep(3)
    core.goto_order("CP5", "Fork-04")


if __name__ == '__main__':
    fun1()
