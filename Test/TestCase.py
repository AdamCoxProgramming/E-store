from BusinessLayer.Customer import Customer, Customers
from BusinessLayer.Basket import PromoCodes, CardPayment, Payment, PromoModifier
from BusinessLayer.Products import ProductListing, ProductListings, ProductSupply
from BusinessLayer.Seller import Sellers, Seller, DeliveryOption, DeliveryOptions
from Datastore.Connection import dbConnection, create_connection
from Datastore.CreateTables import dropAllTables,createTables
import abc

class TestConnection:
    @classmethod
    def resetDatabase(self):
        dropAllTables()
        createTables()

def runBusinessLayerTests():
    TestCases = [AddListing(),AddSeller(),CantAddCustomerWithClashingName(),CantAddSellerWithClashingName(), AddCustomer(),
                 SellerCanStockAProduct(),CustomerCanAddItemToBasket(), AddDeliveryOptions(),CustomerCanPayForOrder(),
                 SellerCanShipOrderedItems()]
    for test in TestCases:
        res = test.runCase()
        print(res['name'] + " : " + str(res['passed']))

class TestCase(metaclass = abc.ABCMeta):
    """Abstract class defines the interface a test case must implement"""
    def runCase(self):
        TestConnection.resetDatabase()
        passed = self.run()
        if passed != True:
            passed = False
        return {"name":self.name,"passed":passed}

    @abc.abstractmethod
    def run(self):
        pass

class AddListing(TestCase):
    name = "AddProductListingTestCase"
    def run(self):
        # create a product listing
        carListing = ProductListing("Car", ["car","Car"])
        products = ProductListings()
        products.addProduct(carListing)
        carRetrivedFromStore = products.searchForProducts(["car"])[0]
        if carRetrivedFromStore.name == 'Car':
            return True

class AddSeller(TestCase):
    name = "AddSeller"
    def run(self):
        # create Sony seller
        sony = Seller("Sony")
        sellers = Sellers()
        sellers.addVendor(sony)
        seller = sellers.searchVendorByName("Sony")
        if seller.getName() == 'Sony':
            return True

class AddCustomer(TestCase):
    name = "AddCustomer"
    def run(self):
        # Create a customer
        customer = Customer("Adam")
        Customers().addCustomer(customer)
        retrievedCustomer = Customers().getCustomerByName("Adam")
        if retrievedCustomer.name == 'Adam':
            return True

class CantAddCustomerWithClashingName(TestCase):
    name = "CantAddCustomerWithClashingName"
    def run(self):
        try:
            customer = Customer("Adam")
            Customers().addCustomer(customer)
            Customers().addCustomer(customer)
        except:
            return True
        return False

class CantAddSellerWithClashingName(TestCase):
    name = "CantAddSellerWithClashingName"
    def run(self):
        try:
            seller = Seller("Adam")
            Sellers().addSeller(seller)
            Sellers().addSeller(seller)
        except:
            return True
        return False

class SellerCanStockAProduct(TestCase):
    name = "SellerCanStockAProduct"
    def run(self):
        storeToyAndHaveSonySupply()
        sonyVendor = Sellers().searchVendorByName("Sony")
        toyRetrieved = ProductListings().searchForProducts(["Toy"])[0]

        fromCatalog = sonyVendor.getCatalog()[0]
        if fromCatalog.productId == toyRetrieved.id:
            return True

def storeToyAndHaveSonySupply():
    # create ps5 product listing
    toy = ProductListing("Toy", ["Toy"])
    products = ProductListings()
    products.addProduct(toy)
    toyRetrieved = products.searchForProducts(["Toy"])[0]

    # create Sony seller
    sony = Seller("Sony")
    vendors = Sellers()
    vendors.addVendor(sony)
    sonyVendor = vendors.searchVendorByName("Sony")

    # have sony supply the ps5
    toySupply = ProductSupply(20, 100, sonyVendor.id, toyRetrieved.id)
    sonyVendor.addProductSupplyToCatalog(toySupply)

def storeAdamCustomer():
    customer = Customer("Adam")
    Customers().addCustomer(customer)
    return Customers().getCustomerByName("Adam")

class CustomerCanAddItemToBasket(TestCase):
    name = "CustomerCanAddItemToBasket"
    def run(self):
        storeToyAndHaveSonySupply()
        sonyVendor = Sellers().searchVendorByName("Sony")
        toyRetrieved = ProductListings().searchForProducts(["Toy"])[0]

        toyFromCatalog = sonyVendor.getCatalog()[0]

        customer = storeAdamCustomer()
        customer.basket.addItem(toyFromCatalog)
        itemFromBasket = customer.basket.getItems()[0]

        if itemFromBasket.productId == toyRetrieved.id:
            return True

class CustomerCanPayForBasket(TestCase):
    name = "CustomerCanPayForBasket"
    def run(self):
        storeToyAndHaveSonySupply()
        sonyVendor = Sellers().searchVendorByName("Sony")
        toyRetrieved = ProductListings().searchForProducts(["Toy"])[0]

        toyFromCatalog = sonyVendor.getCatalog()[0]

        customer = storeAdamCustomer()
        customer.basket.addItem(toyFromCatalog)
        itemFromBasket = customer.basket.getItems()[0]

        if itemFromBasket.productId == toyRetrieved.id:
            return True

class AddDeliveryOptions(TestCase):
    name = "AddDeliveryOptions"
    def run(self):
        storeToyAndHaveSonySupply()
        sonyVendor = Sellers().searchVendorByName("Sony")
        option = DeliveryOption("FastOptTest",10,sonyVendor.id)
        sonyVendor.addDeliveryOption(option)
        optionRetrieved = sonyVendor.getDeliveryOptions()[0]
        if optionRetrieved.name == "FastOptTest":
            return True

class CustomerCanPayForOrder(TestCase):
    name = "CustomerCanPayForOrder"
    def run(self):
        customerOrderProductFromSony()
        return True

def customerOrderProductFromSony():
    storeToyAndHaveSonySupply()
    sonyVendor = Sellers().searchVendorByName("Sony")
    option = DeliveryOption("FastOptTest", 10, sonyVendor.id)
    sonyVendor.addDeliveryOption(option)
    optionRetrieved = sonyVendor.getDeliveryOptions()[0]

    toyRetrieved = ProductListings().searchForProducts(["Toy"])[0]

    customer = storeAdamCustomer()
    customer.basket.addItem(toyRetrieved)

    payment = Payment()
    payment.applyDiscount(PromoCodes().getPromotion(123))
    orderDescription = customer.basket.createOrderDescription()
    orderDescription.getOrderedItems()[0].setDeliveryOption(optionRetrieved)
    payment.payForOrder(orderDescription, CardPayment(124124, 14214), "32 Winding Lane")

class SellerCanShipOrderedItems(TestCase):
    name = "SellerCanShipOrderedItems"
    def run(self):
        customerOrderProductFromSony()
        sonyVendor = Sellers().searchVendorByName("Sony")
        orderedItem = sonyVendor.getSellerOrdersLeftToShip()[0].orderedItem
        orderedItem.setShipped()
        itemsRemaining = sonyVendor.getSellerOrdersLeftToShip()
        if len(itemsRemaining) ==0:
            return True