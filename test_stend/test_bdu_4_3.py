#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки
Тип блока Производитель
БДУ-4-3	Без Производителя
БДУ-4-3	Углеприбор

"""

from sys import exit
from time import sleep
from gen_func_utils import *
from my_msgbox import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["st_test_bdu_4_3"]

reset = ResetRelay()
resist = Resistor()
result = Result()
read_mb = ReadMB()
ctrl_kl = CtrlKL()
mysql_conn = MySQLConnect()
fault = Bug(True)


def st_test_bdu_4_3():
    # reset.reset_all()
    # Тест 1. Проверка исходного состояния блока:
    mysql_conn.mysql_ins_result("идет тест 1", '1')
    in_a1 = __inputs_a()
    if in_a1 == False:
        pass
    else:
        mysql_conn.mysql_ins_result("неисправен", '1')
        result.test_error(1)
        return False
    mysql_conn.mysql_ins_result("исправен", '1')
    # Тест 2. Проверка включения выключения блока от кнопки «Пуск Стоп».
    # 2.1. Проверка исходного состояния блока
    mysql_conn.mysql_ins_result("идет тест 2", '2')
    ctrl_kl.ctrl_relay('KL2', True)
    in_a1 = __inputs_a()
    if in_a1 == False:
        pass
    else:
        mysql_conn.mysql_error(13)
        mysql_conn.mysql_ins_result("неисправен", '2')
        result.test_error(2.1)
        return False
    # 2.2. Включение блока от кнопки «Пуск»
    mysql_conn.mysql_ins_result("идет тест 2.2", '2')
    # 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
    mysql_conn.mysql_ins_result("идет тест 2.3", '2')
    if __subtest_22_23():
        pass
    else:
        mysql_conn.mysql_ins_result("неисправен", '2')
        return False
    # 2.4. Выключение блока от кнопки «Стоп»
    mysql_conn.mysql_ins_result("идет тест 2.4", '2')
    ctrl_kl.ctrl_relay('KL12', False)
    in_a1 = __inputs_a()
    if in_a1 == False:
        pass
    else:
        mysql_conn.mysql_error(23)
        mysql_conn.mysql_ins_result("неисправен", '2')
        result.test_error(2.4)
        return False
    ctrl_kl.ctrl_relay('KL25', False)
    ctrl_kl.ctrl_relay('KL1', False)
    mysql_conn.mysql_ins_result("исправен", '2')
    # 3. Отключение исполнительного элемента при увеличении сопротивления цепи заземления
    mysql_conn.mysql_ins_result("идет тест 3", '3')
    if __subtest_22_23():
        pass
    else:
        mysql_conn.mysql_ins_result("неисправен", '3')
        return False
    resist.resist_0_to_63_ohm()
    in_a1 = __inputs_a()
    if in_a1 == False:
        pass
    else:
        mysql_conn.mysql_error(24)
        mysql_conn.mysql_ins_result("неисправен", '3')
        result.test_error(3)
        return False
    ctrl_kl.ctrl_relay('KL12', False)
    ctrl_kl.ctrl_relay('KL25', False)
    ctrl_kl.ctrl_relay('KL1', False)
    mysql_conn.mysql_ins_result("исправен", '3')
    # Тест 4. Защита от потери управляемости при замыкании проводов ДУ
    mysql_conn.mysql_ins_result("идет тест 4", '4')
    if __subtest_22_23():
        pass
    else:
        mysql_conn.mysql_ins_result("неисправен", '4')
        return False
    ctrl_kl.ctrl_relay('KL11', True)
    in_a1 = __inputs_a()
    if in_a1 == False:
        pass
    else:
        mysql_conn.mysql_error(3)
        mysql_conn.mysql_ins_result("неисправен", '4')
        result.test_error(4)
        return False
    ctrl_kl.ctrl_relay('KL12', False)
    ctrl_kl.ctrl_relay('KL25', False)
    ctrl_kl.ctrl_relay('KL1', False)
    ctrl_kl.ctrl_relay('KL11', False)
    mysql_conn.mysql_ins_result("исправен", '4')
    # Тест 5. Защита от потери управляемости при обрыве проводов ДУ
    mysql_conn.mysql_ins_result("идет тест 5", '5')
    if __subtest_22_23():
        pass
    else:
        mysql_conn.mysql_ins_result("неисправен", '5')
        return False
    ctrl_kl.ctrl_relay('KL12', False)
    in_a1 = __inputs_a()
    if in_a1 == False:
        pass
    else:
        mysql_conn.mysql_error(4)
        mysql_conn.mysql_ins_result("неисправен", '5')
        result.test_error(5)
        return False
    mysql_conn.mysql_ins_result("исправен", '5')
    return True


def __subtest_22_23():
    # 2.2. Включение блока от кнопки «Пуск»
    resist.resist_ohm(0)
    ctrl_kl.ctrl_relay('KL12', True)
    sleep(1)
    in_a1 = __inputs_a()
    if in_a1 == True:
        pass
    else:
        mysql_conn.mysql_error(21)
        return False
    # 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
    ctrl_kl.ctrl_relay('KL1', True)
    ctrl_kl.ctrl_relay('KL25', True)
    sleep(1)
    in_a1 = __inputs_a()
    if in_a1 == True:
        return True
    else:
        mysql_conn.mysql_error(22)
        return False


def __inputs_a():
    in_a1 = read_mb.read_discrete(1)
    return in_a1


if __name__ == '__main__':
    try:
        if st_test_bdu_4_3():
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
