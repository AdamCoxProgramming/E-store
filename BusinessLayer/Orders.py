from Datastore import AccessLayer
from BusinessLayer import Products
from BusinessLayer import Seller
from BusinessLayer import Customer

class OrderedItem:
    """This class represents an item that has been ordered by a customer, this object will be used before after an order has been made"""
    def __init__(self,productStock):
        self.productStock = productStock
        self.state = "Awaiting Shipment"
        self.storeOrderId = -1#Gets added during checkout
        self.deliveryOption = -1 #Gets set by user during checkout
        self.id = -1#Gets added during checkout

    def setDeliveryOption(self,option):
        """Sets the delivery option for thi item
        pre-condition:This should be called before an order has been made, so the delivery option can be stored in the system
        post-condition:This option is stored as part of the objects state and when this ordered item is saved to the system this delivery option will be also"""
        self.deliveryOption = option

    def setShipped(self):
        """Updates the orders, noting that the product has been shipped to the customer
        pre-condition:The ordered item should have been stored in the system
        post-condition:The product stock associated with this product will have its quantity reduced by one and this ordered item will have the state 'Shipped'"""
        self.state = "Shipped"
        self.productStock.notifyItemsShipped(1)
        AccessLayer.setOrderedItemShipped(self.id)

class OrderedItems:
    """A factory for creating and returning Ordered Items objects for Ordered Items stored in the system"""

    def addItem(self,orderedItem,storeOrderId):
        """Adds a new ordered item to the system
        pre-condition:The ordered item as well as the store order id it is part of should be passed in as arguments
        post-condition:The ordered item is stored in the system"""
        AccessLayer.addOrderedItem(orderedItem.productStock.id,"Awaiting Shipment", orderedItem.deliveryOption.id,storeOrderId)

    def getOrderedItemForStoreOrder(self,storeOrderId):
        """Returns all the ordered items for a particular store order
        pre-condition:The id of the store order needs to be passed as an arguments
        post-condition:A list of the store orders for a specific order is returned"""
        itemsArr = AccessLayer.getOrderedItemForStoreOrder(storeOrderId)
        orderedItems = []
        for arr in itemsArr:
            productStockId = arr[0]
            productStock = Products.ProductStocks().getProductStock(productStockId)
            orderdItem = OrderedItem(productStock)
            orderdItem.state = arr[1]
            orderdItem.deliveryOption = Seller.DeliveryOptions().getDeliveryOption(arr[2],arr[4])
            orderedItems.append(orderdItem)
        return orderedItems

class StoreOrders:
    """A factory for creating and returning Store Order objects for Store Order stored in the system"""

    def addStoreOrder(self,orderDescription):
        """Adds a new store order to the system
        pre-condition:The description of the order must be passed as an argument
        post-condition:The store order is added to the system and the id of the stored store order is returned"""
        storeOrderId = AccessLayer.addStoreOrder(orderDescription.customer.customerId, orderDescription.deliveryAddress)
        for orderedItem in orderDescription.orderedItems:
            AccessLayer.addOrderedItem(orderedItem.productStock.id,"Awaiting Shipment",
                                       orderedItem.deliveryOption.id,storeOrderId,orderedItem.productStock.sellerId)
        return storeOrderId

    def getOrdersForCustomer(self,customerId):
        """Returns all the store orders for a particular customer
        pre-condition:The id of the customer needs to be passed as an argument
        post-condition:A list of the store orders for a specific customer is returned"""
        ordersArr = AccessLayer.getOrdersForCustomer(customerId)
        orders = []
        customer = Customer.Customers().getCustomerById(customerId)
        for orderArr in ordersArr:
            orders.append(self.orderArrToStoreOrder(orderArr,customer))

        return orders

    def orderArrToStoreOrder(self,orderArr,customer):
        """Converts the array returned by the data access layer into a StoreOrder object
        pre-condition:The array returned from the access layer and the associated customer object must be provided
        post-condition:A StoreOrder object with the appropriate details is returned"""
        return StoreOrder(orderArr[2],customer,orderArr[0],orderArr[1])

    def getOrder(self,storeOrderId):
        """Fetches a specific store order from the system
        pre-condition:The id of the StoreOrder to fetch must be supplied
        post-condition:A StoreOrder object with the appropriate details is returned"""
        orderArr = AccessLayer.getOrder(storeOrderId)
        if len(orderArr) == 0:
            return None
        customer = Customer.Customers().getCustomerById(orderArr[3])
        return self.orderArrToStoreOrder(orderArr,customer)

