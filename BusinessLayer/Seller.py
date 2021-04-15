from BusinessLayer.Products import ProductStocks
from Datastore.AccessLayer import addSeller, getSellerId, getSeller, getDeliveryOptionsForSeller, addDeliveryOption, getDeliveryOptionsForSeller, getOrderdItemsForSeller
import BusinessLayer.Orders as Orders

class Seller:
    """This class represents a seller in the system"""
    def __init__(self, name):
        self._name = name
        self.id = -1  # the id is populated when the seller is added to the seller list
        self.orders = []

    def getName(self):
        """returns the name of the seller"""
        return self._name

    def getSellerOrdersLeftToShip(self):
        """Returns a list of orders that the seller has yet to ship
        pre-condition:The seller must have been stored in the system using the Sellers class before calling this function
        post-condition:A list of SellerOrders is returned"""
        itemsArr = getOrderdItemsForSeller(self.id)
        orderedItems = Orders.StoreOrder.itemArrToItems(itemsArr)
        orders = []
        for orderedItem in orderedItems:
            orders.append(self.createSellerOrder(orderedItem))
        return orders

    def createSellerOrder(self,orderedItem):
        """A private helper function to assemble a SellerOrder
        pre-condition:The ordered item for which the SellerOrder corresponds to must be passed as an argument
        post-condition:A SellerOrder is created and returned"""
        storeOrder = Orders.StoreOrders().getOrder(orderedItem.storeOrderId)
        return Orders.SellerOrder(orderedItem.storeOrderId,orderedItem,storeOrder.customer,storeOrder.datetime)

    def getCatalog(self):
        """Returns a list of all the products stocks that the seller has
        pre-condition:The seller must have been stored in the system using the Sellers class before calling this function
        post-condition:A list of ProductStocks corresponding to this seller is returned"""
        return ProductStocks().searchForSellerStocks(self.id)

    def addProductSupplyToCatalog(self, productSupply):
        """This function adds a new product supply to the sellers catalog
        pre-condition:The seller must have been stored in the system using the Sellers class before calling this function
        The product stock that the seller will now stock should be passed as an argument
        post-condition:The product stock is added to the sellers catalog"""
        stocks = ProductStocks()
        stocks.addProductSupply(productSupply)

    def payForItemSale(self,amount):
        """Pay the seller for the sale of one of their items"""
        pass

    def getDeliveryOptions(self):
        """This function returns all the delivery options a seller provides
        pre-condition:The seller must have been stored in the system using the Sellers class before calling this function
        post-condition:A list of delivery options provided by the seller is returned"""
        return DeliveryOptions().getOptionsForSeller(self.id)

    def addDeliveryOption(self,deliveryOption):
        """This function adds a new delivery option to the options a seller provides
        pre-condition:The seller must have been stored in the system using the Sellers class before calling this function
        The delivery option to add should be passed as an argument
        post-condition:The option is stored as a new option"""
        DeliveryOptions().addDeliveryOption(deliveryOption)

class DeliveryOption:
    """This class represents a delivery option that seller provides"""
    def __init__(self,name,price,sellerId):
        self.name = name
        self.price = price
        self.sellerId = sellerId
        self.id = -1#The id gets set when addedd to delivery options list

class DeliveryOptions:
    """A factory for creating and returning DeliveryOption objects for DeliveryOptions stored in the system"""
    def __init__(self):
        """Here the default delivery option is specified"""
        self.defaultOption = DeliveryOption("Standard",0,-1)

    def addDeliveryOption(self, option):
        """Adds a new delivery option to the system
        pre-condition:A delivery option object should be supplied as an argument
        post-condition:The delivery options is stored in the system"""
        addDeliveryOption(option.price,option.sellerId,option.name)

    def getDeliveryOption(self,id,sellerId):
        """Returns a specific delivery option
        pre-condition:The id of the delivery option as well as the sellers id should be provided
        post-condition:The corresponding delivery options is returned, if the id is -1, the default options is returned"""
        if id == -1:
            return self.createDefaultDeliveryOption(sellerId)
        else:
            sellerOptions = getDeliveryOptionsForSeller(sellerId)
            for option in sellerOptions:
                if option.id == id:
                    return option

    def getOptionsForSeller(self,sellerId):
        """Returns all the delivery options that a seller provides
        pre-condition:The id of the seller must be provided, the id should match a 'real' seller
        post-condition:A list of delivery options is returned"""
        optionsArr = getDeliveryOptionsForSeller(sellerId)
        sellerOptions = []
        for arr in optionsArr:
            sellerOptions.append(DeliveryOption(arr[1],arr[0],sellerId))

        sellerOptions.append(self.createDefaultDeliveryOption(sellerId))
        return sellerOptions

    def createDefaultDeliveryOption(self,sellerId):
        """Returns all the delivery options that a seller provides
        pre-condition:The id of the seller must be provided, the id should match a 'real' seller
        post-condition:A list of delivery options is returned"""
        return DeliveryOption(self.defaultOption.name, self.defaultOption.price, sellerId)

class Sellers:
    """A factory for creating and returning Seller objects for Sellers stored in the system"""
    def addVendor(self, vendor):
        """Adds a new Seller to the system
        pre-condition:A Seller object should be supplied as an argument
        post-condition:The Seller is stored in the system, the seller object provided has its id updated"""
        vendor.id = addSeller(vendor.getName())

    def searchVendorByName(self, name):
        """Returns a specific seller based on its name
        pre-condition:The name of the Seller should be supplied as an argument (string)
        post-condition:If the Seller exists a corresponding seller object is returned, otherwise a None object is returned"""
        id = getSellerId(name)
        if id == None:
            return None
        seller = Seller(name)
        seller.id = id
        return seller

    def searchVendorById(self, id):
        """Returns a specific seller based on its name
        pre-condition:The id of the Seller should be supplied as an argument (string)
        post-condition:If the Seller exists a corresponding seller object is returned, otherwise a None object is returned"""
        name = getSeller(id)
        if name == None:
            return None
        seller = Seller(name)
        seller.id = id
        return seller