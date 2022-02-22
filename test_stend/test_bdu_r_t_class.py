#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тип блока     Производитель
БДУ-Р-Т	Нет производителя
БДУ-Р-Т	ТЭТЗ-Инвест
БДУ-Р-Т	Стройэнергомаш

"""

from sys import exit
from time import sleep
from gen_func_utils import *
from my_msgbox import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["TestBDURT"]

reset = ResetRelay()
resist = Resistor()
ctrl_kl = CtrlKL()
read_mb = ReadMB()
mysql_conn = MySQLConnect()
fault = Bug(True)


class TestBDURT(object):
    def __init__(self):
        pass

    def st_test_bdu_r_t(self):
        # reset.reset_all()
        mysql_conn.mysql_ins_result("идет тест 1", '1')
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 == False and in_a2 == False:
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", '1')
            if in_a1 == True:
                mysql_conn.mysql_error(288)
            elif in_a2 == True:
                mysql_conn.mysql_error(288)
            return False
        mysql_conn.mysql_ins_result("исправен", "1")
        # Тест 2. Проверка включения/выключения блока от кнопки «Пуск/Стоп» в режиме «Вперед».
        mysql_conn.mysql_ins_result("идет тест 2", '2')
        ctrl_kl.ctrl_relay('KL2', True)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 == False and in_a2 == False:
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", '2')
            if  in_a1 == True:
                mysql_conn.mysql_error(290)
            elif in_a2 == True:
                mysql_conn.mysql_error(291)
            return False
        # 2.2. Включение блока от кнопки «Пуск» в режиме «Вперёд»
        # 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        mysql_conn.mysql_ins_result("идет тест 2.2", '2')
        if self.__subtest_22_23():
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", '2')
            return False
        # 2.4. Выключение блока в режиме «Вперед» от кнопки «Стоп»
        mysql_conn.mysql_ins_result("идет тест 2.4", '2')
        ctrl_kl.ctrl_relay('KL12', False)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 == False and in_a2 == False:
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", '2')
            if in_a1 == True:
                mysql_conn.mysql_error(296)
            elif in_a2 == True:
                mysql_conn.mysql_error(297)
            return False
        ctrl_kl.ctrl_relay('KL25', False)
        ctrl_kl.ctrl_relay('KL1', False)
        mysql_conn.mysql_ins_result("исправен", '2')
        # Тест 3. Проверка включения/выключения блока от кнопки «Пуск/Стоп» в режиме «Назад»
        # 3.1. Включение блока от кнопки «Пуск» в режиме «Назад»
        mysql_conn.mysql_ins_result("идет тест 3", '3')
        ctrl_kl.ctrl_relay('KL26', True)
        resist.resist_ohm(10)
        ctrl_kl.ctrl_relay('KL12', True)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 == False and in_a2 == True:
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", '3')
            if in_a1 == True:
                mysql_conn.mysql_error(298)
            elif in_a2 == False:
                mysql_conn.mysql_error(299)
            return False
        # 3.2. Проверка удержания контактов К5.2 режима «Назад» блока во включенном состоянии
        # при подключении Rш пульта управления:
        mysql_conn.mysql_ins_result("идет тест 3.2", '3')
        ctrl_kl.ctrl_relay('KL27', True)
        ctrl_kl.ctrl_relay('KL1', True)
        ctrl_kl.ctrl_relay('KL25', True)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 == True and in_a2 == False:
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", '3')
            if in_a1 == False:
                mysql_conn.mysql_error(300)
            elif in_a2 == True:
                mysql_conn.mysql_error(301)
            return False
        # 3.3. Выключение блока в режиме «Вперед» от кнопки «Стоп»
        mysql_conn.mysql_ins_result("идет тест 3.3", '3')
        ctrl_kl.ctrl_relay('KL12', False)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 == False and in_a2 == False:
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", '3')
            if in_a1 == True:
                mysql_conn.mysql_error(302)
            elif in_a2 == True:
                mysql_conn.mysql_error(303)
            return False
        ctrl_kl.ctrl_relay('KL26', False)
        ctrl_kl.ctrl_relay('KL27', False)
        ctrl_kl.ctrl_relay('KL1', False)
        ctrl_kl.ctrl_relay('KL25', False)
        mysql_conn.mysql_ins_result("исправен", '3')
        # 4. Отключение исполнительного элемента при увеличении сопротивления цепи заземления на величину свыше 50 Ом
        mysql_conn.mysql_ins_result("идет тест 4", '4')
        if self.__subtest_22_23():
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", '4')
            return False
        resist.resist_10_to_50_ohm()
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 == False and in_a2 == False:
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", '4')
            if in_a1 == True:
                mysql_conn.mysql_error(304)
            elif in_a2 == True:
                mysql_conn.mysql_error(305)
            return False
        ctrl_kl.ctrl_relay('KL12', False)
        ctrl_kl.ctrl_relay('KL25', False)
        ctrl_kl.ctrl_relay('KL1', False)
        mysql_conn.mysql_ins_result("исправен", '4')
        # 5. Защита от потери управляемости при замыкании проводов ДУ
        mysql_conn.mysql_ins_result("идет тест 5", '5')
        if self.__subtest_22_23():
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", '5')
            return False
        ctrl_kl.ctrl_relay('KL11', True)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 == False and in_a2 == False:
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", '5')
            if in_a1 == True:
                mysql_conn.mysql_error(306)
            elif in_a2 == True:
                mysql_conn.mysql_error(307)
            return False
        ctrl_kl.ctrl_relay('KL12', False)
        ctrl_kl.ctrl_relay('KL1', False)
        ctrl_kl.ctrl_relay('KL25', False)
        ctrl_kl.ctrl_relay('KL11', False)
        mysql_conn.mysql_ins_result("исправен", '5')
        # Тест 6. Защита от потери управляемости при обрыве проводов ДУ
        mysql_conn.mysql_ins_result("идет тест 6", '6')
        if self.__subtest_22_23():
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", '6')
            return False
        ctrl_kl.ctrl_relay('KL12', False)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 == False and in_a2 == False:
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", '6')
            if in_a1 == True:
                mysql_conn.mysql_error(308)
            elif in_a2 == True:
                mysql_conn.mysql_error(309)
            return False
        mysql_conn.mysql_ins_result("исправен", '6')
        # Тест 7. Проверка работоспособности функции "Проверка" блока
        mysql_conn.mysql_ins_result("идет тест 7", '7')
        ctrl_kl.ctrl_relay('KL24', True)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 == False and in_a2 == True:
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", '7')
            if in_a1 == True:
                mysql_conn.mysql_error(310)
            elif in_a2 == False:
                mysql_conn.mysql_error(311)
            return False
        mysql_conn.mysql_ins_result("исправен", '7')
        return True

    def __subtest_22_23(self):
        # 2.2. Включение блока от кнопки «Пуск»
        resist.resist_ohm(10)
        ctrl_kl.ctrl_relay('KL12', True)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 == True and in_a2 == False:
            pass
        else:
            if in_a1 == False:
                mysql_conn.mysql_error(292)
            elif in_a2 == True:
                mysql_conn.mysql_error(293)
            return False
        # 2.3. Проверка удержания блока во включенном состоянии при подключении Rш пульта управления:
        ctrl_kl.ctrl_relay('KL1', True)
        ctrl_kl.ctrl_relay('KL25', True)
        sleep(1)
        in_a1, in_a2 = self.__inputs_a()
        if in_a1 == True and in_a2 == False:
            pass
        else:
            if in_a1 == False:
                mysql_conn.mysql_error(294)
            elif in_a2 == False:
                mysql_conn.mysql_error(295)
            return False
        return True

    @staticmethod
    def __inputs_a():
        in_a1 = read_mb.read_discrete(1)
        in_a2 = read_mb.read_discrete(2)
        return in_a1, in_a2


if __name__ == '__main__':
    try:
        test_bdu_r_t = TestBDURT()
        if test_bdu_r_t.st_test_bdu_r_t():
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

