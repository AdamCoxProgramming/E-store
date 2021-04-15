from BusinessLayer.Seller import Seller, Sellers, DeliveryOption
from BusinessLayer.Products import ProductListings, ProductListing, ProductSupply
from BusinessLayer.Seller import Sellers


class aNewState:
    def __init__(self,nextState,tempoary):
        self.nextState = nextState
        self.tempoary = tempoary

class SellerLoginState:

    def run(self):
        print("--Seller Login--")
        currentSeller = None
        doesSellerHaveAccount = ''
        while doesSellerHaveAccount != 'y' and doesSellerHaveAccount != 'n':
            doesSellerHaveAccount = input("Do you have an account (y/n): ")
            if doesSellerHaveAccount == "back":
                return None

        if doesSellerHaveAccount == 'y':
            seller = None
            while seller == None:
                username = input("What is your account name: ")
                if username == "back":
                    return None
                seller = Sellers().searchVendorByName(username)
                if seller == None:
                    print("Account does not exist")
            currentSeller = seller
        else:
            newAccountName = ''
            while newAccountName == '':
                newAccountName = input("Enter a name for your new account: ")
                if Sellers().searchVendorByName(newAccountName) != None:
                    print("An account with that name already exists, please use a different name")
                    newAccountName = ''
                if newAccountName == "back":
                    return None

            newSeller = Seller(newAccountName)
            Sellers().addVendor(newSeller)
            currentSeller = newSeller
            print("Account Created")

        return aNewState(SellerAccountState(currentSeller),False)

class SellerAccountState:
    def __init__(self,seller):
        self.seller = seller

    def run(self):
        print("--" + self.seller.getName() + "'s Seller Account--")

        catalogCommand = "view catalog"
        ordersCommand = "view orders"
        stockCommand = "manage products"
        deliveryCommand = "delivery options"
        posCommands = [catalogCommand, ordersCommand, stockCommand,deliveryCommand]
        print("Type either: '" + "' ,'".join(posCommands) + "'")

        command = ''
        while command not in posCommands:
            command = input("What do you want to do?: ")
            if command == "back":
                return None

        if command == catalogCommand:
            return aNewState(SellerCatalogState(self.seller), False)
        elif command == ordersCommand:
            return aNewState(ViewOrdersState(self.seller), False)
        elif command == stockCommand:
            return aNewState(StockState(self.seller), False)
        elif command == deliveryCommand:
            return aNewState(DeliveryOptionsState(self.seller), False)

class DeliveryOptionsState:
    def __init__(self,seller):
        self.seller = seller

    def run(self):
        print("--" + self.seller.getName() + "'s Delivery Options--")
        print("The delivery options you provide are:")
        options = self.seller.getDeliveryOptions()
        if len(options) == 0:
            print("    No delivery options specified")
        for option in options:
            print("    " + option.name + ", $" + str(option.price))
        res = ''
        while res != 'add':
            res = input("Type 'add' or 'back'")
            if res == 'back':
                return None

        if res == 'add':

            currentDeliveryOptions = self.seller.getDeliveryOptions()

            name = ''
            while name == '':
                name = input("Name this new delivery option:")
                if name =='back':
                    return
                nameIsTaken = False

                for option in currentDeliveryOptions:
                    if option.name == name:
                        nameIsTaken = True
                        print("A delivery options with this name already exists")
                if nameIsTaken:
                    name = ''

            price = None
            while price == None:
                priceInput = input("What price is this delivery option?:")
                if priceInput == 'back':
                    return None
                if not priceInput.isnumeric():
                    price = None
                else:
                    price = int(priceInput)

            self.seller.addDeliveryOption(DeliveryOption(name,price,self.seller.id))

            print(name + " has been added as a delivery option")

        return None


class SellerCatalogState:
    def __init__(self,seller):
        self.seller = seller

    def run(self):
        print("--" + self.seller.getName() + "'s Seller Catalog--")

        printCatalogList(self.seller)

        while input("type 'back'") != 'back':
            pass

def printCatalogList(seller):
    productStocks = seller.getCatalog()
    if len(productStocks) == 0:
        print("This seller has no products available")
    else:
        for stock in productStocks:
            productListing = ProductListings().searchFromProductById(stock.productId)
            print("    " + productListing.name + ", $" + str(stock.price) + ", quantity in stock: " + str(
                stock.quantity))

