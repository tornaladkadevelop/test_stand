#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки
Тип блока Производитель
БДУ-ДР.01	Нет производителя
БДУ-ДР.01	ДонЭнергоЗавод

"""

from sys import exit
from time import sleep
from gen_func_utils import *
from my_msgbox import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["TestBDUDR01"]

reset = ResetRelay()
resist = Resistor()
mb_read = ReadMB()
ctrl_kl = CtrlKL()
mysql_conn = MySQLConnect()
fault = Bug(True)


class TestBDUDR01(object):
    def __init__(self):
        pass
    
    def st_test_bdu_dr01(self):
        # reset.reset_all()
        # Тест 1. Проверка исходного состояния блока:
        mysql_conn.mysql_ins_result("идёт тест 1", '1')
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 == False and in_a2 == False and in_a3 == False and in_a4 == False:
            pass
        else:
            fault.debug_msg('тест 1 положение выходов не соответствует', 1)
            mysql_conn.mysql_ins_result("неисправен", '1')
            if in_a1 == True:
                mysql_conn.mysql_error(216)
            elif in_a2 == True:
                mysql_conn.mysql_error(217)
            elif in_a3 == True:
                mysql_conn.mysql_error(218)
            elif in_a4 == True:
                mysql_conn.mysql_error(219)
            return False
        fault.debug_msg('тест 1 положение выходов соответствует', 4)
        mysql_conn.mysql_ins_result("исправен", '1')
        # Тест 2. Проверка включения/выключения канала № 1 (К1)  блока от кнопки «Пуск/Стоп».
        mysql_conn.mysql_ins_result("идёт тест 2.1", '2')
        ctrl_kl.ctrl_relay('KL2', True)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 == False and in_a2 == False and in_a3 == False and in_a4 == False:
            pass
        else:
            fault.debug_msg('тест 2.1 положение выходов не соответствует', 1)
            mysql_conn.mysql_ins_result("неисправен", '2')
            if in_a1 == True:
                mysql_conn.mysql_error(220)
            elif in_a2 == True:
                mysql_conn.mysql_error(221)
            elif in_a3 == True:
                mysql_conn.mysql_error(222)
            elif in_a4 == True:
                mysql_conn.mysql_error(223)
            return False
        fault.debug_msg('тест 2.1 положение выходов соответствует', 4)
        # 2.2. Включение 1 канала блока от кнопки «Пуск» 1 канала
        # 2.3. Проверка удержания 1 канала блока во включенном состоянии
        # при подключении Rш пульта управления 1 каналом блока:
        mysql_conn.mysql_ins_result("идёт тест 2.2", '2')
        if self.__subtest_22_23():
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", '2')
            return False
        # 2.4. Выключение 1 канала блока от кнопки «Стоп»
        mysql_conn.mysql_ins_result("идёт тест 2.4", '2')
        ctrl_kl.ctrl_relay('KL12', False)
        sleep(1)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 == False and in_a2 == False and in_a3 == False and in_a4 == False:
            pass
        else:
            fault.debug_msg('тест 2.4 положение выходов не соответствует', 1)
            mysql_conn.mysql_ins_result("неисправен", '2')
            if in_a1 == True:
                mysql_conn.mysql_error(232)
            elif in_a2 == True:
                mysql_conn.mysql_error(233)
            elif in_a3 == True:
                mysql_conn.mysql_error(234)
            elif in_a4 == True:
                mysql_conn.mysql_error(235)
            return False
        fault.debug_msg('тест 2.4 положение выходов соответствует', 4)
        ctrl_kl.ctrl_relay('KL25', False)
        ctrl_kl.ctrl_relay('KL1', False)
        mysql_conn.mysql_ins_result("исправен", '2')
        # 3. Отключение исполнительного элемента 1 канала при увеличении сопротивления цепи заземления
        mysql_conn.mysql_ins_result("идёт тест 3.1", '3')
        if self.__subtest_22_23():
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", '3')
            return False
        mysql_conn.mysql_ins_result("идёт тест 3.2", '3')
        resist.resist_10_to_110_ohm()
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 == False and in_a2 == False and in_a3 == False and in_a4 == False:
            pass
        else:
            fault.debug_msg('тест 3 положение выходов не соответствует', 1)
            mysql_conn.mysql_ins_result("неисправен", '3')
            if in_a1 == True:
                mysql_conn.mysql_error(236)
            elif in_a2 == True:
                mysql_conn.mysql_error(237)
            elif in_a3 == True:
                mysql_conn.mysql_error(238)
            elif in_a4 == True:
                mysql_conn.mysql_error(239)
            return False
        fault.debug_msg('тест 3 положение выходов соответствует', 4)
        ctrl_kl.ctrl_relay('KL12', False)
        ctrl_kl.ctrl_relay('KL25', False)
        ctrl_kl.ctrl_relay('KL1', False)
        mysql_conn.mysql_ins_result("исправен", '3')
        # 4. Защита от потери управляемости 1 канала блока при замыкании проводов ДУ
        mysql_conn.mysql_ins_result("идёт тест 4.1", '4')
        if self.__subtest_22_23():
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", '4')
            return False
        mysql_conn.mysql_ins_result("идёт тест 4.2", '4')
        ctrl_kl.ctrl_relay('KL11', True)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 == False and in_a2 == False and in_a3 == False and in_a4 == False:
            pass
        else:
            fault.debug_msg('тест 4 положение выходов не соответствует', 1)
            mysql_conn.mysql_ins_result("неисправен", '4')
            if in_a1 == True:
                mysql_conn.mysql_error(240)
            elif in_a2 == True:
                mysql_conn.mysql_error(241)
            elif in_a3 == True:
                mysql_conn.mysql_error(242)
            elif in_a4 == True:
                mysql_conn.mysql_error(243)
            return False
        fault.debug_msg('тест 4 положение выходов не соответствует', 4)
        ctrl_kl.ctrl_relay('KL12', False)
        ctrl_kl.ctrl_relay('KL25', False)
        ctrl_kl.ctrl_relay('KL1', False)
        ctrl_kl.ctrl_relay('KL11', False)
        mysql_conn.mysql_ins_result("исправен", '4')
        # Тест 5. Защита от потери управляемости 1 канала блока при обрыве проводов ДУ
        mysql_conn.mysql_ins_result("идёт тест 5.1", '5')
        if self.__subtest_22_23():
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", '4')
            return False
        mysql_conn.mysql_ins_result("идёт тест 5.2", '5')
        ctrl_kl.ctrl_relay('KL12', False)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 == False and in_a2 == False and in_a3 == False and in_a4 == False:
            pass
        else:
            fault.debug_msg('тест 5 положение выходов не соответствует', 1)
            mysql_conn.mysql_ins_result("неисправен", '5')
            if in_a1 == True:
                mysql_conn.mysql_error(244)
            elif in_a2 == True:
                mysql_conn.mysql_error(245)
            elif in_a3 == True:
                mysql_conn.mysql_error(246)
            elif in_a4 == True:
                mysql_conn.mysql_error(247)
            return False
        fault.debug_msg('тест 5 положение выходов соответствует', 4)
        ctrl_kl.ctrl_relay('KL25', False)
        ctrl_kl.ctrl_relay('KL1', False)
        mysql_conn.mysql_ins_result("исправен", '5')
        # Тест 6. Проверка включения/выключения канала № 2 (К2)  блока от кнопки «Пуск/Стоп».
        mysql_conn.mysql_ins_result("идёт тест 6.1", '6')
        ctrl_kl.ctrl_relay('KL2', True)
        ctrl_kl.ctrl_relay('KL26', True)
        ctrl_kl.ctrl_relay('KL28', True)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 == False and in_a2 == False and in_a3 == False and in_a4 == False:
            pass
        else:
            fault.debug_msg('тест 6 положение выходов не соответствует', 1)
            mysql_conn.mysql_ins_result("неисправен", '6')
            if in_a1 == True:
                mysql_conn.mysql_error(248)
            elif in_a2 == True:
                mysql_conn.mysql_error(249)
            elif in_a3 == True:
                mysql_conn.mysql_error(250)
            elif in_a4 == True:
                mysql_conn.mysql_error(251)
            return False
        fault.debug_msg('тест 6 положение выходов соответствует', 4)
        # 2.2. Включение 1 канала блока от кнопки «Пуск» 1 канала
        # 2.3. Проверка удержания 1 канала блока во включенном состоянии
        # при подключении Rш пульта управления 1 каналом блока:
        mysql_conn.mysql_ins_result("идёт тест 6.2", '6')
        if self.__subtest_62_63():
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", '6')
            return False
        # 6.4. Выключение 2 канала блока от кнопки «Стоп»
        mysql_conn.mysql_ins_result("идёт тест 6.3", '6')
        ctrl_kl.ctrl_relay('KL12', False)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 == False and in_a2 == False and in_a3 == False and in_a4 == False:
            pass
        else:
            fault.debug_msg('тест 6.4 положение выходов не соответствует', 1)
            mysql_conn.mysql_ins_result("неисправен", '6')
            if in_a1 == True:
                mysql_conn.mysql_error(260)
            elif in_a2 == True:
                mysql_conn.mysql_error(261)
            elif in_a3 == True:
                mysql_conn.mysql_error(262)
            elif in_a4 == True:
                mysql_conn.mysql_error(263)
            return False
        fault.debug_msg('тест 6.4 положение выходов соответствует', 4)
        ctrl_kl.ctrl_relay('KL25', False)
        ctrl_kl.ctrl_relay('KL29', False)
        mysql_conn.mysql_ins_result("исправен", '6')
        # 7. Отключение исполнительного элемента 2 канала при увеличении сопротивления цепи заземления
        mysql_conn.mysql_ins_result("идёт тест 7.1", '7')
        if self.__subtest_62_63():
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", '7')
            return False
        mysql_conn.mysql_ins_result("идёт тест 7.2", '7')
        resist.resist_10_to_110_ohm()
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 == False and in_a2 == False and in_a3 == False and in_a4 == False:
            pass
        else:
            fault.debug_msg('тест 7 положение выходов не соответствует', 1)
            mysql_conn.mysql_ins_result("неисправен", '7')
            if in_a1 == True:
                mysql_conn.mysql_error(264)
            elif in_a2 == True:
                mysql_conn.mysql_error(265)
            elif in_a3 == True:
                mysql_conn.mysql_error(266)
            elif in_a4 == True:
                mysql_conn.mysql_error(267)
            return False
        fault.debug_msg('тест 7 положение выходов соответствует', 4)
        ctrl_kl.ctrl_relay('KL12', False)
        ctrl_kl.ctrl_relay('KL25', False)
        ctrl_kl.ctrl_relay('KL29', False)
        mysql_conn.mysql_ins_result("исправен", '7')
        # 8. Защита от потери управляемости 2 канала блока при замыкании проводов ДУ
        mysql_conn.mysql_ins_result("идёт тест 8.1", '8')
        if self.__subtest_62_63():
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", '7')
            return False
        mysql_conn.mysql_ins_result("идёт тест 8.2", '8')
        ctrl_kl.ctrl_relay('KL11', True)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 == False and in_a2 == False and in_a3 == False and in_a4 == False:
            pass
        else:
            fault.debug_msg('тест 8 положение выходов не соответствует', 1)
            mysql_conn.mysql_ins_result("неисправен", '8')
            if in_a1 == True:
                mysql_conn.mysql_error(268)
            elif in_a2 == True:
                mysql_conn.mysql_error(269)
            elif in_a3 == True:
                mysql_conn.mysql_error(270)
            elif in_a4 == True:
                mysql_conn.mysql_error(271)
            return False
        fault.debug_msg('тест 8 положение выходов соответствует', 4)
        ctrl_kl.ctrl_relay('KL12', False)
        ctrl_kl.ctrl_relay('KL25', False)
        ctrl_kl.ctrl_relay('KL29', False)
        ctrl_kl.ctrl_relay('KL11', False)
        mysql_conn.mysql_ins_result("исправен", '8')
        # Тест 9. Защита от потери управляемости 1 канала блока при обрыве проводов ДУ
        mysql_conn.mysql_ins_result("идёт тест 9.1", '9')
        if self.__subtest_62_63():
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", '9')
            return False
        mysql_conn.mysql_ins_result("идёт тест 9.2", '9')
        ctrl_kl.ctrl_relay('KL12', False)
        sleep(1)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 == False and in_a2 == False and in_a3 == False and in_a4 == False:
            pass
        else:
            fault.debug_msg('тест 9 положение выходов не соответствует', 1)
            mysql_conn.mysql_ins_result("неисправен", '9')
            if in_a1 == True:
                mysql_conn.mysql_error(272)
            elif in_a2 == True:
                mysql_conn.mysql_error(273)
            elif in_a3 == True:
                mysql_conn.mysql_error(274)
            elif in_a4 == True:
                mysql_conn.mysql_error(275)
            return False
        fault.debug_msg('тест 9 положение выходов соответствует', 4)
        mysql_conn.mysql_ins_result("исправен", '9')
        return True
    
    def __subtest_22_23(self):
        # 2.2. Включение 1 канала блока от кнопки «Пуск» 1 канала
        resist.resist_ohm(255)
        resist.resist_ohm(10)
        ctrl_kl.ctrl_relay('KL12', True)
        sleep(1)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 == True and in_a2 == True and in_a3 == False and in_a4 == False:
            pass
        else:
            fault.debug_msg('подтест 2.2 положение выходов не соответствует', 1)
            if in_a1 == False:
                mysql_conn.mysql_error(224)
            elif in_a2 == False:
                mysql_conn.mysql_error(225)
            elif in_a3 == True:
                mysql_conn.mysql_error(226)
            elif in_a4 == True:
                mysql_conn.mysql_error(227)
            return False
        fault.debug_msg('подтест 2.2 положение выходов соответствует', 4)
        # 2.3. Проверка удержания 1 канала блока во включенном состоянии
        # при подключении Rш пульта управления 1 каналом блока:
        ctrl_kl.ctrl_relay('KL1', True)
        ctrl_kl.ctrl_relay('KL25', True)
        sleep(1)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 == True and in_a2 == True and in_a3 == False and in_a4 == False:
            pass
        else:
            fault.debug_msg('подтест 2.3 положение выходов не соответствует', 1)
            if in_a1 == False:
                mysql_conn.mysql_error(228)
            elif in_a2 == False:
                mysql_conn.mysql_error(229)
            elif in_a3 == True:
                mysql_conn.mysql_error(230)
            elif in_a4 == True:
                mysql_conn.mysql_error(231)
            return False
        fault.debug_msg('подтест 2.3 положение выходов соответствует', 4)
        return True
    
    def __subtest_62_63(self):
        # 6.2. Включение 2 канала блока от кнопки «Пуск» 2 канала
        resist.resist_ohm(255)
        resist.resist_ohm(10)
        ctrl_kl.ctrl_relay('KL12', True)
        sleep(1)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 == False and in_a2 == False and in_a3 == True and in_a4 == True:
            pass
        else:
            fault.debug_msg('подтест 6.2 положение выходов не соответствует', 1)
            if in_a1 == True:
                mysql_conn.mysql_error(252)
            elif in_a2 == True:
                mysql_conn.mysql_error(253)
            elif in_a3 == False:
                mysql_conn.mysql_error(254)
            elif in_a4 == False:
                mysql_conn.mysql_error(255)
            return False
        fault.debug_msg('подтест 6.2 положение выходов соответствует', 4)
        # 6.3. Проверка удержания 2 канала блока во включенном состоянии
        # при подключении Rш пульта управления 2 каналом блока:
        ctrl_kl.ctrl_relay('KL29', True)
        ctrl_kl.ctrl_relay('KL25', True)
        sleep(1)
        in_a1, in_a2, in_a3, in_a4 = self.__inputs_a()
        if in_a1 == False and in_a2 == False and in_a3 == True and in_a4 == True:
            pass
        else:
            fault.debug_msg('подтест 6.3 положение выходов не соответствует', 1)
            if in_a1 == True:
                mysql_conn.mysql_error(256)
            elif in_a2 == True:
                mysql_conn.mysql_error(257)
            elif in_a3 == False:
                mysql_conn.mysql_error(258)
            elif in_a4 == False:
                mysql_conn.mysql_error(259)
            return False
        fault.debug_msg('подтест 6.3 положение выходов соответствует', 4)
        return True
    
    @staticmethod
    def __inputs_a():
        in_a1 = mb_read.read_discrete(1)
        in_a2 = mb_read.read_discrete(2)
        in_a3 = mb_read.read_discrete(3)
        in_a4 = mb_read.read_discrete(4)
        return in_a1, in_a2, in_a3, in_a4


if __name__ == '__main__':
    try:
        test_bdu_dr01 = TestBDUDR01()
        if test_bdu_dr01.st_test_bdu_dr01():
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
