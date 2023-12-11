import types
from alpGenerator import *
from getConfigFile import *


"""
코드의 정상적인 동작유무를 확인하기 위한 파이썬 테스트 파일이다.
테스트는 pytest 모듈을 활용한다.
"""


def test_alpGenerator() -> None:
    """
    aaa ~ zzz 까지를 생성해주는 alpGenterator 테스트 함수
    :Test 1: Generator type이 return 되는지 확인
    :Test 2: Generator로 생성된 값의 개수가 일치하는지 확인
    :Test 3-1: Generator의 임의의 값(5번째 값)이 일치하는지 확인
    :Test 3-2: Generator의 임의의 값(뒤에서 3번째 값)이 일치하는지 확인
    """
    alps = alpGenerator()
    assert type(alps) == types.GeneratorType, "alpGenrator 함수가 Generator 함수가 아닙니다."

    alps = alpGenerator()
    assert len(list(alps)) == 26 * 26 * 26, "alpGenrator 함수가 생성하는 값의 개수가 일치하지 않습니다."

    alps = alpGenerator()
    assert list(alps)[4] == "aae", "alpGenerator 함수가 생성하는 5번 째 값이 일치하지 않습니다."

    alps = alpGenerator()
    assert list(alps)[-3] == "zzx", "alpGenerator 함수가 생성하는 뒤에서 3번 째 값이 일치하지 않습니다."


def testConfigManager() -> None:
    """ """
    CM = ConfigManager()
    assert type(CM) == types.ClassMethodDescriptorType, "ConfigManger가 클래스 자료형이 아닙니다."
