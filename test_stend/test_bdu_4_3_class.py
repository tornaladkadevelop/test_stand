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

__all__ = ["TestBDU43"]


class TestBDU43(object):

    __resist = Resistor()
    __result = Result()
    __read_mb = ReadMB()
    __ctrl_kl = CtrlKL()
    __mysql_conn = MySQLConnect()
    __fault = Bug(True)

    def __init__(self):
        pass
    
    def st_test_bdu_4_3(self):
        # reset.reset_all()
        # Тест 1. Проверка исходного состояния блока:
        self.__mysql_conn.mysql_ins_result("идет тест 1", '1')
        in_a1 = self.__inputs_a()
        if in_a1 == False:
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '1')
            self.__result.test_error(1)
            return False
        self.__mysql_conn.mysql_ins_result("исправен", '1')
        # Тест 2. Проверка включения выключения блока от кнопки «Пуск Стоп».
        # 2.1. Проверка исходного состояния блока
        self.__mysql_conn.mysql_ins_result("идет тест 2", '2')
        self.__ctrl_kl.ctrl_relay('KL2', True)
        in_a1 = self.__inputs_a()
        if in_a1 == False:
            pass
        else:
            self.__mysql_conn.mysql_error(13)
            self.__mysql_conn.mysql_ins_result("неисправен", '2')
            self.__result.test_error(2.1)
            return False
        # 2.2. Включение блока от кнопки «Пуск»
        self.__mysql_conn.mysql_ins_result("идет тест 2.2", '2')
        # 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        self.__mysql_conn.mysql_ins_result("идет тест 2.3", '2')
        if self.__subtest_22_23():
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '2')
            return False
        # 2.4. Выключение блока от кнопки «Стоп»
        self.__mysql_conn.mysql_ins_result("идет тест 2.4", '2')
        self.__ctrl_kl.ctrl_relay('KL12', False)
        in_a1 = self.__inputs_a()
        if in_a1 == False:
            pass
        else:
            self.__mysql_conn.mysql_error(23)
            self.__mysql_conn.mysql_ins_result("неисправен", '2')
            self.__result.test_error(24)
            return False
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__ctrl_kl.ctrl_relay('KL1', False)
        self.__mysql_conn.mysql_ins_result("исправен", '2')
        # 3. Отключение исполнительного элемента при увеличении сопротивления цепи заземления
        self.__mysql_conn.mysql_ins_result("идет тест 3", '3')
        if self.__subtest_22_23():
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '3')
            return False
        self.__resist.resist_0_to_63_ohm()
        in_a1 = self.__inputs_a()
        if in_a1 == False:
            pass
        else:
            self.__mysql_conn.mysql_error(24)
            self.__mysql_conn.mysql_ins_result("неисправен", '3')
            self.__result.test_error(3)
            return False
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__ctrl_kl.ctrl_relay('KL1', False)
        self.__mysql_conn.mysql_ins_result("исправен", '3')
        # Тест 4. Защита от потери управляемости при замыкании проводов ДУ
        self.__mysql_conn.mysql_ins_result("идет тест 4", '4')
        if self.__subtest_22_23():
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '4')
            return False
        self.__ctrl_kl.ctrl_relay('KL11', True)
        in_a1 = self.__inputs_a()
        if in_a1 == False:
            pass
        else:
            self.__mysql_conn.mysql_error(3)
            self.__mysql_conn.mysql_ins_result("неисправен", '4')
            self.__result.test_error(4)
            return False
        self.__ctrl_kl.ctrl_relay('KL12', False)
        self.__ctrl_kl.ctrl_relay('KL25', False)
        self.__ctrl_kl.ctrl_relay('KL1', False)
        self.__ctrl_kl.ctrl_relay('KL11', False)
        self.__mysql_conn.mysql_ins_result("исправен", '4')
        # Тест 5. Защита от потери управляемости при обрыве проводов ДУ
        self.__mysql_conn.mysql_ins_result("идет тест 5", '5')
        if self.__subtest_22_23():
            pass
        else:
            self.__mysql_conn.mysql_ins_result("неисправен", '5')
            return False
        self.__ctrl_kl.ctrl_relay('KL12', False)
        in_a1 = self.__inputs_a()
        if in_a1 == False:
            pass
        else:
            self.__mysql_conn.mysql_error(4)
            self.__mysql_conn.mysql_ins_result("неисправен", '5')
            self.__result.test_error(5)
            return False
        self.__mysql_conn.mysql_ins_result("исправен", '5')
        return True
    
    def __subtest_22_23(self):
        # 2.2. Включение блока от кнопки «Пуск»
        self.__resist.resist_ohm(0)
        self.__ctrl_kl.ctrl_relay('KL12', True)
        sleep(1)
        in_a1 = self.__inputs_a()
        if in_a1 == True:
            pass
        else:
            self.__mysql_conn.mysql_error(21)
            return False
        # 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        self.__ctrl_kl.ctrl_relay('KL1', True)
        self.__ctrl_kl.ctrl_relay('KL25', True)
        sleep(1)
        in_a1 = self.__inputs_a()
        if in_a1 == True:
            return True
        else:
            self.__mysql_conn.mysql_error(22)
            return False
    
    def __inputs_a(self) -> bool:
        in_a1 = self.__read_mb.read_discrete(1)
        if in_a1 is None:
            self.__fault.debug_msg(f'нет связи с контроллером', 1)
        return in_a1


if __name__ == '__main__':
    try:
        test_bdu_4_3 = TestBDU43()
        if test_bdu_4_3.st_test_bdu_4_3():
            self.__mysql_conn.mysql_block_good()
            my_msg('Блок исправен')
        else:
            self.__mysql_conn.mysql_block_bad()
            my_msg('Блок неисправен')
    except OSError:
        my_msg("ошибка системы")
    except SystemError:
        my_msg("внутренняя ошибка")
    finally:
        reset.reset_all()
        exit()
