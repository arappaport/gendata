import pytest
import json
from collections import OrderedDict
from gendata import gen_permutations, gen_random, prepare_col_opts


@pytest.fixture
def col_opts_test_data_one_level():
    col_opts = OrderedDict()
    col_opts["Col0"] =  {
        "Value0_A": 0.1,
        "Value0_B": 0.2,
        "Value0_C": 0.7
    }
    return dict(col_opts=col_opts,
                    total_cols_exp=1,
                    total_rows_exp=3)

@pytest.fixture
def col_opts_test_data_two_level(col_opts_test_data_one_level):
    test_data = col_opts_test_data_one_level
    col_opts = test_data['col_opts']
    col_opts["Col1"] =  {
        "Value1_A_half": 0.5,
        "Value1_B_half": 0.5
    }
    test_data['total_cols_exp'] += 1 #we added one column
    test_data['total_rows_exp'] *= 2 # we added 2 values. so 2x expected permutations
    return test_data


@pytest.fixture
def col_opts_test_data_three_level(col_opts_test_data_two_level):
    test_data = col_opts_test_data_two_level
    col_opts = test_data['col_opts']
    col_opts["Col2"] =  {
        "Value2_A_10perc": 0.10,
        "Value2_B_20perc": 0.20,
        "Value2_C_30perc": 0.30,
        "Value2_D_40perc_DEFAULT": "DEFAULT"
    }
    test_data['total_cols_exp'] += 1 #we added one column
    test_data['total_rows_exp'] *= 4 # we added 3 values. so 3x expected permutations
    return test_data

@pytest.fixture
def col_opts_test_data_four_level(col_opts_test_data_three_level):
    test_data = col_opts_test_data_three_level
    col_opts = test_data['col_opts']
    col_opts["Col3"] =  {
        "Value3_A_100perc": "DEFAULT"
    }

    test_data['total_cols_exp'] += 1 #we added one column
    test_data['total_rows_exp'] *= 1 # we added 1 value.  No additional rows
    return test_data

def _assert_result_shape(test_data, rows):
    """
    Make sure the row result set is correct shape (#rows, # columns
    :param col_opts:
    :param rows:    array or rows
"""

    assert test_data
    assert rows

    assert len(rows) == test_data['total_rows_exp']
    assert len(rows[0].keys()) ==  test_data['total_cols_exp']
    assert len(rows[-1].keys()) == test_data['total_cols_exp']


class Test_gen_permutations():

    def test_one_level(self, col_opts_test_data_one_level):
        test_data = col_opts_test_data_one_level
        rows = gen_permutations(test_data['col_opts'])
        _assert_result_shape(test_data, rows)

    def test_two_level(self, col_opts_test_data_two_level):
        test_data = col_opts_test_data_two_level
        rows = gen_permutations(test_data['col_opts'])
        _assert_result_shape(test_data, rows)

    def test_three_level(self, col_opts_test_data_three_level):
        test_data = col_opts_test_data_three_level
        rows = gen_permutations(test_data['col_opts'])
        _assert_result_shape(test_data, rows)

    def test_four_level(self, col_opts_test_data_four_level):
        test_data = col_opts_test_data_four_level
        rows = gen_permutations(test_data['col_opts'])
        _assert_result_shape(test_data, rows)

