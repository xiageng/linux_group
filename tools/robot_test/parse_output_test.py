#! /user/bin/enn python
#-*- coding: utf-8 -*-

from robot.result.visitor import ResultVisitor
from robot.result.executionresult import Result
from robot.utils import ETSource
from robot.result.resultbuilder import ExecutionResult, ExecutionResultBuilder

def test_outputfile(source_xml):
    ets = ETSource(source_xml)
    test_result = Result(source=source_xml)
    test_result=ExecutionResultBuilder(ets).build(test_result)
    #test_resultvisitor= ResultVisitor()
    #test_result.visit(test_resultvisitor)
    print("gxy")

if __name__ == "__main__":
    source_xml=r"C:\linux\linux group\project\robot_test\output.xml"
    #source_xml = r"C:\linux\linux group\project\robot_test\LTE2666_On_Air_with calibraiton_output.xml"
    test_outputfile(source_xml)
