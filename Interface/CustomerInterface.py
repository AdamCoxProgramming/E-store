from .AdminInterface import AdminState
from BusinessLayer.Customer import Customers, Customer
from BusinessLayer.Seller import Sellers
from BusinessLayer.Basket import PromoCodes, CardPayment, DebitPayment, PaypalPayment,Payment
from BusinessLayer.Products import ProductListings, ProductListing, ProductSupply, ProductStocks
from .SellerInterface import SellerLoginState, SellerCatalogState
from Datastore.Connection import Connection

class Controller:
    """This class is the main controller for the command line interface.
    New interface states can be added to the prevStates stack(list) and the previous state can be re-started."""

    def __init__(self):
        self.prevStates = []

    def start(self,nextState):
        """This function starts the command line program from the state specified
        A state must implement a run function.
        The run function should return the next state and whether or not it is temporary or alternatively a None object.
        Returning a None object will cause the previous state to be resumed.
        The program will end when None is returned and there are no states on the stack to return to.
        pre-condition:The first state should be passed as an argument.
        post-condition:The first state will be run"""
        currNextState = nextState
        reusedState = False
        while True:
            temp = currNextState.tempoary
            if currNextState.tempoary == False and reusedState == False:
                self.prevStates.append(currNextState)
            currNextState = currNextState.nextState.run()
            if currNextState == None:
                reusedState = True
                if temp == False:
                    self.prevStates.pop()
                if len(self.prevStates) == 0:
                    return
                currNextState = self.prevStates[-1]
            else:
                reusedState = False

class LoginState:
    def run(self):
        print("--Customer Login--")
        currentCustomer = None
        doesUserHaveAccount = ''
        while doesUserHaveAccount != 'y' and doesUserHaveAccount != 'n':
            doesUserHaveAccount = input("Do you have an account (y/n): ")
            if doesUserHaveAccount == "back":
                return None

        if doesUserHaveAccount == 'y':
            customer = None
            while customer == None:
                username = input("What is your username: ")
                if username == "back":
                    return None
                customer = Customers().getCustomerByName(username)
                if customer == None:
                    print("User does not exist")
            currentCustomer = customer
        else:
            newUserName = ''
            while newUserName == '':
                newUserName = input("Enter a name for your new account: ")
                if Customers().getCustomerByName(newUserName) != None:
                    print("A user with that name already exists, please use a different name")
                    newUserName = ''
                if newUserName == "back":
                    return None

            newCustomer = Customer(newUserName)
            Customers().addCustomer(newCustomer)
            currentCustomer = newCustomer
            print("Account Created")

        return NextState(CustomerState(currentCustomer),False)

class NextState:
    def __init__(self,nextState,tempory):
        self.nextState = nextState
        self.tempoary = tempory

class CustomerState:
    def __init__(self,customer):
        self.customer = customer

    def run(self):
        print("--" + self.customer.name + "s Account--")
        searchCommand = "search products"
        basketCommand = "open basket"
        ordersCommand = "view history"
        posCommands = [searchCommand, basketCommand, ordersCommand]
        print("Type either: '" + "' ,'".join(posCommands) + "'")

        command = ''
        while command not in posCommands:
            command = input("What do you want to do?: ")
            if command == "back":
                return None

        if command == searchCommand:
            return NextState(ProductsSearch(self.customer),False)
        elif command == basketCommand:
            return NextState(BasketState(self.customer),False)
        elif command == ordersCommand:
            return NextState(ViewOrdersState(self.customer),False)

class BasketState:
    def __init__(self,customer):
        self.customer = customer

    def run(self):
        print("--" + self.customer.name + "s Basket--")
        print("Items in basket:")
        basketItems = self.customer.basket.getItems()
        if len(basketItems) == 0:
            print("    Basket empty")
        else:
            for productStock in basketItems:
                productListing = ProductListings().searchFromProductById(productStock.productId)
                productSeller = Sellers().searchVendorById(productStock.sellerId)
                print("    " + productListing.name + ": $" + str(productStock.price) + ", ordered from: " + productSeller.getName())

        res = ''
        while res != 'back' and res != 'checkout':
            res = input("type 'back' or 'checkout': ")

        if res == 'back':
            return None
        elif res == "checkout":
            if len(basketItems) ==0:
                print("You have no items in your basket to checkout")
                self.run()
            else:
                return NextState(CheckoutState(self.customer.basket.createOrderDescription(),
                                               self.customer.storedPaymentMethod, self.customer),True)

