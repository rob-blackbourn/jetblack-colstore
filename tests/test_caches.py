"""Tests for caches"""

from jetblack_colstore.caches import LRUCache


def test_lru_cache():
    """Test for LRUCache"""
    cache: LRUCache[int, str] = LRUCache(5)

    for i, pair in enumerate([(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five')]):
        key, value = cache.set(*pair)
        assert key is None and value is None, 'should not evict'
        assert len(cache) == i + 1, 'should grow cache'
    # keys: 5,4,3,2,1

    key, value = cache.set(6, 'six')
    assert key == 1 and value == 'one', 'should evict oldest'
    assert len(cache) == 5, 'should not grow cache'
    # keys: 6,5,4,3,2

    key, value = cache.set(2, 'two')
    assert key is None and value is None, 'should not evict already present'
    assert len(cache) == 5, 'should not grow cache'
    # keys: 2,6,5,4,3

    key, value = cache.set(7, 'seven')
    assert key == 3 and value == 'three', 'should evict oldest'
    assert len(cache) == 5, 'should not grow cache'
    # keys: 7,2,6,5,4

    items = cache.clear()
    assert items == [
        (2, 'two'),
        (4, 'four'),
        (5, 'five'),
        (6, 'six'),
        (7, 'seven'),
    ], 'should return cache content'
    assert len(cache) == 0, 'cache should be empty'