class StockState:
    def __init__(self, seller):
        self.seller = seller

    def run(self):
        print("--Stock Management--")
        addCommand = "add to catalog"
        stockCommand = "add stock"
        possCommands = [addCommand, stockCommand]
        print("Type either: '" + "' ,'".join(possCommands) + "'")

        command = ''
        while command not in possCommands:
            command = input("What do you want to do?: ")
            if command == "back":
                return None

        if command == addCommand:
            return aNewState(StockNewProductState(self.seller), False)
        elif command == stockCommand:
            return aNewState(AddStockState(self.seller), False)

class StockNewProductState:
    def __init__(self,seller):
        self.seller = seller

    def run(self):
        print("--Add To Catalog--")
        print("the products that can be sold on this site are:")
        products = ProductListings().getAllListings()
        for product in products:
            print("    " + product.name)

        productName = None
        productToSell = None
        while productName == None:
            productNameInput = input("What is the name of the product you would like to sell?:")
            if productNameInput == 'back':
                return None

            validName= False
            for product in products:
                if product.name == productNameInput:
                    validName = True
                    productToSell = product
            if validName:
                productName = productNameInput

        price = None
        while price == None:
            priceInput = input("What price would you like to sell this product for:")
            if priceInput == 'back':
                return None
            if not priceInput.isnumeric():
                price = None
            else:
                price = int(priceInput)

        amountToAdd = None
        while amountToAdd == None:
            amountToAddInput = input("What quantity of stock would you like to add?:")
            if amountToAddInput == 'back':
                return None
            if not amountToAddInput.isnumeric():
                amountToAdd = None
            else:
                amountToAdd = int(amountToAddInput)

        productSupply = ProductSupply(price, amountToAdd, self.seller.id, productToSell.id)
        self.seller.addProductSupplyToCatalog(productSupply)

        print("You have added " + productName + " to your catalog")

class AddStockState:
    def __init__(self,seller):
        self.seller = seller

    def run(self):
        print("--Add Additional Product Stock--")
        printCatalogList(self.seller)

        productName = ''
        productSupply = None
        while productSupply == None:
            productName = input("What is the products name you want to add more stock for?")
            if productName == 'back':
                return None
            productListing = ProductListings().searchForProduct(productName)
            if productListing != None:
                catalog = self.seller.getCatalog()
                for supply in catalog:
                    if supply.productId == productListing.id:
                        productSupply = supply
            if productSupply is None:
                print("you do not stock a product with that name")

        amountToAdd = None
        while amountToAdd == None:
            amountToAddInput = input("What quantity of stock would you like to add?:")
            if amountToAddInput == 'back':
                return None
            if not amountToAddInput.isnumeric():
                amountToAdd = None
            else:
                amountToAdd = int(amountToAddInput)

        productSupply.addStock(amountToAdd)

        print(str(amountToAdd) + " more " + productName + " stock added")

class ViewOrdersState:
    def __init__(self, seller):
        self.seller = seller

    def run(self):
        print("--Customer Orders--")
        ordersPendingDeliver = self.seller.getSellerOrdersLeftToShip()
        if len(ordersPendingDeliver) == 0:
            print("There are no pending orders to deliver")
        else:
            for order in ordersPendingDeliver:
                productListing = ProductListings().searchFromProductById(order.orderedItem.productStock.productId)
                print("    orderID:" + str(order.orderedItem.id) +  " " + order.customer.name + " ordered a "
                      + productListing.name + ", delivery option: " + order.orderedItem.deliveryOption.name)

        stepRes = False
        while stepRes == False:
            stepRes = self.handleNextStep(ordersPendingDeliver)

        return stepRes

    def handleNextStep(self,pendingOrders):
        inputRes = input("Type 'back' or 'notify shipped'  ")

        if inputRes.startswith("back"):
            return None
        elif inputRes.startswith('notify shipped'):

            validOrderId = False
            firstTime = True
            while not validOrderId:
                if not firstTime:
                    print('Invalid order number')
                firstTime = False
                orderID = input('What is the orderID of the shipped product?:')
                if orderID.startswith('back'):
                    return  None
                for order in pendingOrders:
                    if str(order.orderedItem.id) == orderID:
                        order.notifyAsShipped()
                        print("order " + str(orderID) + 's shipment has been notified')
                        return None
                else:
                    validOrderId = False
        else:
            return False