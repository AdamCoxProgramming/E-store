from BusinessLayer.Products import ProductListings, ProductListing
from BusinessLayer.Basket import PromoCodes, PromoModifier

class NewState:
    def __init__(self,nextState,tempoary):
        self.nextState = nextState
        self.tempoary = tempoary

class AdminState:
    def run(self):
        print("--Administrator--")
        manageProductListings = "manage listings"
        mangagePromos = "manage promotions"
        posCommands = [manageProductListings, mangagePromos]
        print("Type either: '" + "' ,'".join(posCommands) + "'")

        command = ''
        while command not in posCommands:
            command = input("What do you want to do?: ")
            if command == "back":
                return None

        if command == manageProductListings:
            return NewState(ManageProductListingsState(), False)
        elif command == mangagePromos:
            return NewState(ManagePromotionsState(), False)

class ManageProductListingsState:
    def run(self):
        print("--Product Listings--")
        allListings = ProductListings().getAllListings()
        if len(allListings) == 0:
            print("    There are no product listings")
        else:
            print("All products:")
            for listing in allListings:
                print("    " + str(listing))

        addCommand = "add"
        posCommands = [addCommand]
        print("Type either: '" + "' ,'".join(posCommands) + "'")
        command = ''
        while command not in posCommands:
            command = input("What do you want to do?: ")
            if command == "back":
                return None
        if command == addCommand:
            return NewState(AddProduct(),False)

class AddProduct:
    def run(self):
        print("--Add Product Listing--")
        name = ''
        while name == '':
            name = input("What is the new products name?: ")
            if name == "back":
                return None
            if ProductListings().searchForProduct(name) != None:
                print("A product with that name already exists")
                name = ''

        tagsString = input("What are the products tags (comma sepereated, i.e phone,samsung,galaxy)?: ")
        if tagsString == "back":
            return None
        tags = tagsString.split(',')
        tagsStripped = [x.strip(' ') for x in tags]
        newProduct = ProductListing(name, tagsStripped)
        products = ProductListings()
        products.addProduct(newProduct)
        print(name + " added to the list of available products")

class ManagePromotionsState:
    def run(self):
        print("--Promotions--")
        allPromotions = PromoCodes().getAllPromotions()
        if len(allPromotions) == 0:
            print("    There are no promotions")
        else:
            print("All promotions:")
            for promotion in allPromotions:
                print("    " + str(promotion.code))

        addCommand = "add"
        possCommands = [addCommand]
        print("Type either: '" + "' ,'".join(possCommands) + "'")
        command = ''
        while command not in possCommands:
            command = input("What do you want to do?: ")
            if command == "back":
                return None
        if command == addCommand:
            return NewState(AddPromoCodeState(),False)

class AddPromoCodeState:
    def run(self):
        print("--Add Promotion--")
        code = ''
        while code == '' :
            code = input("What is the new promotions code?: ")
            if code == "back":
                return None
            if PromoCodes().getPromotion(code) != None:
                print("A promtion with that code already exists")
                code = ''

        discount = -1
        while discount == -1:
            discountInput = input("What is the percentage discount? (type a number between 0 and 100):")
            if discountInput.isnumeric():
                val = int(discountInput)
                if val >=0 and val <= 100:
                    discount = val

        PromoCodes().addPromo(code, PromoModifier(discount))

        print("'" + code + "'" + " added to the list of promotions")

