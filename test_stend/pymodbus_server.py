#!/usr/bin/env python
"""
Pymodbus Server Payload Example
--------------------------------------------------------------------------

Если вы хотите инициализировать контекст сервера со сложным
расположением памяти, вы можете использовать конструктор полезной нагрузки.
"""
# --------------------------------------------------------------------------- # 
# import the various server implementations
# --------------------------------------------------------------------------- # 
from pymodbus.version import version
from pymodbus.server.sync import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

# --------------------------------------------------------------------------- # 
# import the payload builder
# --------------------------------------------------------------------------- # 

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

# --------------------------------------------------------------------------- # 
# configure the service logging
# --------------------------------------------------------------------------- # 
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)


def run_payload_server():
    # ----------------------------------------------------------------------- #
    # создайте свою полезную нагрузку
    # ----------------------------------------------------------------------- #
    builder = BinaryPayloadBuilder(byteorder=Endian.Little,
                                   wordorder=Endian.Little)
    '''builder.add_string('abcdefgh')
    builder.add_bits([0, 1, 0, 1, 1, 0, 1, 0])
    builder.add_8bit_int(-0x12)
    builder.add_8bit_uint(0x12)
    '''
    builder.add_16bit_int(-0x5678)
    '''
    builder.add_16bit_uint(0x1234)
    builder.add_32bit_int(-0x1234)
    builder.add_32bit_uint(0x12345678)
    builder.add_16bit_float(12.34)
    builder.add_16bit_float(-12.34)
    builder.add_32bit_float(22.34)
    builder.add_32bit_float(-22.34)
    builder.add_64bit_int(-0xDEADBEEF)
    builder.add_64bit_uint(0x12345678DEADBEEF)
    builder.add_64bit_uint(0xDEADBEEFDEADBEED)
    builder.add_64bit_float(123.45)
    builder.add_64bit_float(-123.45)
    '''
    
    # ----------------------------------------------------------------------- #
    # используйте эту полезную нагрузку в хранилище данных
    # ----------------------------------------------------------------------- #
    # Здесь мы используем один и тот же ссылочный блок для каждого базового хранилища.
    # ----------------------------------------------------------------------- #
    
    block = ModbusSequentialDataBlock(1, builder.to_registers())
    store = ModbusSlaveContext(di=block, co=block, hr=block, ir=block)
    context = ModbusServerContext(slaves=store, single=True)
    
    # ----------------------------------------------------------------------- #
    # инициализируйте информацию о сервере
    # ----------------------------------------------------------------------- #
    # Если вы не зададите это или какие-либо другие поля, они по умолчанию
    # будут пустыми строками.
    # ----------------------------------------------------------------------- #
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = version.short()
    # ----------------------------------------------------------------------- #
    # запустите сервер, который вы хотите
    # ----------------------------------------------------------------------- #
    StartTcpServer(context, identity=identity, address=("localhost", 505))
    

if __name__ == "__main__":
    run_payload_server()
