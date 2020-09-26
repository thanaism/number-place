import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def group():
    from src.group import Group

    group = Group()
    print('\n')
    yield group


@pytest.mark.parametrize(
    'bool',
    [
        (True),
    ],
)
def test_can_replace(bool, group):
    from src.pysimplegui import show_on_gui

    # ジグソーシャッフル
    for _ in [1] * 50:
        group.shuffle()
        for i in group.members:
            assert len(i) == 9
    show_on_gui([*map(str, group.group)], group.show_lines(), False)
    # サムグループ生成
    group.get_new_random_group(2, 5)
    show_on_gui([*map(str, group.group)], group.show_lines(), False)


if __name__ == '__main__':
    parameter = '-sv'
    pytest.main([parameter, __file__])
