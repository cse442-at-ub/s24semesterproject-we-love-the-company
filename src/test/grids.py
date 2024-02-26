import unittest

import os
import sys

# python is such a well designed language
sys.path.append(os.getcwd() + "/src/game")

from grid import Grid

class GridTests(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(10,5)
    
    def assertListEqualIgnoringOrder(self,listA:list,listB:list):
        self.assertEqual(len(listA),len(listB))
        for itemA in listA:
            self.assertIn(itemA,listB)
        for itemB in listB:
            self.assertIn(itemB,listA)
    
    def test_inbounds(self):
        for x in range(-5,15):
            for y in range(-5,15):
                if x < 0 or x > 9 or y < 0 or y > 4:
                    self.assertFalse(self.grid.is_inbounds(x,y))
                else:
                    self.assertTrue(self.grid.is_inbounds(x,y))
    
    def test_insert_object(self):
        # place object on the grid and try to place something on top of it
        self.assertTrue(self.grid.insert({"name":"test object"},3,3))
        self.assertFalse(self.grid.insert({"name":"test object"},3,3))
    
    def test_insert_badly(self):
        # try to insert empty space
        with self.assertRaises(ValueError):
            self.grid.insert({},2,2)
        
        # try to insert out of bounds
        with self.assertRaises(ValueError):
            self.grid.insert({"name":"test object"},99,99)
    
    def test_retrieve_object(self):
        #place an object on the grid and retrieve it
        self.assertTrue(self.grid.insert({"name":"test object"},3,3))
        self.assertDictEqual({"name":"test object"},self.grid.get_object(3,3))
    
    def test_retrieve_nothing(self):
        self.assertIsNone(self.grid.get_object(3,3))
    
    def test_remove_object_at_location(self):
        # remove object while nothing is there should return none
        self.assertIsNone(self.grid.remove_at_location(3,3))

        # place object and remove it, should return the object
        self.assertTrue(self.grid.insert({"name":"test object"},3,3))
        self.assertDictEqual(self.grid.remove_at_location(3,3),{"name":"test object"})

        # attempt to remove after space is empty, should return none again
        self.assertIsNone(self.grid.remove_at_location(3,3))
    
    def test_remove_object_badly(self):
        # place an object
        self.assertTrue(self.grid.insert({"name":"test object"},3,3))

        # try to remove something out of bounds
        with self.assertRaises(ValueError):
            self.grid.remove_at_location(99,99)
    
    def test_find_precise(self):
        # place complex objects on the grid
        self.assertTrue(self.grid.insert({"name":"test object","hp": 3,"shoes":None},3,3))
        self.assertTrue(self.grid.insert({"name":"example object","hp": 3,"shoes":None},4,4))
        self.assertTrue(self.grid.insert({"name":"test object","hp": 2,"shoes":"Big"},2,2))

        # find only the one called 'test object' with 3 HP
        self.assertSetEqual( self.grid.find_object_with_properties({"name":"test object","hp":3},False) , {(3,3)} )

        # find all objects with the name 'test object'
        self.assertSetEqual( self.grid.find_object_with_properties({"name":"test object"},False) , {(3,3),(2,2)} )

    def test_find_loose(self):
        # place complex objects on the grid
        self.assertTrue(self.grid.insert({"name":"test object","hp": 3,"shoes":None},3,3))
        self.assertTrue(self.grid.insert({"name":"example object","hp": 3,"shoes":None},4,4))
        self.assertTrue(self.grid.insert({"name":"test object","hp": 2,"shoes":"Big"},2,2))

        # find any object with 'Big' shoes OR the name 'example object'
        self.assertSetEqual( self.grid.find_object_with_properties({"name":"example object","shoes":"Big"},True) , {(4,4),(2,2)} )

    def test_remove_single_precise(self):
        # place complex objects on the grid
        self.assertTrue(self.grid.insert({"name":"test object","hp": 3,"shoes":None},3,3))
        self.assertTrue(self.grid.insert({"name":"example object","hp": 3,"shoes":None},4,4))
        self.assertTrue(self.grid.insert({"name":"test object","hp": 2,"shoes":"Big"},2,2))

        # find only the one called 'test object' with 3 HP
        self.assertListEqualIgnoringOrder(self.grid.remove_all_with_properties({"name":"test object","hp":3},False),[{"name":"test object","hp": 3,"shoes":None}])

        # ensure the space is newly empty
        self.assertIsNone(self.grid.get_object(3,3))

    def test_remove_several_precise(self):
        # place complex objects on the grid
        self.assertTrue(self.grid.insert({"name":"test object","hp": 3,"shoes":None},3,3))
        self.assertTrue(self.grid.insert({"name":"example object","hp": 3,"shoes":None},4,4))
        self.assertTrue(self.grid.insert({"name":"test object","hp": 2,"shoes":"Big"},2,2))

        # find all objects with the name 'test object'
        self.assertListEqualIgnoringOrder(self.grid.remove_all_with_properties({"name":"test object"},False),[{"name":"test object","hp": 3,"shoes":None},{"name":"test object","hp": 2,"shoes":"Big"}])

        # ensure the space is newly empty
        self.assertIsNone(self.grid.get_object(3,3))
        self.assertIsNone(self.grid.get_object(2,2))

    def test_remove_several_loose(self):
        # place complex objects on the grid
        self.assertTrue(self.grid.insert({"name":"test object","hp": 3,"shoes":None},3,3))
        self.assertTrue(self.grid.insert({"name":"example object","hp": 3,"shoes":None},4,4))
        self.assertTrue(self.grid.insert({"name":"test object","hp": 2,"shoes":"Big"},2,2))

        # find any object with 'Big' shoes OR the name 'example object'
        self.assertListEqualIgnoringOrder( self.grid.remove_all_with_properties({"name":"example object","shoes":"Big"},True) , [{"name":"example object","hp": 3,"shoes":None},{"name":"test object","hp": 2,"shoes":"Big"}] )

        # ensure the space is newly empty
        self.assertIsNone(self.grid.get_object(4,4))
        self.assertIsNone(self.grid.get_object(2,2))