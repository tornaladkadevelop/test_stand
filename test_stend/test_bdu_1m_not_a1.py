#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тип блока     Производитель
БДУ-1М  Нет производителя
БДУ-1М  Пульсар
"""

from sys import exit
from time import sleep
from gen_func_utils import *
from my_msgbox import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["st_test_bdu_1m"]

reset = ResetRelay()
resist = Resistor()
ctrl_kl = CtrlKL()
read_mb = ReadMB()
mysql_conn = MySQLConnect()
fault = Bug(True)


def st_test_bdu_1m():
    # reset.reset_all()
    mysql_conn.mysql_ins_result("идёт тест 1", '1')
    in_a1, in_a2 = __inputs_a()
    fault.debug_msg('выходы\t' + str(in_a1) + "\t" + str(in_a2), 3)
    if in_a2 == False:
        pass
    else:
        fault.debug_msg('тест 1 положение выходов не соответствует', 1)
        mysql_conn.mysql_ins_result("неисправен", '1')
        if in_a1 == True:
            mysql_conn.mysql_error(198)
        elif in_a2 == True:
            mysql_conn.mysql_error(199)
        return False
    fault.debug_msg('тест 1 положение выходов соответствует', 4)
    mysql_conn.mysql_ins_result("исправен", '1')
    # Тест 2. Проверка включения / выключения блока от кнопки «Пуск / Стоп».
    mysql_conn.mysql_ins_result("идёт тест 2.1", '2')
    ctrl_kl.ctrl_relay('KL22', True)
    sleep(1)
    ctrl_kl.ctrl_relay('KL21', True)
    sleep(1)
    ctrl_kl.ctrl_relay('KL2', True)
    sleep(1)
    ctrl_kl.ctrl_relay('KL33', True)
    sleep(1)
    ctrl_kl.ctrl_relay('KL32', True)
    sleep(1)
    in_a1, in_a2 = __inputs_a()
    fault.debug_msg('выходы\t' + str(in_a1) + "\t" + str(in_a2), 3)
    if in_a2 == False:
        pass
    else:
        fault.debug_msg('тест 2.1 положение выходов не соответствует', 1)
        mysql_conn.mysql_ins_result("неисправен", '2')
        if  in_a1 == False:
            mysql_conn.mysql_error(200)
        elif in_a2 == True:
            mysql_conn.mysql_error(201)
        return False
    fault.debug_msg('тест 2.1 положение выходов соответствует', 4)
    # 2.2. Включение блока от кнопки «Пуск»
    # 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
    mysql_conn.mysql_ins_result("идёт тест 2.2", '2')
    if __subtest_22_23():
        pass
    else:
        fault.debug_msg('тест 2.2 положение выходов не соответствует', 1)
        mysql_conn.mysql_ins_result("неисправен", '2')
        return False
    fault.debug_msg('тест 2.2 положение выходов соответствует', 4)
    # 2.4. Выключение блока от кнопки «Стоп»
    mysql_conn.mysql_ins_result("идёт тест 2.3", '2')
    ctrl_kl.ctrl_relay('KL12', False)
    sleep(2)
    in_a1, in_a2 = __inputs_a()
    fault.debug_msg('выходы\t' + str(in_a1) + "\t" + str(in_a2), 3)
    if in_a2 == False:
        pass
    else:
        fault.debug_msg('тест 2.4 положение выходов не соответствует', 1)
        mysql_conn.mysql_ins_result("неисправен", '2')
        if in_a1 == False:
            mysql_conn.mysql_error(206)
        elif in_a2 == True:
            mysql_conn.mysql_error(207)
        return False
    fault.debug_msg('тест 2.4 положение выходов соответствует', 4)
    ctrl_kl.ctrl_relay('KL25', False)
    ctrl_kl.ctrl_relay('KL1', False)
    ctrl_kl.ctrl_relay('KL22', True)
    mysql_conn.mysql_ins_result("исправен", '2')
    # 3. Удержание исполнительного элемента при увеличении сопротивления цепи заземления до 50 Ом
    mysql_conn.mysql_ins_result("идёт тест 3.1", '3')
    if __subtest_22_23():
        pass
    else:
        fault.debug_msg('тест 3.1 положение выходов не соответствует', 1)
        mysql_conn.mysql_ins_result("неисправен", '3')
        return False
    fault.debug_msg('тест 3.1 положение выходов соответствует', 4)
    mysql_conn.mysql_ins_result("идёт тест 3.2", '3')
    resist.resist_10_to_20_ohm()
    sleep(3)
    in_a1, in_a2 = __inputs_a()
    fault.debug_msg('выходы\t' + str(in_a1) + "\t" + str(in_a2), 3)
    if in_a2 == True:
        pass
    else:
        fault.debug_msg('тест 3.2 положение выходов не соответствует', 1)
        mysql_conn.mysql_ins_result("неисправен", '3')
        if in_a1 == True:
            mysql_conn.mysql_error(208)
        elif in_a2 == False:
            mysql_conn.mysql_error(209)
        return False
    fault.debug_msg('тест 3.2 положение выходов соответствует', 4)
    mysql_conn.mysql_ins_result("исправен", '3')
    # 4. Отключение исполнительного элемента при увеличении сопротивления цепи заземления на величину свыше 50 Ом
    mysql_conn.mysql_ins_result("идёт тест 4.1", '4')
    if __subtest_22_23():
        pass
    else:
        fault.debug_msg('тест 4.1 положение выходов не соответствует', 1)
        mysql_conn.mysql_ins_result("неисправен", '4')
        return False
    fault.debug_msg('тест 4.1 положение выходов соответствует', 4)
    mysql_conn.mysql_ins_result("идёт тест 4.2", '4')
    resist.resist_10_to_100_ohm()
    sleep(2)
    in_a1, in_a2 = __inputs_a()
    fault.debug_msg('выходы\t' + str(in_a1) + "\t" + str(in_a2), 3)
    if in_a2 == False:
        pass
    else:
        fault.debug_msg('тест 4.2 положение выходов не соответствует', 1)
        mysql_conn.mysql_ins_result("неисправен", '4')
        if in_a1 == False:
            mysql_conn.mysql_error(210)
        elif in_a2 == True:
            mysql_conn.mysql_error(211)
        return False
    fault.debug_msg('тест 4.2 положение выходов соответствует', 4)
    ctrl_kl.ctrl_relay('KL12', False)
    ctrl_kl.ctrl_relay('KL25', False)
    mysql_conn.mysql_ins_result("исправен", '4')
    # 5. Защита от потери управляемости при замыкании проводов ДУ
    mysql_conn.mysql_ins_result("идёт тест 5.1", '5')
    if __subtest_22_23():
        pass
    else:
        fault.debug_msg('тест 5.1 положение выходов не соответствует', 1)
        mysql_conn.mysql_ins_result("неисправен", '5')
        return False
    fault.debug_msg('тест 5.1 положение выходов соответствует', 4)
    mysql_conn.mysql_ins_result("идёт тест 5.2", '5')
    ctrl_kl.ctrl_relay('KL11', True)
    sleep(2)
    in_a1, in_a2 = __inputs_a()
    fault.debug_msg('выходы\t' + str(in_a1) + "\t" + str(in_a2), 3)
    if in_a2 == False:
        pass
    else:
        fault.debug_msg('тест 5.2 положение выходов не соответствует', 1)
        mysql_conn.mysql_ins_result("неисправен", '5')
        if in_a1 == False:
            mysql_conn.mysql_error(212)
        elif in_a2 == True:
            mysql_conn.mysql_error(213)
        return False
    fault.debug_msg('тест 5.2 положение выходов соответствует', 4)
    ctrl_kl.ctrl_relay('KL12', False)
    ctrl_kl.ctrl_relay('KL1', False)
    ctrl_kl.ctrl_relay('KL25', False)
    ctrl_kl.ctrl_relay('KL11', False)
    mysql_conn.mysql_ins_result("исправен", '5')
    # Тест 6. Защита от потери управляемости при обрыве проводов ДУ
    mysql_conn.mysql_ins_result("идёт тест 6.1", '6')
    if __subtest_22_23():
        pass
    else:
        fault.debug_msg('тест 6.1 положение выходов не соответствует', 1)
        mysql_conn.mysql_ins_result("неисправен", '6')
        return False
    fault.debug_msg('тест 6.1 положение выходов соответствует', 4)
    mysql_conn.mysql_ins_result("идёт тест 6.2", '6')
    ctrl_kl.ctrl_relay('KL12', False)
    sleep(2)
    in_a1, in_a2 = __inputs_a()
    fault.debug_msg('выходы\t' + str(in_a1) + "\t" + str(in_a2), 3)
    if in_a2 == False:
        pass
    else:
        fault.debug_msg('тест 6.2 положение выходов не соответствует', 1)
        mysql_conn.mysql_ins_result("неисправен", '6')
        if in_a1 == False:
            mysql_conn.mysql_error(214)
        elif in_a2 == True:
            mysql_conn.mysql_error(215)
        return False
    fault.debug_msg('тест 6.2 положение выходов соответствует', 4)
    mysql_conn.mysql_ins_result("исправен", '6')
    return True


def __subtest_22_23():
    # 2.2. Включение блока от кнопки «Пуск»
    # resist.resist_ohm(255)
    ctrl_kl.ctrl_relay('KL22', True)
    ctrl_kl.ctrl_relay('KL1', False)
    ctrl_kl.ctrl_relay('KL25', False)
    sleep(1)
    resist.resist_ohm(10)
    sleep(1)
    ctrl_kl.ctrl_relay('KL12', True)
    sleep(1)
    in_a1, in_a2 = __inputs_a()
    fault.debug_msg('тест 2.2 выходы\t' + str(in_a1) + "\t" + str(in_a2), 3)
    if in_a2 == True:
        pass
    else:
        fault.debug_msg('тест 2.2 положение выходов не соответствует', 1)
        if in_a1 == False:
            mysql_conn.mysql_error(202)
        elif in_a2 == False:
            mysql_conn.mysql_error(203)
        return False
    fault.debug_msg('тест 2.2 положение выходов соответствует', 4)
    # 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
    ctrl_kl.ctrl_relay('KL1', True)
    ctrl_kl.ctrl_relay('KL22', False)
    sleep(1)
    ctrl_kl.ctrl_relay('KL25', True)
    sleep(1)
    in_a1, in_a2 = __inputs_a()
    fault.debug_msg('тест 2.4 выходы\t' + str(in_a1) + "\t" + str(in_a2), 3)
    if in_a2 == True:
        pass
    else:
        fault.debug_msg('тест 2.3 положение выходов не соответствует', 1)
        if in_a1 == False:
            mysql_conn.mysql_error(204)
        elif in_a2 == False:
            mysql_conn.mysql_error(205)
        return False
    fault.debug_msg('тест 2.3 положение выходов соответствует', 4)
    return True


def __inputs_a():
    in_a1 = read_mb.read_discrete(1)
    in_a2 = read_mb.read_discrete(2)
    return in_a1, in_a2


if __name__ == '__main__':
    try:
        if st_test_bdu_1m():
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
