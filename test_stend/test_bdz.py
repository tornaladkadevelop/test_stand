#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока	Производитель
БДЗ	Строй-энергомаш
БДЗ	ТЭТЗ-Инвест
БДЗ	нет производителя

"""

from sys import exit
from time import sleep
from my_msgbox import *
from gen_func_procedure import *
from gen_func_utils import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["st_test_bdz"]

proc = Procedure()
reset = ResetRelay()
resist = Resistor()
mb_ctrl = CtrlKL()
read_mb = ReadMB()
mysql_conn = MySQLConnect()
fault = Bug(True)


def st_test_bdz():
    # reset.reset_all()
    # Тест 1. Включение/выключение блока при нормальном уровне сопротивления изоляции:
    # Сообщение	Убедитесь в отсутствии блоков в панелях разъемов.
    # Вставьте испытуемый блок БДЗ в разъем Х16 на панели B.
    # Вставьте заведомо исправные блок БИ в разъем Х26 и блок БУЗ-2 в разъем Х17, расположенные на панели B.
    msg_1 = "Убедитесь в отсутствии блоков в панелях разъемов. Вставьте испытуемый блок БДЗ в разъем Х16 на панели B"
    msg_2 = "Вставьте заведомо исправные блок БИ в разъем Х26 и блок БУЗ-2 в разъем Х17, расположенные на панели B"
    if my_msg(msg_1):
        if my_msg(msg_2):
            pass
        else:
            return False
    else:
        return False
    mb_ctrl.ctrl_relay('KL21', True)
    mb_ctrl.ctrl_relay('KL2', True)
    mb_ctrl.ctrl_relay('KL66', True)
    sleep(6)
    mb_ctrl.ctrl_relay('KL84', True)
    sleep(2)
    mb_ctrl.ctrl_relay('KL84', False)
    sleep(1)
    mb_ctrl.ctrl_relay('KL80', True)
    sleep(0.1)
    mb_ctrl.ctrl_relay('KL24', True)
    sleep(5)
    in_a1, in_a2 = __inputs_a()
    if in_a1 == True and in_a2 == True:
        pass
    else:
        fault.debug_msg("положение выходов блока не соответствует", 1)
        mysql_conn.mysql_ins_result("неисправен", "1")
        return False
    fault.debug_msg("положение выходов блока соответствует", 4)
    # 1.2.	Выключение блока
    sleep(1)
    mb_ctrl.ctrl_relay('KL80', False)
    sleep(0.1)
    mb_ctrl.ctrl_relay('KL24', False)
    sleep(5)
    in_a1, in_a2 = __inputs_a()
    if in_a1 == False and in_a2 == False:
        pass
    else:
        fault.debug_msg("положение выходов блока не соответствует", 1)
        mysql_conn.mysql_ins_result("неисправен", "1")
        return False
    fault.debug_msg("положение выходов блока соответствует", 4)
    mysql_conn.mysql_ins_result("исправен", "1")
    # Тест 2. Блокировка включения при снижении уровня сопротивления изоляции:
    sleep(1)
    mb_ctrl.ctrl_relay('KL22', True)
    sleep(1)
    mb_ctrl.ctrl_relay('KL80', True)
    sleep(0.1)
    mb_ctrl.ctrl_relay('KL24', True)
    sleep(5)
    in_a1, in_a2 = __inputs_a()
    if in_a1 == False and in_a2 == False:
        pass
    else:
        fault.debug_msg("положение выходов блока не соответствует", 1)
        mysql_conn.mysql_ins_result("неисправен", "2")
        return False
    fault.debug_msg("положение выходов блока соответствует", 4)
    mysql_conn.mysql_ins_result("исправен", "2")
    return True


def __inputs_a():
    in_a1 = read_mb.read_discrete(1)
    in_a2 = read_mb.read_discrete(2)
    return in_a1, in_a2


if __name__ == '__main__':
    try:
        if st_test_bdz():
            mysql_conn.mysql_block_good()
            my_msg('Блок исправен')
        else:
            mysql_conn.mysql_block_bad()
            my_msg('Блок неисправен')
    except OSError:
        my_msg("ошибка системы")
    except SystemError:
        my_msg("внутренняя ошибка")
    finally:
        reset.reset_all()
        exit()
