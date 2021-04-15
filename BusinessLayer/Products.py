from Datastore.AccessLayer import addProductListing, getProductListingByName,\
    getProductListingNameById, getProductListingIdsByTags, getAllProductListingIds,\
    addProductStock, getProductStocksByProductId, getProductStockBySellerId, updateQuantity, getProductStocksByProductStockId

class ProductListings:
    """A factory for creating and returning ProductListing objects for listings stored in the system"""

    def searchFromProductById(self, productId):
        """Returns a specific product listing
        pre-condition:The id of the product listing needs to be passed as an argument
        post-condition:If a listing with the provided id exists it is returned, other wise a None object is returned"""
        listingArr = getProductListingNameById(productId)
        if listingArr == None:
            return None
        listing = ProductListing(listingArr[0], listingArr[1])
        listing.id = listingArr[2]
        return listing

    def searchForProduct(self, name):
        """Returns a specific product listing
        pre-condition:The name of the product listing needs to be passed as an argument
        post-condition:If a listing with the provided name exists it is returned, other wise a None object is returned"""
        listingArr = getProductListingByName(name)
        if listingArr == None:
            return None
        listing = ProductListing(listingArr[0],listingArr[1])
        listing.id = listingArr[2]
        return listing

    def searchForProducts(self, tags):
        """Returns all product listings that feature any of the tags provided
        pre-condition:A list of tags (strings) must be provided as an argument
        post-condition:A list of corresponding product listings is returned"""
        ids= getProductListingIdsByTags(tags)
        listings = []
        for id in list(set(ids)):#unique ids
            listings.append(self.searchFromProductById(id))
        return listings

    def addProduct(self, productListing):
        """Stores a new product listing in the system
        pre-condition:A product listing should be provided as an argument
        post-condition:The product listing is stored in the system"""
        addProductListing(productListing.name, productListing.tags)

    def getAllListings(self):
        """Returns a list of all product listings stored in the system
        pre-condition:None
        post-condition:A list of all product listings is returned"""
        ids = getAllProductListingIds()
        listings = []
        for id in list(set(ids)):  # unique ids
            listings.append(self.searchFromProductById(id))
        return listings

class ProductStocks:
    """A factory for creating and returning ProductStock objects for stocks stored in the system"""
    def addProductSupply(self, productSupply):
        """Stores a new product stock in the system
        pre-condition:A product stock should be provided as an argument
        post-condition:The product stock is stored in the system, and the argument stock has its id updated with the corresponding id"""
        id = addProductStock(productSupply.price, productSupply.quantity,productSupply.sellerId,productSupply.productId)
        productSupply.id = id

    def searchForProductStock(self, productId):
        """Returns a list of all the stocks of a particular product
        pre-condition:A product id should be provided as an argument
        post-condition:A list of all all stocks of the specified product is returned"""
        stockArrs = getProductStocksByProductId(productId)
        matchingSupplys = []
        for stockArr in stockArrs:
            matchingSupplys.append(self._stockArrToStock(stockArr))
        return matchingSupplys

    def getProductStock(self,productStockId):
        """Returns a specific product stock
        pre-condition:A product stock id should be provided as an argument
        post-condition:If a stock with the provided id exists it is returned, other wise a None object is returned"""
        stockArr = getProductStocksByProductStockId(productStockId)
        if stockArr == None:
            return None
        else:
            return self._stockArrToStock(stockArr)

    def _stockArrToStock(self, stockArr):
        """Converts the array returned from the access layer into a ProductStock object
        pre-condition:A array from the access layer should be provided as an argument
        post-condition:A product stock filled in with the appropriate details will be returned"""
        supply = ProductSupply(stockArr[0],stockArr[1],stockArr[2],stockArr[3])
        supply.id = stockArr[4]
        return supply

    def searchForSellerStocks(self, vendorId):
        """Returns a list of all the stocks a particular seller sells
        pre-condition:A seller id should be provided as an argument
        post-condition:A list of all all stocks sold by a specific seller is returned"""
        stockArrs = getProductStockBySellerId(vendorId)
        matchingSupplys = []
        for stockArr in stockArrs:
            matchingSupplys.append(self._stockArrToStock(stockArr))
        return matchingSupplys

class ProductListing:
    """This class represents an product that can be sold on the e-store"""
    def __init__(self, name, tags):
        self.name = name
        self.tags = tags
        self.id = -1  # the id is populated when the listing is added to the product list

    def __str__(self):
        """Formats a string that represents the contents of this object"""
        return self.name + " : " + ",".join(self.tags)

class ProductSupply:
    """This class represents a sellers stock of product that customer can purchase"""
    def __init__(self, price, quantity, sellerId, productId):
        self.price = price
        self.quantity = quantity
        self.sellerId = sellerId
        self.productId = productId
        self.id = -1#get added when added to ProductStocks

    def __str__(self):
        """Formats a string that represents the contents of this object"""
        return "$" + str(self.price) + " , quantity: " + str(self.quantity) + ", vendorId: " + str(
            self.sellerId) + ", productId: " + str(self.productId)

    def notifyItemsShipped(self,quanityShipped):
        """Updates the system changing the quantity remaining of the stock by a specific amount
        pre-condition:The amount that has been shipped should be passed as an argument (as an integer)
        post-condition:Updates the quantity of stock remaining"""
        updateQuantity(self.sellerId,self.productId,-quanityShipped)
        self.quantity = self.quantity - quanityShipped

    def addStock(self,quantity):
        """Updates the system changing the quantity remaining of the stock by a specific amount
        pre-condition:The amount that has been added should be passed as an argument (as an integer)
        post-condition:Updates the quantity of stock remaining"""
        updateQuantity(self.sellerId,self.productId,quantity)
        self.quantity += quantity