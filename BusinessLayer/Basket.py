import abc
from datetime import datetime
from BusinessLayer.Seller import Seller, Sellers
from BusinessLayer.Orders import StoreOrderDescription, OrderedItem, SellerOrder, StoreOrders
from Datastore.AccessLayer import addBasketItem, getBasketItems, clearBasket
from BusinessLayer.Products import ProductStocks

class Basket:
    """This class represents a customers basket"""
    def __init__(self,customer):
        """Creates a new basket
        pre-condition: the customer for whom this basket belongs to must be passed as an argument
        post-condition: stores a reference to the customer"""
        self._customer = customer

    def addItem(self,productSupply):
        """Adds a product supply to the users basker
        pre-condition: takes a product supply object as an input
        post-condition: the datalayer stores the supply in the customers basket"""
        addBasketItem(self._customer.customerId,productSupply.id)

    def getItems(self):
        """Returns all the ProductStocks currently in the users basket"""
        basketRows = getBasketItems(self._customer.customerId)
        supplys = []
        for row in basketRows:
            supplys.append(ProductStocks().getProductStock(row[1]))
        return supplys

    def createOrderDescription(self):
        """Creates an order description from the items currently in a users basket
        pre-condition:None
        post-condition:returns a StoreOrderDescription object with information about the baskets items"""
        return StoreOrderDescription(self.getItems(), self._customer, datetime.now())

    def clearBasket(self):
        """Removes all items from the users basket
        pre-condition:None
        post-condition:Commands the datalayer to remove all items from the users basket"""
        clearBasket(self._customer.customerId)

class Payment:
    """This class is used to handle the payment process"""
    def __init__(self):
        self.promoModifier = None

    def applyDiscount(self,promoModifier):
        """This adds a promotion to the payment which will alter the price
        pre-condition:This function takes a promotion modifier as an argument. This function should be called before payForOrder
        post-condition:The modifier is stored as part of the objects state and will be used during the payForOrder function call"""
        self.promoModifier = promoModifier

    def calculatePriceAfterPromo(self,order):
        """This function calculatest the price of the order description passsed in taking into account if a promo is applied
        pre-condition:An order description should be passed in
        post-condition:Returns the price of the order taking into account a optional promotion"""
        amountToCharge = order.getTotalPrice()
        if self.promoModifier != None:
            amountToCharge = self.promoModifier.applyPromotion(amountToCharge)
        return amountToCharge

    def payForOrder(self, orderDescription, paymentMethod, devliverAddress):
        """This function confirms an order in the system
        pre-condition:An order description is passed in along with payment method and an address
        post-condition:The customer is charged, the sellers are payed, the orders are stored in the system and added to the sellers order list"""
        orderDescription.deliveryAddress = devliverAddress

        amountToCharge = self.calculatePriceAfterPromo(orderDescription)
        paymentMethod.chargeCustomer(amountToCharge)

        storeOrders = StoreOrders()
        storeOrderId = storeOrders.addStoreOrder(orderDescription)
        self.payForVendorsOrders(orderDescription)

    def payForVendorsOrders(self, storeOrderDescription):
        """This function pays the required sellers for orders
        pre-condition:The store order description should be passed in as an argument
        post-condition:Payments are made to the relevant sellers accounts"""
        for orderdItem in storeOrderDescription.getOrderedItems():
            sellers = Sellers()
            vendor = sellers.searchVendorById(orderdItem.productStock.sellerId)
            vendor.payForItemSale(orderdItem.productStock.price)

class PromoCodes:
    """This class stores the available promotion codes in tempory memory (due to time constraints)"""
    codes = {}

    def addPromo(self,code,modifier):
        """Stores a new promotion modifier at the code value
        pre-condition:A code (string or integer) and modifier are required as arguments
        post-condition:The modifier is stored in the dictionary with the key being the code passed in"""
        PromoCodes.codes[code] = modifier

    def removePromo(self,code):
        """Removes the promotion modifier with the code passed as the argument
        pre-condition:The code of the modifier to remove should be passed as an argument
        post-condition:The matching promotion modifier is removed"""
        del PromoCodes.codes[code]

    def getPromotion(self,code):
        """Returns the promotion modifier for the code
        pre-condition:The code of the modifier to fetch should be passed as an argument
        post-condition:The matching promotion modifier is fetched"""
        return PromoCodes.codes.get(code,None)

    def getAllPromotions(self):
        """Returns all the promotions in the system
        pre-condition:None
        post-condition:All the promotions in the system are returned, the return value is a list of objects with both the code and modifier as values"""
        codeComps = []
        for item in self.codes.items():
            promo = Object()
            promo.code = item[0]
            promo.promo = item[1]
            codeComps.append(promo)
        return codeComps

class Object(object):
    pass

class PromoModifier(metaclass = abc.ABCMeta):
    """this class represents a promotion modifier """
    def __init__(self,percentageDiscount):
        self.percentageDiscount = percentageDiscount

    def applyPromotion(self, amount):
        """This function applies the promotion modifier to a price
        pre-condition:The price to apply the discount to should be passed as an argument
        post-condition:The reduced price is returned"""
        return amount * (1 - (self.percentageDiscount/100.0))

class PaymentMethod(metaclass = abc.ABCMeta):
    """Abstract class defines the interface a payment method must implement"""
    @abc.abstractmethod
    def chargeCustomer(self,amount):
        pass

class DebitPayment(metaclass = abc.ABCMeta):
    """This is the debit card implementation of the abstract Payment Method"""
    def __init__(self):
        pass

    def chargeCustomer(self,amount):
        pass

class PaypalPayment(metaclass = abc.ABCMeta):
    """This is the paypal card implementation of the abstract Payment Method"""
    def __init__(self):
        pass

    def chargeCustomer(self,amount):
        pass

class CardPayment(metaclass = abc.ABCMeta):
    """This is the credit card card implementation of the abstract Payment Method"""
    def __init__(self,cardNo,csv):
        self.cardNo = cardNo
        self.csv = csv

    def chargeCustomer(self,amount):
        pass