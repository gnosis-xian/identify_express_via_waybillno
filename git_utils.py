import os
import logging as log
import constants
import lock_util

log.basicConfig(format=constants.log_format, level=constants.log_level)

def commit_and_push():
    try:
        if lock_util.locked():
            return
        lock_util.create_lock()
        config()
        pull()
        add()
        commit()
        push()
    except Exception as e:
        log.warning("git推送出错", e)
    finally:
        lock_util.remove_lock()

def config():
    os.system("git config --global user.email \"gaojing1996@vip.qq.com\"")
    os.system("git config --global user.name \"Gnosis\"")

def pull():
    os.system("git pull")


def add():
    os.system("git add .")


def commit():
    os.system("git commit -m \"update data sets.\"")


def push():
    os.system("git push")