class CheckoutState:
    def __init__(self,orderDescription,storedPaymentMethod,customer):
        self.orderDescription = orderDescription
        self.storedPaymentMethod = storedPaymentMethod
        self.payment = Payment()
        self.customer = customer

    def run(self):
        print("--Checkout--")

        payment = Payment()
        deliveryAddress = ''
        while deliveryAddress == '':
            deliveryAddress= input("Please type your delivery address: ")
            if deliveryAddress == 'back':
                return None
            if deliveryAddress == '':
                print("Delivery address cannot be empty")

        print("Now select delivery options for your ordered products")
        for orderedItem in self.orderDescription.getOrderedItems():
            seller = Sellers().searchVendorById(orderedItem.productStock.sellerId)
            deliveryOptions = seller.getDeliveryOptions()
            productListing = ProductListings().searchFromProductById(orderedItem.productStock.productId)
            print("Delivery options for the " + productListing.name + ": ")
            for deliveryOption in deliveryOptions:
                print("    " + deliveryOption.name + ", $" + str(deliveryOption.price))

            deliveryOption = None
            while deliveryOption == None:
                optInput = input("Type the name of the delivery option to use: ")
                if optInput == 'back':
                    return None

                for option in deliveryOptions:
                    if option.name == optInput:
                        deliveryOption = option

            orderedItem.deliveryOption = deliveryOption

        usePromoInput = ''
        while usePromoInput != 'y' and usePromoInput != 'n':
            usePromoInput = input("Do you want to use a promotional code (y/n): ")
            if usePromoInput == "back":
                return None

        promoApplied = False
        if usePromoInput == 'y':
            validCode = False
            while validCode == False:
                codeInput = input("Enter your promotion code: ")
                if codeInput == "back":
                    return None
                else:
                    realCode = PromoCodes().getPromotion(codeInput)
                    if realCode != None:
                        payment.applyDiscount(realCode)
                        validCode = True
                        promoApplied = True

        if promoApplied:
            print("Total price before promotion: $" + str(self.orderDescription.getTotalPrice()))
            print("Price after promotion code: $" + str(payment.calculatePriceAfterPromo(self.orderDescription)))
        else:
            print("Total price: $" + str(self.orderDescription.getTotalPrice()))

        useStoredPaymentMethod = False
        if self.storedPaymentMethod != None:
            useStored = ''
            while useStored != 'y' and useStored != 'n':
                useStored = input("Do you want to use your stored payment method?(y,n): ")
                if useStored == "back":
                    return None
            useStoredPaymentMethod = useStored == 'y'

        paymentMethod = None
        toStore = False
        if not useStoredPaymentMethod:
            paymentTypeInput = ''
            while paymentTypeInput != 'credit' and paymentTypeInput != 'debit' and paymentTypeInput != 'paypal':
                paymentTypeInput = input("What payment type do you want to use (credit,debit,paypal): ")
                if paymentTypeInput == "back":
                    return None

            if paymentTypeInput == 'credit':
                paymentMethod = CardPayment(0,0)
            if paymentTypeInput == 'debit':
                paymentMethod = DebitPayment()
            if paymentTypeInput == 'paypal':
                paymentMethod = PaypalPayment()

            toStoreInput = ''
            while toStoreInput != 'y' and toStoreInput != 'n':
                toStoreInput = input("Do you want to store this payment method for future use?(y,n): ")
                if toStoreInput == "back":
                    return None
            if toStoreInput == 'y':
                toStore = True
        else:
            paymentMethod = self.storedPaymentMethod

        if toStore: #Only store when the payment is complete
            self.customer.storedPaymentMethod = paymentMethod

        payment.payForOrder(self.orderDescription, paymentMethod, deliveryAddress)
        self.customer.basket.clearBasket()

        print("Payment successful, you have ordered the products!")

    def choosePaymentOptions(self):
        pass

