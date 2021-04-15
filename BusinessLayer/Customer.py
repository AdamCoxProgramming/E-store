from BusinessLayer import Basket 
from Datastore import AccessLayer
from BusinessLayer import Orders 

class Customer:
    """This class represents a customer in the system"""
    def __init__(self,name):
        self.name = name
        self.storedPaymentMethod = None
        self.customerId = -1 # Gets added when the customer is stored in the CustomerList
        self.basket = Basket.Basket(self)

    def getOrders(self):
        """Gets the orders associated with the customer
        pre-condition:The customer must have been stored using the Customers class before this can function can be called
        post-condition:All the orders associated with this customer are returned"""
        return Orders.StoreOrders().getOrdersForCustomer(self.customerId)

class Customers:
    """A factory for creating and returning customer objects for customers stored in the system"""
    def addCustomer(self,customer):
        """Adds a new customer to the system
        pre-condition:A customer object should be supplied as an argument, the customer should have a unique name
        post-condition:The customer is stored in the system"""
        if self.getCustomerByName(customer.name) != None:
            raise ValueError()

        customer.customerId = AccessLayer.addCustomer(customer)
        return customer.customerId

    def getCustomerByName(self,name):
        """Fetches a customer based on the customer name
        pre-condition:The name of the customer (string) to fetch should be passed as an argument
        post-condition:If a customer with that name exists they will be returned, otherwise a None object will be"""
        id = AccessLayer.getCustomerId(name)
        if id == None:
            return None
        return self._createCustomerObject(id, name)

    def _createCustomerObject(self, id, name):
        """creates a customer object with the id and name provided, this is a 'private' method
        pre-condition:The name of the customer (string) and id (integer) should be provided as arguments
        post-condition:A customer object will be returned"""
        customer = Customer(name)
        customer.customerId = id
        return customer

    def getCustomerById(self,id):
        """Fetches a customer based on the customer id
        pre-condition:The id of the customer (integer) to fetch should be passed as an argument
        post-condition:If a customer with that id exists they will be returned, otherwise a None object will be"""
        name = AccessLayer.getCustomerName(id)
        if name == None:
            return None
        return self._createCustomerObject(id, name)
