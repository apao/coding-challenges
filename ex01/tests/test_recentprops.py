"""Test suite for recentprops.py"""

from ex01 import recentprops
from random import randint
import pytest


class TestRecentProperties(object):
    """Tests for RecentProperties class."""

    def setup_method(self, method):
        """ setup_method is invoked for every test method of a class.
        """

        self.recent_properties_obj = recentprops.RecentProperties()

    def test__init__(self):
        assert type(self.recent_properties_obj.pq) is list
        assert self.recent_properties_obj.counter == 0
        assert type(self.recent_properties_obj.id_finder) is dict
        assert self.recent_properties_obj.max_size == recentprops.DEFAULT_MAX_SIZE

    def test_add_less_than_size_not_in_finder(self):
        # CONDITION 1 of 4: CURRENT SIZE < MAX SIZE AND PROPERTY_ID NOT IN FINDER
        assert not self.recent_properties_obj.id_finder
        self.recent_properties_obj.add_property(1)
        assert self.recent_properties_obj.id_finder

    def test_add_less_than_size_in_finder(self):
        # CONDITION 2 of 4: CURRENT SIZE < MAX SIZE AND PROPERTY_ID IN FINDER
        list_of_ids = [1, 10, 421, 67]

        for property_id in list_of_ids:
            self.recent_properties_obj.add_property(property_id)

        assert len(self.recent_properties_obj.id_finder) == 4
        assert self.recent_properties_obj.id_finder.get(1).count == 1

        # WHEN AN ID IS IN THE FINDER, COUNT OF THAT ID SHOULD BE UPDATED,
        # AND THE NUMBER OF ITEMS IN THE FINDER SHOULD REMAIN THE SAME AS BEFORE.
        assert self.recent_properties_obj.id_finder.get(10).count == 2
        self.recent_properties_obj.add_property(10)
        assert self.recent_properties_obj.id_finder.get(10).count == 5
        assert len(self.recent_properties_obj.id_finder) == 4

    def test_add_max_size_in_finder(self):
        # CONDITION 3 of 4: CURRENT SIZE == MAX SIZE AND PROPERTY_ID IN FINDER

        for count in range(1, recentprops.DEFAULT_MAX_SIZE + 1):
            self.recent_properties_obj.add_property(count)

        assert len(self.recent_properties_obj.id_finder) == recentprops.DEFAULT_MAX_SIZE

        # WHEN AN ID IS IN THE FINDER, COUNT OF THAT ID SHOULD BE UPDATED.
        assert self.recent_properties_obj.id_finder.get(1).count == 1
        self.recent_properties_obj.add_property(1)
        assert self.recent_properties_obj.id_finder.get(1).count == 101
        assert len(self.recent_properties_obj.id_finder) == recentprops.DEFAULT_MAX_SIZE

        assert len(self.recent_properties_obj.pq) == recentprops.DEFAULT_MAX_SIZE
        assert self.recent_properties_obj.pq[0]

        # WHEN AN ID'S COUNT HAS BEEN UPDATED, IT WILL NO LONGER BE THE OLDEST VIEWED ID.
        test_removal = self.recent_properties_obj._pop_property()
        assert test_removal.prop_id == 2
        assert len(self.recent_properties_obj.pq) == recentprops.DEFAULT_MAX_SIZE - 1

    def test_add_max_size_not_in_finder(self):
        # CONDITION 4 of 4: CURRENT SIZE == MAX SIZE AND PROPERTY_ID NOT IN FINDER
        for count in range(1, 101):
            self.recent_properties_obj.add_property(count)

        assert len(self.recent_properties_obj.id_finder) == recentprops.DEFAULT_MAX_SIZE

        assert 1 in self.recent_properties_obj.id_finder
        self.recent_properties_obj.add_property(101)
        assert 1 not in self.recent_properties_obj.id_finder
        assert 101 in self.recent_properties_obj.id_finder
        assert len(self.recent_properties_obj.id_finder) == recentprops.DEFAULT_MAX_SIZE

    def test_add_same_id_more_than_max_size_times(self):

        for count in range(200):
            self.recent_properties_obj.add_property(1)

        assert 1 in self.recent_properties_obj.id_finder
        assert len(self.recent_properties_obj.id_finder) == 1
        assert len(self.recent_properties_obj.pq) == 1

    def test_add_None_id(self):

        with pytest.raises(TypeError):
            self.recent_properties_obj.add_property(None)

    def test_add_hello_id(self):

        with pytest.raises(ValueError):
            self.recent_properties_obj.add_property("hello")

    def test_pop_property(self):
        list_of_ids = [1, 10, 421, 67]

        for property_id in list_of_ids:
            self.recent_properties_obj.add_property(property_id)

        for idx in range(len(list_of_ids)):
            test_removal = self.recent_properties_obj._pop_property()
            assert test_removal.prop_id == list_of_ids[idx]
            assert test_removal.count == idx + 1  # COUNT STARTS WITH 1, NOT 0

        assert not self.recent_properties_obj.pq

    def test_most_recent_less_than_max_size(self):
        list_of_ids = [1, 10, 421, 67]

        for property_id in list_of_ids:
            self.recent_properties_obj.add_property(property_id)

        assert set(list_of_ids) == set(self.recent_properties_obj.most_recent())
        assert len(self.recent_properties_obj.most_recent()) == 4

        for property_id in list_of_ids:
            self.recent_properties_obj.add_property(property_id)

        assert set(list_of_ids) == set(self.recent_properties_obj.most_recent())
        assert len(self.recent_properties_obj.most_recent()) == 4

    def test_most_recent_equal_to_max_size(self):

        for count in range(1, recentprops.DEFAULT_MAX_SIZE + 1):
            self.recent_properties_obj.add_property(count)

        assert set(range(1, recentprops.DEFAULT_MAX_SIZE + 1)) == set(self.recent_properties_obj.most_recent())
        assert len(self.recent_properties_obj.most_recent()) == recentprops.DEFAULT_MAX_SIZE

    def test_most_recent_one_more_than_max_size(self):

        for count in range(1, recentprops.DEFAULT_MAX_SIZE + 2):
            self.recent_properties_obj.add_property(count)

        assert set(range(2, recentprops.DEFAULT_MAX_SIZE + 2)) == set(self.recent_properties_obj.most_recent())
        assert len(self.recent_properties_obj.most_recent()) == recentprops.DEFAULT_MAX_SIZE

    def test_most_recent_repeated_props_greater_than_max_size(self):

        for count in range(200):
            random_id = randint(1, 10)
            self.recent_properties_obj.add_property(random_id)

        assert len(self.recent_properties_obj.most_recent()) <= 10


class TestPropertyDetails(object):
    """Tests for PropertyDetails class."""

    def setup_method(self, method):
        """ setup_method is invoked for every test method of a class.
        """

        self.prop_details_obj1 = recentprops.PropertyDetails(1, 1)
        self.prop_details_obj2 = recentprops.PropertyDetails(2, 2)
        self.prop_details_obj_default = recentprops.PropertyDetails()

    def test__init__(self):
        assert type(self.prop_details_obj1.prop_id) is int
        assert self.prop_details_obj1.prop_id == 1
        assert self.prop_details_obj1.count == 1

    def test__lt__(self):
        assert self.prop_details_obj1 < self.prop_details_obj2
        assert self.prop_details_obj_default < self.prop_details_obj1
        assert self.prop_details_obj_default < self.prop_details_obj2
        # assert self.prop_details_obj1 > self.prop_details_obj_default
        # assert self.prop_details_obj1 == self.prop_details_obj1

    def test_update_count(self):
        self.prop_details_obj1.update_count(5)
        assert self.prop_details_obj1.count == 5