class ProductsSearch():
    def __init__(self, customer):
        self.customer = customer
    def run(self):
        searchRes = self.searchProducts()
        if searchRes is None:
            return None

        result = False
        while result == False:
            result = self.nextStep(searchRes)

        if result == None:  # User wants to go back
            return None
        else:
            return result

    def nextStep(self,searchResults):
        res = input("Type 'view' product name, or type 'search' to start another search: ")
        if res == "back":
            return None
        if res == 'search':
            return self.run()
        if res.startswith("view"):
            if len(res) < 5:
                return False
            productNameInput = res.split("view")[1].strip()

            realProductName = False

            for product in searchResults:
                if product.name == productNameInput:
                    realProductName = True

            if not realProductName:
                print("That product name is not in the search result")
                return False
            else:
                return NextState(ViewProductState(productNameInput , self.customer),False)
        else:
            return False

    def searchProducts(self):
        print("--Product Search--")
        keywords = input("Type in keywords to search by: ")
        if keywords == "back":
            return None
        results = ProductListings().searchForProducts(keywords.split(" "))
        print("Search Results:")
        if len(results) != 0:
            for item in results:
                print("    " + str(item))
        else:
            print("No results match those keywords")
        return results

class ViewProductState():
    def __init__(self, productName, customer):
        self.productName = productName
        self.customer = customer

    def run(self):
        print("--Viewing " + self.productName + "--")
        productListing = ProductListings().searchForProduct(self.productName)
        productSupplys = ProductStocks().searchForProductStock(productListing.id)

        productStockBySellerName = {}
        supplyTexts = []
        for productSupply in productSupplys:
            seller = Sellers().searchVendorById(productSupply.sellerId)
            supplyTexts.append(seller.getName() + " - price: $" + str(productSupply.price) + ", "
                               + "stock remaining : " + str(productSupply.quantity))
            productStockBySellerName[seller.getName()] = productSupply

        print(productListing.name + " is available from: ")
        if len(supplyTexts)==0:
            print("No one")
        else:
            for supplyText in supplyTexts:
                print("    " + supplyText)

        result = False
        while result == False:
            result = self.addToBasketOrBack(productStockBySellerName)

        return result

    def addToBasketOrBack(self,productStockBySellerName):
        orderText = input("type either 'order from name' or 'view *sellers name*': ")
        if orderText == 'back':
            return None

        if orderText.startswith("view") and len(orderText) > len("view"):
            sellerName = orderText.split("view")[1].strip()
            seller = Sellers().searchVendorByName(sellerName)
            if seller != None:
                return NextState(SellerCatalogState(seller),False)

        elif orderText.startswith("order from") and len(orderText) > len("order from"):
            sellerName = orderText.split("order from")[1].strip()

            productSupplyToOrder = productStockBySellerName.get(sellerName, None)
            if productSupplyToOrder == None:
                print("Invalid Seller name")
                return False

            self.customer.basket.addItem(productSupplyToOrder)

            print("A " + self.productName + " from the seller " + sellerName + " has been added to your basket, " +
                  "proceed to the check out when you are ready")

class ViewOrdersState():
    def __init__(self, customer):
        self.customer = customer

    def run(self):
        print("--Customer Purchase History--")
        customersOrders = self.customer.getOrders()
        if len(customersOrders) == 0:
            print("You have no purchases")
        else:
            print("Orders:")
            for order in customersOrders:
                print(order)

        while input("Type 'back' when done: ") != 'back':
            pass
        return None

class WelcomeState():
    def run(self):
        print("--Weclome--")
        print("Type 'back' at anytime to return to the previous state")
        userType = ''
        while userType != 'customer' and userType != 'admin' and userType != 'seller':
            if userType == 'back':
                return None
            userType = input("What type of user are you?(customer,admin,seller): ")
        if userType == 'customer':
            return NextState(LoginState(),False)
        if userType == 'admin':
            return NextState(AdminState(),False)
        if userType == 'seller':
            return NextState(SellerLoginState(),True)
        return

def startProgram(isTesting):
    if not isTesting:
        Connection().usePrimaryDatabase()
    controller = Controller()
    controller.start(NextState(WelcomeState(),False))
