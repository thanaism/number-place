import requests
import pytest


def test_requests():
    from src.grid import Grid

    grid = Grid(np_type=2)
    grid.create()
    grid.create_problem(0)
    data_problem = {}
    for i in range(81):
        digit = grid.problem[i]
        sum = grid.group


if __name__ == '__main__':
    parameter = '-sv'
    pytest.main([parameter, __file__])
