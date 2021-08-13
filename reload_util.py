import os

import constants
import logging as log

reload_file = 'reload.lock'

# 文件存在 不要reload
# 文件不存在 去reload

log.basicConfig(format=constants.log_format, level=constants.log_level)

def need_reload():
    need_re = not os.path.exists(reload_file)
    log.info("需要reload：" + str(need_re))
    return need_re

def to_reload():
    log.info("准备重新reload...")
    if os.path.exists(reload_file):
        os.remove(reload_file)

def has_reloaded():
    log.info("reload完成，创建reload状态")
    if os.path.exists(reload_file) is False:
        with open(reload_file, "w") as file:
            file.write("")
