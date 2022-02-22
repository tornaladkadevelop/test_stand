#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Алгоритм проверки

Тип блока	Производитель
БП	Строй-энергомаш
БП	ТЭТЗ-Инвест
БП	нет производителя


"""

import math

from sys import exit
from time import sleep
from my_msgbox import *
from gen_func_procedure import *
from gen_func_utils import *
from gen_mb_client import *
from gen_mysql_connect import *

__all__ = ["TestBP"]

proc = Procedure()
reset = ResetRelay()
resist = Resistor()
mb_ctrl = CtrlKL()
read_mb = ReadMB()
mysql_conn = MySQLConnect()
fault = Bug(True)


class TestBP(object):
    def __init__(self):
        pass
    
    def st_test_bp(self):
        # reset.reset_all()
        # Тест 1. Проверка исходного состояния блока:
        # Переключение АЦП на AI.1 канал
        msg_1 = "Убедитесь в отсутствии других блоков и вставьте блок БП в соответствующий разъем"
        if my_msg(msg_1):
            pass
        else:
            return False
        mysql_conn.mysql_ins_result("идёт тест 1", "1")
        fault.debug_msg("тест 1", 3)
        mb_ctrl.ctrl_relay('KL78', True)
        in_a1, in_a2, in_a6, in_a7 = self.__inputs_a()
        fault.debug_msg(str(in_a1) + "\t" + str(in_a2) + "\t" + str(in_a6) + "\t" + str(in_a7), 3)
        if in_a6 == True and in_a1 == False and in_a7 == True and in_a2 == False:
            pass
        else:
            fault.debug_msg("тест 1 положение выходов не соответствует", 1)
            mysql_conn.mysql_ins_result("неисправен", "1")
            return False
        fault.debug_msg("тест 1 положение выходов соответствует", 4)
        mysql_conn.mysql_ins_result("исправен", "1")
        # Тест 2. Определение ёмкости пусковых конденсаторов
        # 2.1. Заряд конденсаторов
        mysql_conn.mysql_ins_result("идёт тест 2.1", "2")
        fault.debug_msg("тест 2", 3)
        mb_ctrl.ctrl_relay('KL77', True)
        sleep(0.3)
        mb_ctrl.ctrl_relay('KL65', True)
        sleep(0.3)
        mb_ctrl.ctrl_relay('KL66', True)
        sleep(5)
        mb_ctrl.ctrl_relay('KL76', True)
        sleep(5)
        zaryad_1 = read_mb.read_analog_ai2()
        fault.debug_msg("заряд конденсатора по истечении 5с \t" + str(zaryad_1) + "В", 2)
        if zaryad_1 != 999:
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", "2")
            fault.debug_msg("тест 2 не пройден", 1)
            return False
        sleep(15)
        zaryad_2 = read_mb.read_analog_ai2()
        fault.debug_msg("заряд конденсатора по истечении 15с \t" + str(zaryad_2) + "В", 2)
        if zaryad_2 != 999:
            pass
        else:
            mysql_conn.mysql_ins_result("неисправен", "2")
            fault.debug_msg("тест 2 не пройден", 1)
            return False
        delta_zaryad = zaryad_1 - zaryad_2
        fault.debug_msg("дельта заряда конденсатора\t" + str(delta_zaryad) + "В", 2)
        if delta_zaryad != 0:
            pass
        else:
            mb_ctrl.ctrl_relay('KL77', False)
            sleep(0.1)
            mb_ctrl.ctrl_relay('KL65', False)
            sleep(0.1)
            mb_ctrl.ctrl_relay('KL76', False)
            mb_ctrl.ctrl_relay('KL66', False)
            mb_ctrl.ctrl_relay('KL78', False)
            mysql_conn.mysql_ins_result("неисправен", "2")
            fault.debug_msg("тест 2 не пройден", 1)
            return False
        # С1=ln(volt1/ volt2)
        emkost_kond = math.log(zaryad_1/zaryad_2)
        fault.debug_msg("ёмкость\t" + str(emkost_kond), 2)
        # C1 = t2/C1/31300
        emkost_kond = (15000 / emkost_kond / 31300) * 1000
        fault.debug_msg("ёмкость\t" + str(emkost_kond), 2)
        # C1=C1*1000
        # Cd = 100-100*(C1/2000)
        emkost_kond_d = 100 - 100 * (emkost_kond / 2000)
        fault.debug_msg("ёмкость\t" + str(emkost_kond_d), 2)
        # C1 ≥ 0.8*2000
        if emkost_kond >= 1600:
            pass
        else:
            mb_ctrl.ctrl_relay('KL77', False)
            sleep(0.1)
            mb_ctrl.ctrl_relay('KL65', False)
            sleep(0.1)
            mb_ctrl.ctrl_relay('KL76', False)
            mb_ctrl.ctrl_relay('KL66', False)
            mb_ctrl.ctrl_relay('KL78', False)
            mysql_conn.mysql_ins_result("неиспр. емкость снижена на" + str(round(emkost_kond_d, 1)) + "%", "2")
            fault.debug_msg("тест 2 не пройден", 1)
            return False
        # 2.3. Форсированный разряд
        mysql_conn.mysql_ins_result("идёт тест 2.3", "2")
        fault.debug_msg("тест 2.3", 3)
        mb_ctrl.ctrl_relay('KL79', True)
        sleep(1)
        mb_ctrl.ctrl_relay('KL79', False)
        sleep(0.3)
        mysql_conn.mysql_ins_result("исправен", "2")
        mysql_conn.mysql_ins_result(str(round(emkost_kond, 1)), "3")
        mysql_conn.mysql_ins_result(str(round(emkost_kond_d, 1)), "4")
        # Тест 3. Проверка работоспособности реле удержания
        mysql_conn.mysql_ins_result("идёт тест 3", "5")
        fault.debug_msg("тест 3", 3)
        mb_ctrl.ctrl_relay('KL75', True)
        sleep(0.3)
        in_a1, in_a2, in_a6, in_a7 = self.__inputs_a()
        fault.debug_msg(str(in_a1) + "\t" + str(in_a2) + "\t" + str(in_a6) + "\t" + str(in_a7), 3)
        if in_a6 == False and in_a1 == True and in_a7 == False and in_a2 == True:
            pass
        else:
            fault.debug_msg("тест 3 положение выходов не соответствует", 1)
            mb_ctrl.ctrl_relay('KL77', False)
            sleep(0.1)
            mb_ctrl.ctrl_relay('KL65', False)
            sleep(0.1)
            mb_ctrl.ctrl_relay('KL76', False)
            mb_ctrl.ctrl_relay('KL66', False)
            mb_ctrl.ctrl_relay('KL78', False)
            mb_ctrl.ctrl_relay('KL75', False)
            mysql_conn.mysql_ins_result("неисправен", "5")
            fault.debug_msg("тест 3 не пройден", 1)
            return False
        fault.debug_msg("тест 3 положение выходов соответствует", 4)
        mysql_conn.mysql_ins_result("исправен", "5")
        # Тест 4. Проверка работоспособности реле удержания
        # Измерение	A0:AI.1
        # Вычисление	volt3 = (A0:AI.1)*(103/3)
        # Состояние правильное	volt3  ≥ 6В
        mysql_conn.mysql_ins_result("идёт тест 4", "6")
        fault.debug_msg("тест 4", 3)
        meas_volt = read_mb.read_analog_ai2()
        calc_volt = meas_volt * (103 / 3)
        fault.debug_msg("вычисленное напряжение, должно быть больше 6\t" + str(calc_volt), 2)
        if calc_volt >= 6:
            pass
        else:
            mb_ctrl.ctrl_relay('KL77', False)
            sleep(0.1)
            mb_ctrl.ctrl_relay('KL65', False)
            sleep(0.1)
            mb_ctrl.ctrl_relay('KL75', False)
            mb_ctrl.ctrl_relay('KL76', False)
            mb_ctrl.ctrl_relay('KL66', False)
            mb_ctrl.ctrl_relay('KL78', False)
            mysql_conn.mysql_ins_result("неисправен", "6")
            fault.debug_msg("тест 4 не пройден", 1)
            return False
        mb_ctrl.ctrl_relay('KL77', False)
        sleep(0.1)
        mb_ctrl.ctrl_relay('KL65', False)
        sleep(0.1)
        mb_ctrl.ctrl_relay('KL75', False)
        mb_ctrl.ctrl_relay('KL76', False)
        mb_ctrl.ctrl_relay('KL66', False)
        mb_ctrl.ctrl_relay('KL78', False)
        mysql_conn.mysql_ins_result("исправен", "6")
        fault.debug_msg("тест 4 пройден", 4)
        return True
    
    def __inputs_a(self):
        in_a1 = read_mb.read_discrete(1)
        in_a2 = read_mb.read_discrete(2)
        in_a6 = read_mb.read_discrete(6)
        in_a7 = read_mb.read_discrete(7)
        return in_a1, in_a2, in_a6, in_a7


if __name__ == '__main__':
    try:
        test_bp = TestBP()
        if test_bp.st_test_bp():
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
