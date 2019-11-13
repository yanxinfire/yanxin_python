import random


def continueGame(yn):
    assert yn.lower() in ('y', 'n'), "\033[41;1mOnly can be y/n!\033[0m"


def game():
    cmds = {"+": lambda x, y: x + y, "-": lambda x, y: x - y, "*": lambda x, y: x * y, "/": lambda x, y: x // y}
    while 1:
        counts = 0
        op = random.choice(["*", "+", "-", "/"])
        a = [random.randint(1, 100) for i in range(2)]
        a.sort(reverse=True)
        while counts < 3:
            try:
                result = int(input("%s %s %s = " % (a[0], op, a[1])).strip())
            except ValueError:
                print("\033[31;1mPlease using number to answer the question!\033[0m")
                result = None
            except (EOFError, InterruptedError):
                print("\033[31;1m好好读书！多赚钱！\033[0m")
                exit()
            if result == cmds[op](*a):
                print("\033[32;1mbingo!\033[0m")
                break
            else:
                counts += 1
        else:
            print("The right answer is : ", cmds[op](*a))

        while 1:
            # try:
            #     yn = input("\033[34;1mContinue?(y/n):\033[0m").strip()[0]
            #     continueGame(yn)
            # except AssertionError as e:
            #     print(e)
            #     continue
            # if yn.lower() == "y":
            #     break
            # elif yn.lower() == "n":
            #     print("\033[31;1m好好读书！多赚钱！\033[0m")
            #     exit()
            try:
                yn = input("\033[34;1mContinue?(y/n):\033[0m").strip()[0]
            except IndexError:
                yn = "error"
            if yn.lower() == "y":
                break
            elif yn.lower() == "n":
                print("\033[31;1m好好读书！多赚钱！\033[0m")
                exit()
            else:
                print("\033[41;1mPlease enter y/n!\033[0m")
                continue


if __name__ == '__main__':
    game()
