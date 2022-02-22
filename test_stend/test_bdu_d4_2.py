#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки
Тип блока Производитель
БДУ-Д4-2	Нет производителя
БДУ-Д4-2	ДонЭнергоЗавод
БДУ-Д.01	Без Производителя

"""

from sys import exit
from time import sleep
from gen_func_utils import *
from my_msgbox import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["st_test_bdu_d4_2"]

reset = ResetRelay()
resist = Resistor()
ctrl_kl = CtrlKL()
read_mb = ReadMB()
mysql_conn = MySQLConnect()
fault = Bug(True)


def st_test_bdu_d4_2():
    # reset.reset_all()
    # Тест 1. Проверка исходного состояния блока:
    in_a1, in_a2 = __inputs_a()
    if in_a1 == False and in_a2 == False:
        pass
    else:
        fault.debug_msg('тест 1 неисправен', 1)
        mysql_conn.mysql_ins_result("неисправен", '1')
        if in_a1 == True:
            mysql_conn.mysql_error(5)
        elif in_a2 == True:
            mysql_conn.mysql_error(6)
        return False
    fault.debug_msg('тест 1 исправен', 4)
    mysql_conn.mysql_ins_result("исправен", '1')
    # Тест 2. Проверка включения выключения блока от кнопки «Пуск Стоп».
    # 2.1. Проверка исходного состояния блока
    ctrl_kl.ctrl_relay('KL2', True)
    sleep(1)
    in_a1, in_a2 = __inputs_a()
    if in_a1 == False and in_a2 == False:
        pass
    else:
        fault.debug_msg('тест 2.1 неисправен', 1)
        mysql_conn.mysql_ins_result("неисправен", '2')
        if in_a1 == True:
            mysql_conn.mysql_error(13)
        elif in_a2 == True:
            mysql_conn.mysql_error(14)
        return False
    fault.debug_msg('тест 2.1 исправен', 4)
    # 2.2. Включение блока от кнопки «Пуск»
    # 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
    if __subtest_22_23():
        pass
    else:
        return False
    # 2.4. Выключение блока от кнопки «Стоп»
    ctrl_kl.ctrl_relay('KL12', False)
    sleep(2)
    in_a1, in_a2 = __inputs_a()
    if in_a1 == False and in_a2 == False:
        pass
    else:
        fault.debug_msg('тест 2.4 неисправен', 1)
        mysql_conn.mysql_ins_result("неисправен", '2')
        if in_a1 == True:
            mysql_conn.mysql_error(17)
        elif in_a2 == True:
            mysql_conn.mysql_error(18)
        return False
    fault.debug_msg('тест 2.4 исправен', 4)
    ctrl_kl.ctrl_relay('KL12', False)
    ctrl_kl.ctrl_relay('KL1', False)
    ctrl_kl.ctrl_relay('KL25', False)
    mysql_conn.mysql_ins_result("исправен", '2')
    # 3. Отключение исполнительного элемента при увеличении сопротивления цепи заземления
    if __subtest_22_23():
        pass
    else:
        mysql_conn.mysql_ins_result("неисправен", '3')
        return False
    resist.resist_10_to_110_ohm()
    sleep(3)
    in_a1, in_a2 = __inputs_a()
    if in_a1 == False and in_a2 == False:
        pass
    else:
        fault.debug_msg('тест 3 неисправен', 1)
        mysql_conn.mysql_ins_result("неисправен", '3')
        if in_a1 == True:
            mysql_conn.mysql_error(19)
        elif in_a2 == True:
            mysql_conn.mysql_error(20)
        return False
    fault.debug_msg('тест 3 исправен', 4)
    ctrl_kl.ctrl_relay('KL12', False)
    ctrl_kl.ctrl_relay('KL25', False)
    ctrl_kl.ctrl_relay('KL1', False)
    mysql_conn.mysql_ins_result("исправен", '3')
    # Тест 4. Защита от потери управляемости при замыкании проводов ДУ
    if __subtest_22_23():
        pass
    else:
        mysql_conn.mysql_ins_result("неисправен", '4')
        return False
    ctrl_kl.ctrl_relay('KL11', True)
    sleep(1)
    in_a1, in_a2 = __inputs_a()
    if in_a1 == False and in_a2 == False:
        pass
    else:
        fault.debug_msg('тест 4 неисправен', 1)
        mysql_conn.mysql_ins_result("неисправен", '4')
        if in_a1 == True:
            mysql_conn.mysql_error(9)
        elif in_a2 == True:
            mysql_conn.mysql_error(10)
        return False
    fault.debug_msg('тест 4 исправен', 4)
    ctrl_kl.ctrl_relay('KL12', False)
    ctrl_kl.ctrl_relay('KL25', False)
    ctrl_kl.ctrl_relay('KL1', False)
    ctrl_kl.ctrl_relay('KL11', False)
    mysql_conn.mysql_ins_result("исправен", '4')
    # Тест 5. Защита от потери управляемости при обрыве проводов ДУ
    if __subtest_22_23():
        pass
    else:
        mysql_conn.mysql_ins_result("неисправен", '5')
        return False
    ctrl_kl.ctrl_relay('KL12', False)
    sleep(1)
    in_a1, in_a2 = __inputs_a()
    if in_a1 == False and in_a2 == False:
        pass
    else:
        fault.debug_msg('тест 5 неисправен', 1)
        mysql_conn.mysql_ins_result("неисправен", '5')
        if in_a1 == True:
            mysql_conn.mysql_error(11)
        elif in_a2 == True:
            mysql_conn.mysql_error(12)
        return False
    fault.debug_msg('тест 5 исправен', 4)
    mysql_conn.mysql_ins_result("исправен", '5')
    return True


def __subtest_22_23():
    # 2.2. Включение блока от кнопки «Пуск»
    resist.resist_ohm(255)
    resist.resist_ohm(10)
    ctrl_kl.ctrl_relay('KL12', True)
    sleep(1)
    in_a1, in_a2 = __inputs_a()
    if in_a1 == True and in_a2 == True:
        pass
    else:
        fault.debug_msg('тест 2.2 неисправен', 1)
        if in_a1 == False:
            mysql_conn.mysql_error(15)
        elif in_a2 == False:
            mysql_conn.mysql_error(16)
        return False
    fault.debug_msg('тест 2.2 исправен', 4)
    # 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
    ctrl_kl.ctrl_relay('KL1', True)
    ctrl_kl.ctrl_relay('KL25', True)
    sleep(1)
    in_a1, in_a2 = __inputs_a()
    if in_a1 == True and in_a2 == True:
        pass
    else:
        fault.debug_msg('тест 2.3 неисправен', 1)
        if in_a1 == False:
            mysql_conn.mysql_error(7)
        elif in_a2 == False:
            mysql_conn.mysql_error(8)
        return False
    fault.debug_msg('тест 2.3 исправен', 4)
    return True


def __inputs_a():
    in_a1 = read_mb.read_discrete(1)
    in_a2 = read_mb.read_discrete(2)
    return in_a1, in_a2


if __name__ == '__main__':
    try:
        if st_test_bdu_d4_2():
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