class StoreOrder:
    """The StoreOrder object represents a whole order made by a customer, one store order has many OrderedItems"""
    def __init__(self, storeOrderId, customer, datetime, deliveryAddress):
        self.customer = customer
        self.datetime = datetime
        self.deliveryAddress = deliveryAddress
        self.storeOrderId = storeOrderId

    def getOrderedItems(self):
        """Returns the Ordered Items associated with this specific store order
        pre-condition:None
        post-condition:All the Ordered Items are returned in a list"""
        return StoreOrder.itemArrToItems(AccessLayer.getOrderedItemsForStoreOrder(self.storeOrderId))

    def itemArrToItems(itemArr):
        """Converts the array returned by the data access layer an array of StoreOrder objects
        pre-condition:The array returned from the access layer must be provided
        post-condition:A list of StoreOrder objects with the appropriate details is returned"""
        #supply_id, state, delivery_option_id, store_order_id, seller_id
        res = []
        for arr in itemArr:
            supply = Products.ProductStocks().getProductStock(arr[0])
            orderItem = OrderedItem(supply)
            orderItem.state = arr[1]
            orderItem.storeOrderId = arr[3]
            orderItem.id = arr[5]
            orderItem.deliveryOption = Seller.DeliveryOptions().getDeliveryOption(arr[2],arr[4])
            res.append(orderItem)
        return res

    def __str__(self):
        """Formats a string that represents the contents of this object"""
        res = "order ID: " + str(self.storeOrderId) + ", items: { "
        for orderedItem in self.getOrderedItems():
            productId = orderedItem.productStock.productId
            productName = Products.ProductListings().searchFromProductById(productId).name
            res += productName + " , " + "status: " + orderedItem.state + " | "

        return res[0:-3] + " }"

class DevilveryOptionNotSetExeption(Exception):
    """A special exception that helps debug if a delivery option has not been set"""
    pass

class StoreOrderDescription:
    """This class represents a StoreOrder before it has been 'paid for' and added to the system.
    This class is used to build up a store order description before adding it to the system.
    Once added to the system a StoreOrder item will be available with the details specified in this description"""
    def __init__(self, productStocks, customer, datetime):
        self.orderedItems = []
        for productStock in productStocks:
            self.orderedItems.append(OrderedItem(productStock))
        self.customer = customer
        self.datetime = datetime
        self.deliveryAddress = -1 #Gets added during payment

    def getOrderedItems(self):
        """Returns the Ordered Items associated with this store order description
        pre-condition:None
        post-condition:All the Ordered Items are returned in a list"""
        return self.orderedItems

    def getTotalPrice(self):
        """Calculates the total price of all the items for the StoreOrderDescription (including the price of delivery options)
        pre-condition:None
        post-condition:If any of the items have not got a delivery option set, then an exception is thrown.
        other wise the total price of the order (before any promotions) is returned"""
        totalPrice = 0
        for orderedItem in self.orderedItems:
            totalPrice += orderedItem.productStock.price
            if orderedItem.deliveryOption == -1:
                raise DevilveryOptionNotSetExeption()
            totalPrice += + orderedItem.deliveryOption.price
        return totalPrice

    def __str__(self):
        """Formats a string that represents the contents of this object"""
        res = "order ID: " + str(self.storeOrderId) + ", items: { "
        for orderedItem in self.orderedItems:
            res += str(orderedItem.productStock) + " , " + "status: " + orderedItem.state + " | "

        return res[0:-3] + " }"

class SellerOrder:
    """This class represents an order that has been placed with a specific seller.
    This class features the details necessary for the seller to know"""
    def __init__(self,storeOrderId,orderedItem,customer,datetime):
        self.orderedItem = orderedItem
        self.customer = customer
        self.datetime = datetime
        self.storeOrderId = storeOrderId

    def __str__(self):
        """Formats a string that represents the contents of this object"""
        return str(self.orderedItem.productStock) + ", Customer name: " + self.customer.name

    def notifyAsShipped(self):
        """This function notifies the system that the seller has shipped this seller order
        pre-condition:The order should not have been shipped yet
        post-condition:The state of the OrderedItem is updated"""
        self.orderedItem.setShipped()