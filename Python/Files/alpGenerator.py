import string
from typing import Generator


def alpGenerator() -> Generator:
    """
    aaa부터 zzz까지의 문자열을 순차적으로 반환해주는 Generator 함수
    """
    alp = list(string.ascii_lowercase)
    for i in alp:
        for j in alp:
            for k in alp:
                yield (i + j + k)
