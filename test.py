__author__ = 'ttrebat'

if __name__ == "__main__":
    exec(compile(open("server.py").read(), "server.py", 'exec'))
    for i in range(8):
        exec(compile(open("poker.py").read(), "poker.py", 'exec'))