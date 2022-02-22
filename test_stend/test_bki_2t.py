#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки
Тип блока Производитель
БКИ-2Т	нет производителя	52
БКИ-2Т	ТЭТЗ-Инвест	53
БКИ-2Т	Строй-энерго	54

"""

from sys import exit
from time import sleep
from gen_func_utils import *
from my_msgbox import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["st_test_bki_2t"]

reset = ResetRelay()
resist = Resistor()
result = Result()
ctrl_kl = CtrlKL()
read_mb = ReadMB()
mysql_conn = MySQLConnect()
fault = Bug(None)


def st_test_bki_2t():
    # reset.reset_all()
    # Тест 1. Проверка исходного состояния блока:
    mysql_conn.mysql_ins_result("идет тест 1", "1")
    in_a1, in_a2, in_a5, in_a6 = __inputs_a()
    if in_a5 == True and in_a1 == False and in_a6 == True and in_a2 == False:
        pass
    else:
        mysql_conn.mysql_ins_result("неисправен", "1")
        fault.debug_msg('тест 1 не пройден', 1)
        if in_a5 == False or in_a1 == True:
            mysql_conn.mysql_error(35)
        elif in_a6 == False or in_a2 == True:
            mysql_conn.mysql_error(36)
        return False
    fault.debug_msg('тест 1 пройден', 3)
    mysql_conn.mysql_ins_result("исправен", '1')
    # Тест 2. Проверка работы блока при подаче питания и при
    # нормальном сопротивлении изоляции контролируемого присоединения
    mysql_conn.mysql_ins_result("идет тест 2", "2")
    ctrl_kl.ctrl_relay('KL21', True)
    sleep(5)
    if __subtest_21():
        pass
    else:
        mysql_conn.mysql_ins_result("неисправен", '2')
        fault.debug_msg('тест 2.1 не пройден', 1)
        return False
    fault.debug_msg('тест 2.1 пройден', 3)
    mysql_conn.mysql_ins_result("исправен", '2')
    # Тест 3. Проверка работы 1 канала (К1) блока при снижении
    # уровня сопротивлении изоляции ниже 30 кОм в цепи 1 канала
    mysql_conn.mysql_ins_result("идет тест 3", "3")
    ctrl_kl.ctrl_relay('KL31', True)
    resist.resist_kohm(12)
    in_a1, in_a2, in_a5, in_a6 = __inputs_a()
    if in_a5 == False and in_a1 == True and in_a6 == True and in_a2 == False:
        pass
    else:
        mysql_conn.mysql_ins_result("неисправен", '3')
        if in_a5 == True or in_a1 == False:
            mysql_conn.mysql_error(39)
        elif in_a6 == False or in_a2 == True:
            mysql_conn.mysql_error(40)
        return False
    resist.resist_kohm(590)
    mysql_conn.mysql_ins_result("исправен", '3')
    # Тест 4. Проверка работы 1 канала (К1) блока от кнопки «Проверка БКИ» в цепи 1 канала
    mysql_conn.mysql_ins_result("идет тест 4", "4")
    if __subtest_21():
        pass
    else:
        mysql_conn.mysql_ins_result("неисправен", '4')
        return False
    ctrl_kl.ctrl_relay('KL23', True)
    ctrl_kl.ctrl_relay('KL22', True)
    sleep(1)
    in_a1, in_a2, in_a5, in_a6 = __inputs_a()
    if in_a5 == False and in_a1 == True and in_a6 == True and in_a2 == False:
        pass
    else:
        mysql_conn.mysql_ins_result("неисправен", '4')
        if in_a5 == True or in_a1 == False:
            mysql_conn.mysql_error(41)
        elif in_a6 == False or in_a2 == True:
            mysql_conn.mysql_error(42)
        return False
    resist.resist_kohm(590)
    ctrl_kl.ctrl_relay('KL22', False)
    mysql_conn.mysql_ins_result("исправен", '4')
    # Тест 5. Проверка работы 2 канала (К2) блока при снижении уровня
    # сопротивлении изоляции ниже 30 кОм в цепи 2 канала
    mysql_conn.mysql_ins_result("идет тест 5", "5")
    ctrl_kl.ctrl_relay('KL31', False)
    sleep(1)
    resist.resist_kohm(12)
    sleep(1)
    in_a1, in_a2, in_a5, in_a6 = __inputs_a()
    if in_a5 == True and in_a1 == False and in_a6 == False and in_a2 == True:
        pass
    else:
        mysql_conn.mysql_ins_result("неисправен", '5')
        if in_a5 == False or in_a1 == True:
            mysql_conn.mysql_error(43)
        elif in_a6 == True or in_a2 == False:
            mysql_conn.mysql_error(44)
        return False
    resist.resist_kohm(590)
    mysql_conn.mysql_ins_result("исправен", '5')
    # Тест 6. Проверка работы 2 канала (К2) блока от кнопки «Проверка БКИ» в цепи 2 канала
    mysql_conn.mysql_ins_result("идет тест 6", "6")
    if __subtest_21():
        pass
    else:
        mysql_conn.mysql_ins_result("неисправен", '6')
    ctrl_kl.ctrl_relay('KL22', True)
    in_a1, in_a2, in_a5, in_a6 = __inputs_a()
    if in_a5 == True and in_a1 == False and in_a6 == False and in_a2 == True:
        pass
    else:
        mysql_conn.mysql_ins_result("неисправен", '6')
        if in_a5 == False or in_a1 == True:
            mysql_conn.mysql_error(45)
        elif in_a6 == True or in_a2 == False:
            mysql_conn.mysql_error(46)
        return False
    mysql_conn.mysql_ins_result("исправен", '6')
    return True


def __subtest_21():
    in_a1, in_a2, in_a5, in_a6 = __inputs_a()
    if in_a5 == True and in_a1 == False and in_a6 == True and in_a2 == False:
        pass
    else:
        if in_a5 == False or in_a1 == True:
            mysql_conn.mysql_error(37)
        elif in_a6 == False or in_a2 == True:
            mysql_conn.mysql_error(38)
        return False
    return True


def __inputs_a():
    in_a1 = read_mb.read_discrete(1)
    in_a2 = read_mb.read_discrete(2)
    in_a5 = read_mb.read_discrete(5)
    in_a6 = read_mb.read_discrete(6)
    return in_a1, in_a2, in_a5, in_a6


if __name__ == '__main__':
    try:
        if st_test_bki_2t():
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
