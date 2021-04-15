from Interface.CustomerInterface import startProgram
from BusinessLayer.Customer import Customers
from BusinessLayer.Products import ProductListings
from BusinessLayer.Seller import Sellers
from unittest import mock
from unittest import TestCase
from .TestCase import TestConnection
import unittest
from contextlib import contextmanager
import sys, os

commands = ["admin",
"manage listings",
"add",
"Xbox",
"Xbox,xbox,games",
"back",
"back",
"seller",
"n",
"Microsoft",
"manage products",
"add to catalog",
"Xbox",
"299",
"100",
"back",
"delivery options",
"add",
"Fast",
"5",
"back",
"customer",
"n",
"Adam",
"search products",
"Xbox",
"view Xbox",
"order from Microsoft",
"back",
"open basket",
"checkout",
"33 Hilltop Rd",
"Fast",
"n",
"credit",
"n"]

backs = ['back','back','back','back','back','back','back','back','back','back','back','back','back','back']

"""This print suppression code is based of an answer from https://thesmithfam.org/blog/2012/10/25/temporarily-suppress-console-output-in-python/"""
@contextmanager
def suppress_print():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

class InterfaceTestCase(TestCase):
    @mock.patch('builtins.input', create=True)
    def testInterface(self, mocked_input):
        TestConnection().resetDatabase()
        mocked_input.side_effect = commands + backs
        with suppress_print():
            runInterfaceCommands()

        assertSystemState()

        self.assertEqual(1, 1)

def runInterfaceCommands():
    startProgram(True)

def assertSystemState():
    customer = Customers().getCustomerByName("Adam")
    storeOrder = customer.getOrders()[0]
    orderedItem = storeOrder.getOrderedItems()[0]
    xboxProductListing = ProductListings().searchForProducts(["Xbox"])[0]
    if orderedItem.productStock.productId != xboxProductListing.id:
        print("Customer has ordered item: False")
    else:
        print("Customer has ordered item: True")

    seller = Sellers().searchVendorByName("Microsoft")
    sellerOrder = seller.getSellerOrdersLeftToShip()[0]

    if sellerOrder.orderedItem.productStock.productId != xboxProductListing.id:
        print("Seller has received an order: False")
    else:
        print("Seller has received an order: True")

if __name__ == '__main__':
    unittest.main()