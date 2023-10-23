from typing import Dict

from common.data_models.base import Diffable


def test_diff_two_objects():
    class A(Diffable):
        a: str
        b: float

    class B(Diffable):
        a: int
        b: str
        c: Dict[str, A]

    print(list(Diffable.diff(None, B(a=4, b='b', c={'d': A(a='a', b=5.6)}))))
    assert False
