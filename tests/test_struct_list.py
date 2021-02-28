"""Tests for StructList"""

import io

from jetblack_colstore.struct_list import StructList


def test_add() -> None:
    """Tests for add"""
    int_list: StructList[int] = StructList("<i", io.BytesIO(bytearray()))
    int_list.add(5)
    int_list.add(2)
    int_list.add(7)
    int_list.add(1)
    assert int_list == [1, 2, 5, 7]


def test_insert_smoke_test() -> None:
    int_list: StructList[int] = StructList("<i", io.BytesIO(bytearray()))
    int_list.insert(0, 5)
    assert int_list == [5]
    int_list.insert(0, 2)
    assert int_list == [2, 5]
    int_list.insert(2, 7)
    assert int_list == [2, 5, 7]
    int_list.insert(0, 1)
    assert int_list == [1, 2, 5, 7]


def test_insert_at_end() -> None:
    """Tests for insert"""
    int_list: StructList[int] = StructList("<i", io.BytesIO(bytearray()))
    int_list.append(1)
    int_list.insert(len(int_list), 2)
    assert int_list == [1, 2], 'insert at len(list) should append'
    int_list.insert(len(int_list)+1, 3)
    assert int_list == [1, 2, 3], 'insert after len(list) should append'


def test_len():
    """Tests for len(list)"""
    int_list: StructList[int] = StructList("<i", io.BytesIO(bytearray()))
    assert len(int_list) == 0, 'len should be 0 for empty list'
    int_list.append(1)
    assert len(int_list) == 1, 'len should be 1 after adding a single item'
    int_list.append(2)
    int_list.append(3)
    int_list.append(4)
    assert len(int_list) == 4, 'len should work after adding multiple items'
    int_list.insert(0, 0)
    assert len(int_list) == 5, 'len should work after an insert'
    del int_list[0]
    assert len(int_list) == 4, 'len should work after deleting the first item'
    del int_list[1]
    assert len(int_list) == 3, 'len should work after deleting the middle item'
    del int_list[2]
    assert len(int_list) == 2, 'len should work after deleting the last item'
    del int_list[:]
    assert len(int_list) == 0, 'len should work after deleting all items'


def test_iadd():
    """Test for +="""
    int_list: StructList[int] = StructList("<i", io.BytesIO(bytearray()))
    int_list += [0, 1, 2]
    assert int_list == [0, 1, 2], '+= should work on empty list'
    int_list += [3, 4, 5]
    assert int_list == [0, 1, 2, 3, 4, 5], '+= should work on non-empty list'


def test_append():
    """Test for append"""
    int_list: StructList[int] = StructList("<i", io.BytesIO(bytearray()))
    int_list.append(1)
    assert int_list == [1], 'should append to empty list'
    int_list.append(2)
    assert int_list == [1, 2], 'should append to non-empty list'


def test_get():
    """Test for get"""
    int_list: StructList[int] = StructList("<i", io.BytesIO(bytearray()))
    int_list += [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert int_list[0] == 0, 'should index start of list'
    assert int_list[1] == 1, 'should index forward'
    assert int_list[-1] == 9, 'should index start of list'
    assert int_list[-2] == 8, 'should index backward'
    assert int_list[:3] == [0, 1, 2], 'should slice start'
    assert int_list[7:] == [7, 8, 9], 'should slice end'
    assert int_list[3:6] == [3, 4, 5], 'should slice middle'
    assert int_list[3:-4] == [3, 4, 5], 'should slice middle from end'
    try:
        _ = int_list[len(int_list)]
        assert False, 'should raise out of range'
    except BaseException as error:  # pylint: disable=broad-except
        assert isinstance(error, IndexError), 'should raise out of range'
    assert int_list[::2] == [0, 2, 4, 6, 8], 'should step entire list'
    assert int_list[::-2] == [9, 7, 5, 3, 1], 'should step list backward'
    assert int_list[:4:2] == [0, 2], 'should step from start'
    assert int_list[5::2] == [5, 7, 9], 'should step from end'
    assert int_list[2:8:2] == [2, 4, 6], 'should step in middle'
    assert int_list[-7:-2:2] == [3, 5, 7], 'should step in middle negative'


def test_set():
    """Tests for set"""
    int_list: StructList[int] = StructList("<i", io.BytesIO(bytearray()))
    try:
        int_list[0] = 0
        assert False, 'should raise out of range'
    except BaseException as error:  # pylint: disable=broad-except
        assert isinstance(error, IndexError), 'should raise out of range'
    int_list.append(0)
    int_list[0] = -1
    assert int_list == [-1], 'should index start'
    int_list[-1] = 0
    assert int_list == [0], 'should index end'
    int_list += [1, 2, 3, 4, 5, 6, 7, 8, 9]
    int_list[:3] = [-3, -2, -1]
    assert int_list == [-3, -2, -1, 3, 4, 5, 6, 7, 8, 9], 'Should update slice'


def test_del():
    """Tests for delete"""
    int_list: StructList[int] = StructList("<i", io.BytesIO(bytearray()))
    int_list += [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    del int_list[0]
    assert int_list == [1, 2, 3, 4, 5, 6, 7, 8, 9], 'should delete first'
    del int_list[-1]
    assert int_list == [1, 2, 3, 4, 5, 6, 7, 8], 'should delete last'
    del int_list[4]
    assert int_list == [1, 2, 3, 4, 6, 7, 8], 'should delete middle'
    del int_list[:]
    assert int_list == [], 'should delete all'
    int_list += [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    del int_list[::2]
    assert int_list == [1, 3, 5, 7, 9], 'should delete positive step'
    del int_list[:]
    int_list += [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    del int_list[::-2]
    assert int_list == [0, 2, 4, 6, 8], 'should delete negative step'
