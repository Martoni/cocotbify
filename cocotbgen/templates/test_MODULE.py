#! /usr/bin/python3
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Author:   
# Created:  
#-----------------------------------------------------------------------------
#  
#-----------------------------------------------------------------------------
""" test_MODULE
"""
import os
import sys
import cocotb
import logging
from cocotb import SimLog
from cocotb.clock import Clock
from cocotb.result import TestError
from cocotb.result import ReturnValue
from cocotb.binary import BinaryValue
from cocotb.triggers import Timer
from cocotb.triggers import RisingEdge
from cocotb.triggers import FallingEdge


class MODULE(object):
    """ test class for MODULE 
    """
    LOGLEVEL = logging.INFO
    # clock frequency is 50Mhz
    PERIOD = (20, "ns")

    def __init__(self, dut):
        if sys.version_info[0] < 3:
            raise Exception("Must be using Python 3")
        self._dut = dut
        self.log = SimLog("MODULE.{}".format(self.__class__.__name__))
        self._dut._log.setLevel(self.LOGLEVEL)
        self.log.setLevel(self.LOGLEVEL)
        self.clock = Clock(self._dut.clock, self.PERIOD[0], self.PERIOD[1])
        self._clock_thread = cocotb.fork(self.clock.start())

    @cocotb.coroutine
    def reset(self):
        self._dut.reset <= 1
        short_per = Timer(100, units="ns")
        yield short_per
        self._dut.reset <= 0


@cocotb.test()#skipe=True)
def test_simple_with_error(dut):
    tbobj = MODULE(dut)
    yield tbobj.reset()
    yield Timer(200, units="ns")

