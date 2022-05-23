import subprocess
import sys
import os


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


if __name__ == '__main__':
    install('tksheet')
    install('tkcalendar')
    os.system('python page_login_signup.py')
