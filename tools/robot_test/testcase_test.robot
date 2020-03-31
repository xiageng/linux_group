*** Settings ***
Library          OperatingSystem

*** Variables ***
${message}   Hello, World!

*** Test Cases ***
My test
    Log    ${message}
    My Keyword  C:\linux\linux group\project\robot_test

*** Keywords ***
My Keyword
   [Arguments]    ${path}
    Directory Should Exist    ${path}