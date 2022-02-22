#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки
Тип блока Производитель
БДУ	Без Производителя
БДУ	Углеприбор

"""
from sys import exit
from time import sleep
from gen_func_utils import *
from my_msgbox import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["TestBDU"]

reset = ResetRelay()
resist = Resistor()
result = Result()
ctrl_kl = CtrlKL()
read_mb = ReadMB()
mysql_conn = MySQLConnect()
fault = Bug(True)


class TestBDU(object):
    def __init__(self):
        pass

    def st_test_bdu(self):
        # reset.reset_all()
        in_a1 = self.__inputs_a()
        if in_a1 == False:
            pass
        else:
            fault.debug_msg(f'{in_a1=} \tблок неисправен', 1)
            mysql_conn.mysql_ins_result('неисправен', '1')
            return False
        mysql_conn.mysql_ins_result('исправен', '1')
        fault.debug_msg(f'{in_a1=} \tтест 1 пройден', 3)
        # Тест-2 Проверка включения/отключения блока от кнопки пуск
        # Включение KL2
        ctrl_kl.ctrl_relay('KL2', True)
        sleep(3)
        # Тест-2.1 Проверка исходного состояния
        in_a1 = self.__inputs_a()
        if in_a1 == False:
            fault.debug_msg(f'{in_a1=} \tтест 2.1 пройден', 3)
        else:
            fault.debug_msg(f'{in_a1=} \tблок неисправен', 1)
            mysql_conn.mysql_ins_result('неисправен', '2')
            return False
        # Тест-2.2 Проверка канала блока от кнопки "Пуск"
        #  формируем 10 Ом
        resist.resist_ohm(10)
        sleep(3)
        ctrl_kl.ctrl_relay('KL12', True)
        sleep(3)
        in_a1 = self.__inputs_a()
        if in_a1 == True:
            fault.debug_msg(f'{in_a1=} \tтест 2.2 пройден', 3)
        else:
            fault.debug_msg(f'{in_a1=} \tТест 2.2 блок неисправен', 1)
            mysql_conn.mysql_ins_result('неисправен', '2')
            return False
        # Тест 2.3 Выключение канала блока от кнопки «Пуск» при сопротивлении 10 Ом
        sleep(3)
        ctrl_kl.ctrl_relay('KL12', False)
        sleep(3)
        in_a1 = self.__inputs_a()
        if in_a1 == False:
            fault.debug_msg(f'{in_a1=} \tтест 2.3 пройден', 3)
            mysql_conn.mysql_ins_result('исправен', '2')
        else:
            fault.debug_msg(f'{in_a1=} \tТест 2.3 блок неисправен', 1)
            mysql_conn.mysql_ins_result('неисправен', '2')
            return False
        # Тест-3. Удержание исполнительного элемента при сопротивлении цепи заземления до 35 Ом
        sleep(3)
        ctrl_kl.ctrl_relay('KL12', True)
        sleep(0.5)
        # Отключаем KL5, KL8 для формирования 35 Ом
        ctrl_kl.ctrl_relay('KL5', False)
        ctrl_kl.ctrl_relay('KL8', False)
        sleep(1)
        in_a1 = self.__inputs_a()
        if in_a1 == False:
            fault.debug_msg(f'{in_a1=} \tтест 3 пройден', 3)
            mysql_conn.mysql_ins_result('исправен', '3')
        else:
            fault.debug_msg(f'{in_a1=} \tТест 3 блок неисправен', 1)
            mysql_conn.mysql_ins_result('неисправен', '3')
            return False
        # Тест 4. Отключение исполнительного элемента при сопротивлении цепи заземления свыше 50 Ом
        ctrl_kl.ctrl_relay('KL7', False)
        ctrl_kl.ctrl_relay('KL9', False)
        ctrl_kl.ctrl_relay('KL4', True)
        ctrl_kl.ctrl_relay('KL6', True)
        ctrl_kl.ctrl_relay('KL10', True)
        in_a1 = self.__inputs_a()
        if in_a1 == False:
            fault.debug_msg(f'{in_a1=} \tтест 4 пройден', 3)
            mysql_conn.mysql_ins_result('исправен', '4')
        else:
            fault.debug_msg(f'{in_a1=} \tТест 4 блок неисправен', 1)
            mysql_conn.mysql_ins_result('неисправен', '4')
            return False
        ctrl_kl.ctrl_relay('KL12', True)
        sleep(0.5)
        # Тест 5. Защита от потери управляемости при замыкании проводов ДУ
        #  формируем 10 Ом
        resist.resist_ohm(10)
        sleep(1)
        ctrl_kl.ctrl_relay('KL12', True)
        sleep(0.5)
        ctrl_kl.ctrl_relay('KL11', True)
        sleep(1)
        in_a1 = self.__inputs_a()
        if in_a1 == False:
            fault.debug_msg(f'{in_a1=} \tтест 5 пройден', 3)
            mysql_conn.mysql_ins_result('исправен', '5')
        else:
            fault.debug_msg(f'{in_a1=} \tТест 5 блок неисправен', 1)
            mysql_conn.mysql_ins_result('неисправен', '5')
            return False
        ctrl_kl.ctrl_relay('KL12', False)
        ctrl_kl.ctrl_relay('KL11', False)
        ctrl_kl.ctrl_relay('KL1', False)
        # Тест 6. Защита от потери управляемости при обрыве проводов ДУ
        #  формируем 10 Ом
        resist.resist_ohm(10)
        sleep(1)
        ctrl_kl.ctrl_relay('KL12', True)
        sleep(1)
        ctrl_kl.ctrl_relay('KL12', False)
        in_a1 = self.__inputs_a()
        if in_a1 == False:
            fault.debug_msg(f'{in_a1=} \tтест 6 пройден', 3)
            mysql_conn.mysql_ins_result('исправен', '6')
            fault.debug_msg(f'{in_a1=} \tтест завершен', 3)
        else:
            fault.debug_msg(f'{in_a1=} \tТест 6 блок неисправен', 1)
            mysql_conn.mysql_ins_result('неисправен', '6')
            return False
        return True

    def __inputs_a(self):
        in_a1 = read_mb.read_discrete(1)
        return in_a1


if __name__ == '__main__':
    try:
        test_bdu = TestBDU()
        if test_bdu.st_test_bdu():
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
