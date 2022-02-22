#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тип блока     Производитель
БДУ             Без Производителя
БДУ             Углеприбор
БДУ-1           Без Производителя
БДУ-1           Углеприбор
БДУ-4           Без Производителя
БДУ-4           Углеприбор
БДУ-Т           Без Производителя
БДУ-Т           Углеприбор
БДУ-Т           ТЭТЗ-Инвест
БДУ-Т           Строй-ЭнергоМаш
БДУ-П Х5-01     Пульсар
БДУ-П УХЛ 01    Пульсар
БДУ-П УХЛ5-03   Пульсар
"""

from sys import exit
from time import sleep
from gen_func_utils import *
from my_msgbox import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["TestBDU014TP"]

reset = ResetRelay()
resist = Resistor()
fault = Bug(None)
result = Result()
ctrl_kl = CtrlKL()
read_mb = ReadMB()
mysql_conn = MySQLConnect()


class TestBDU014TP(object):
    def __init__(self):
        pass
    
    def st_test_bdu_014tp(self):
        """
        :return:
        """
        # reset.reset_all()
        # Тест 1. Проверка исходного состояния блока:
        mysql_conn.mysql_ins_result("идет тест 1", "1")
        in_a0, in_a1 = self.__inputs_a()
        if in_a1 == False:
            # in_a0 == True and
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", "1")
            result.test_error(1)
            mysql_conn.mysql_error(476)
            return False
        mysql_conn.mysql_ins_result("исправен", "1")
        # Тест 2. Проверка включения / выключения блока от кнопки «Пуск / Стоп».
        mysql_conn.mysql_ins_result("идет тест 2", "2")
        ctrl_kl.ctrl_relay('KL2', True)
        # 2.1. Проверка исходного состояния блока
        mysql_conn.mysql_ins_result("идет тест 2.1", "2")
        in_a0, in_a1 = self.__inputs_a()
        sleep(1)
        if in_a1 == False:
            # in_a0 == True and
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", "2")
            result.test_error(2.1)
            return False
        # 2.2. Включение канала блока от кнопки «Пуск» при сопротивлении 10 Ом
        mysql_conn.mysql_ins_result("идет тест 2.2", "2")
        if self.__subtest_22():
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", "2")
            mysql_conn.mysql_error(26)
            result.test_error(2.2)
            return False
        # 2.3. Выключение канала блока от кнопки «Пуск» при сопротивлении 10 Ом
        mysql_conn.mysql_ins_result("идет тест 2.3", "2")
        ctrl_kl.ctrl_relay('KL12', False)
        sleep(1)
        in_a0, in_a1 = self.__inputs_a()
        if in_a1 == False:
            # in_a0 == True and
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", "2")
            mysql_conn.mysql_error(27)
            result.test_error(2.3)
            return False
        mysql_conn.mysql_ins_result("исправен", "2")
        # 3. Удержание исполнительного элемента при сопротивлении цепи заземления до 35 Ом
        mysql_conn.mysql_ins_result("идет тест 3", "3")
        if self.__subtest_22():
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", "3")
            mysql_conn.mysql_error(26)
            result.test_error(3)
            return False
        resist.resist_10_to_35_ohm()
        sleep(1)
        in_a0, in_a1 = self.__inputs_a()
        if in_a1 == True:
            # in_a0 == False and
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", "3")
            mysql_conn.mysql_error(28)
            result.test_error(3.1)
            return False
        mysql_conn.mysql_ins_result("исправен", "3")
        # 4. Отключение исполнительного элемента при сопротивлении цепи заземления свыше 50 Ом
        mysql_conn.mysql_ins_result("идет тест 4", "4")
        resist.resist_35_to_110_ohm()
        in_a0, in_a1 = self.__inputs_a()
        if in_a1 == False:
            # in_a0 == True and
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", "4")
            mysql_conn.mysql_error(29)
            result.test_error(4.0)
            return False
        ctrl_kl.ctrl_relay('KL12', False)
        ctrl_kl.ctrl_relay('KL1', False)
        mysql_conn.mysql_ins_result("исправен", "4")
        # 5. Защита от потери управляемости при замыкании проводов ДУ
        mysql_conn.mysql_ins_result("идет тест 5", "5")
        if self.__subtest_22():
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", "5")
            mysql_conn.mysql_error(26)
            result.test_error(5.0)
            return False
        ctrl_kl.ctrl_relay('KL11', True)
        in_a0, in_a1 = self.__inputs_a()
        if in_a1 == False:
            # in_a0 == True and
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", "5")
            mysql_conn.mysql_error(3)
            result.test_error(5.1)
            return False
        ctrl_kl.ctrl_relay('KL12', False)
        ctrl_kl.ctrl_relay('KL1', False)
        ctrl_kl.ctrl_relay('KL11', False)
        mysql_conn.mysql_ins_result("исправен", "5")
        # Тест 6. Защита от потери управляемости при обрыве проводов ДУ
        if self.__subtest_22():
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", "6")
            mysql_conn.mysql_error(26)
            result.test_error(6.0)
            return False
        ctrl_kl.ctrl_relay('KL12', False)
        in_a0, in_a1 = self.__inputs_a()
        if in_a1 == False:
            # in_a0 == True and
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", "6")
            mysql_conn.mysql_error(4)
            result.test_error(6.1)
            return False
        mysql_conn.mysql_ins_result("исправен", "6")
        result.test_good()
        return True
    
    def __subtest_22(self):
        resist.resist_ohm(255)
        resist.resist_ohm(10)
        ctrl_kl.ctrl_relay('KL12', True)
        ctrl_kl.ctrl_relay('KL1', True)
        sleep(1)
        in_a0, in_a1 = self.__inputs_a()
        if in_a1 == True:
            # in_a0 == False and
            return True
        else:
            return False
    
    def __inputs_a(self):
        in_a0 = read_mb.read_discrete(0)
        in_a1 = read_mb.read_discrete(1)
        return in_a0, in_a1


if __name__ == '__main__':
    try:
        test_bdu_014tp = TestBDU014TP()
        if test_bdu_014tp.st_test_bdu_014tp():
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
