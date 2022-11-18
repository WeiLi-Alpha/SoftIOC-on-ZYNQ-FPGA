#!/usr/bin/env python3

from softioc import softioc, builder, asyncio_dispatcher
import asyncio, time

## import neccesory libs and modules
from pynq.overlays.base import BaseOverlay
from pynq.lib import Pmod_IO
from pynq.lib.arduino import Arduino_Analog
from pynq.lib.arduino import ARDUINO_GROVE_A1,ARDUINO_GROVE_A2,ARDUINO_GROVE_A3\
    ,ARDUINO_GROVE_A4

base = BaseOverlay("base.bit")

PAOUT = [0]*8
PBIN  = [0]*8
for i in range(8):
        PAOUT[i] = Pmod_IO(base.PMODA,i,'out')
        PBIN[i]  = Pmod_IO(base.PMODB,i,'in')

AIN = [0]*4
AIN[0] = Arduino_Analog(base.ARDUINO, ARDUINO_GROVE_A1)
AIN[1] = Arduino_Analog(base.ARDUINO, ARDUINO_GROVE_A2)
AIN[2] = Arduino_Analog(base.ARDUINO, ARDUINO_GROVE_A3)
AIN[3] = Arduino_Analog(base.ARDUINO, ARDUINO_GROVE_A4)

# Create an asyncio dispatcher, the event loop is now running
dispatcher = asyncio_dispatcher.AsyncioDispatcher()

# Set the record prefix
builder.SetDeviceName("ARTY-Z720")

# Create some records
PA_OUT = [0]*8
PB_IN = [0]*8
BO_Init_Value = 0
for i in range(8):
    PA_OUT[i] = builder.boolOut("PAOUT"+str(i),ZNAM="OFF", ONAM="ON", initial_value=BO_Init_Value, always_update=True,on_update=PAOUT[i].write)
    PB_IN[i]  = builder.boolIn("PBIN"+str(i),  ZNAM="OFF", ONAM="ON", initial_value=PBIN[i].read())

A_IN = [0]*6
A_IN[0] = builder.aIn("AIN0",PREC=4,initial_value=AIN[0].read()[0])
A_IN[1] = builder.aIn("AIN1",PREC=4,initial_value=AIN[0].read()[1])
A_IN[2] = builder.aIn("AIN2",PREC=4,initial_value=AIN[1].read()[0])
A_IN[3] = builder.aIn("AIN3",PREC=4,initial_value=AIN[1].read()[1])
A_IN[4] = builder.aIn("AIN4",PREC=4,initial_value=AIN[2].read()[1])
A_IN[5] = builder.aIn("AIN5",PREC=4,initial_value=AIN[3].read()[1])

builder.LoadDatabase()
softioc.iocInit(dispatcher)

async def update():
    while True:
        #AIN_READ_VAL = AIN[0].read()[1]
        A_IN[0].set(AIN[0].read()[0])
        A_IN[1].set(AIN[0].read()[1])
        A_IN[2].set(AIN[1].read()[0])
        A_IN[3].set(AIN[1].read()[1])
        A_IN[4].set(AIN[2].read()[1])
        A_IN[5].set(AIN[3].read()[1])
        for i in range(8):
            PB_IN[i].set(PBIN[i].read())

        #print("READ=",AIN_READ_VAL,end="\r")
        await asyncio.sleep(0.1)

dispatcher(update)
softioc.interactive_ioc(globals())


            
