"""Tests for helper functions"""

import os
import os.path
import tempfile

from jetblack_colstore.helpers import open_column_store
from jetblack_colstore.list_types import IntList


def test_open_column_store():
    """Test open_column_store"""
    with tempfile.TemporaryDirectory() as folder_name:
        filenames = [
            os.path.join(folder_name, filename)
            for filename in ("one.bin", "two.bin", "three.bin")
        ]
        struct_list_factories = (IntList, IntList, IntList)

        store = open_column_store(filenames, struct_list_factories)

        store.append(1, 10, 100)
        store.append(2, 20, 200)
        store.append(3, 30, 300)

        assert store[0] == (1, 10, 100)
        assert store[1] == (2, 20, 200)
        assert store[2] == (3, 30, 300)

        store.close()

        store = open_column_store(filenames, struct_list_factories)

        assert store[0] == (1, 10, 100)
        assert store[1] == (2, 20, 200)
        assert store[2] == (3, 30, 300)

        store.close()
