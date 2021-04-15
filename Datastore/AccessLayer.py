from .Connection import Connection

def getCustomerId(name):
    select_customer = "SELECT * FROM customers WHERE name ='" + name +"';"
    customerRows = Connection.connection.execute_query(select_customer)
    if len(customerRows) == 0:
        return None
    return customerRows[0][0]

def getCustomerName(id):
    select_customer = "SELECT name FROM customers WHERE id ='" + str(id) + "';"
    customerRows = Connection.connection.execute_query(select_customer)
    if len(customerRows) == 0:
        return None
    return customerRows[0][0]

def addCustomer(customer):
    insert_customer = """ INSERT INTO customers (name) VALUES (""" + "'" + customer.name + "'" + ");"
    return Connection.connection.execute_query(insert_customer)

def addProductListing(name,tags):
    insert_listing = " INSERT INTO  product_listings (name)    VALUES      ('" + name + "');"
    Connection.connection.execute_query(insert_listing)
    select_listing = "SELECT id FROM product_listings WHERE name ='" + name + "';"
    listingId = Connection.connection.execute_query(select_listing)[0][0]
    values = ''
    for tag in tags:
        values += "( " + str(listingId) + " ,'" + tag.strip() +"'),"
    values = values[0:-1]
    insert_listing_tags = " INSERT INTO  product_listing_tags (product_id,tag) VALUES " + values + ";"
    Connection.connection.execute_query(insert_listing_tags)
    return listingId

def getProductListingByName(name):
    select_listing = "SELECT id FROM product_listings WHERE name ='" + name + "';"
    listingRows = Connection.connection.execute_query(select_listing)
    if len(listingRows) == 0:
        return None
    listingid = listingRows[0][0]
    tagsQuery = "SELECT tag FROM product_listing_tags WHERE product_id = " + str(listingid) + ";"
    tagsRows = Connection.connection.execute_query(tagsQuery)
    tags = []
    for tagsRow in tagsRows:
        tags.append(tagsRow[0])
    listing =  [name,tags,listingid]
    return listing

def getProductListingNameById(id):
    select_listing = "SELECT id,name FROM product_listings WHERE id = " + str(id) + ";"
    listingRows = Connection.connection.execute_query(select_listing)
    if len(listingRows) == 0:
        return None
    listingName = listingRows[0][1]
    tagsQuery = "SELECT tag FROM product_listing_tags WHERE product_id = " + str(id) + ";"
    tagsRows = Connection.connection.execute_query(tagsQuery)
    tags = []
    for tagsRow in tagsRows:
        tags.append(tagsRow[0])
    listing =  [listingName,tags,id]
    return listing

def getProductListingIdsByTags(tags):
    tagsStr = ""
    for tag in tags:
        tagsStr += "'" + tag + "',"
    tagsStr = tagsStr[0:-1]
    select_tags = "SELECT product_id FROM product_listing_tags WHERE tag IN( " + tagsStr + ");"
    idsRows = Connection.connection.execute_query(select_tags)
    ids = []
    for idsRow in idsRows:
        ids.append(idsRow[0])
    return ids

def getAllProductListingIds():
    select_tags = "SELECT id FROM product_listings;"
    idsRows = Connection.connection.execute_query(select_tags)
    ids = []
    for idsRow in idsRows:
        ids.append(idsRow[0])
    return ids

def addSeller(name):
    insert_seller = """ INSERT INTO  sellers (name) VALUES (""" + "'" + name + "'" + ");"
    Connection.connection.execute_query(insert_seller)
    return getSellerId(name)

def getSellerId(name):
    select_id = "SELECT id FROM sellers WHERE name = '" + name + "';"
    idRows = Connection.connection.execute_query(select_id)
    if len(idRows) == 0:
        return None
    return idRows[0][0]

def getSeller(id):
    select_name = "SELECT name FROM sellers WHERE id = " + str(id) + ";"
    nameRows = Connection.connection.execute_query(select_name)
    if len(nameRows) == 0:
        return None
    return nameRows[0][0]

def addProductStock(price, quantity,sellerId,productId):
    insert_seller = "INSERT INTO product_supplies (price,quantity,seller_id,product_id) VALUES (" \
                    + str(price) + "," + str(quantity) + "," + str(sellerId) + "," + str(productId) + ");"
    return Connection.connection.execute_query(insert_seller)

def getProductStocksByProductId(id):
    select_stock = "SELECT price,quantity,seller_id,product_id, id FROM product_supplies WHERE product_id = " + str(id) + ";"
    return Connection.connection.execute_query(select_stock)

def getProductStocksByProductStockId(id):
    select_stock = "SELECT price,quantity,seller_id,product_id, id FROM product_supplies WHERE id = " + str(id) + ";"
    res = Connection.connection.execute_query(select_stock)
    if len(res) == 0:
        return None
    else:
        return res[0]

def getProductStockBySellerId(id):
    select_stock = "SELECT price,quantity,seller_id,product_id, id FROM product_supplies WHERE seller_id = " + str(id) + ";"
    return Connection.connection.execute_query(select_stock)

def updateQuantity(sellerId,productId,quantityChange):
    update_quanity = "UPDATE product_supplies SET quantity = quantity + " + str(quantityChange) + \
                  " WHERE seller_id = " + str(sellerId) + " AND" + " product_id = " + str(productId) + ";"
    return Connection.connection.execute_query(update_quanity)

def addDeliveryOption(price,sellerId,name):
    insert_delivery_option = "INSERT INTO delivery_options (price,seller_id,name) VALUES (" + str(price) + "," + str(sellerId) + ",'" + name + "');"
    Connection.connection.execute_query(insert_delivery_option)

def getDeliveryOptionsForSeller(id):
    select_delivery_options = "SELECT price,name FROM delivery_options WHERE seller_id = " + str(id) + ";"
    return Connection.connection.execute_query(select_delivery_options)

def addOrderedItem(stockId,state,deliveryOptionId,storeOrderdId,sellerId):
    insert_item = "INSERT INTO ordered_items (supply_id,state,delivery_option_id,store_order_id,seller_id) VALUES ("\
                             + str(stockId) + ",'" + state + "'," + str(deliveryOptionId) + "," + str(storeOrderdId) + "," + str(sellerId) + ");"
    Connection.connection.execute_query(insert_item)

def getOrderedItemsForStoreOrder(storeOrderId):
    select_items = "SELECT supply_id, state, delivery_option_id, store_order_id, seller_id, id FROM ordered_items WHERE store_order_id = " + str(storeOrderId) + ";"
    return Connection.connection.execute_query(select_items)

def getOrderdItemsForSeller(sellerId):
    select_items = "SELECT supply_id, state, delivery_option_id, store_order_id, seller_id, id FROM ordered_items WHERE seller_id = " + str( sellerId) + " AND state = 'Awaiting Shipment';"
    return Connection.connection.execute_query(select_items)

def setOrderedItemShipped(id):
    update_shipped = "UPDATE ordered_items SET state = 'Shipped' WHERE id = " + str(id) + ";"
    Connection.connection.execute_query(update_shipped)

def addStoreOrder(customerId,address):
    insert_item = "INSERT INTO store_orders (customer_id,address) VALUES (" + str(customerId) + ",'" + address + "');"
    return Connection.connection.execute_query(insert_item)

def getOrdersForCustomer(customerId):
    select_orders = "SELECT date, address, id FROM store_orders WHERE customer_id = '" + str(customerId) + "';"
    return Connection.connection.execute_query(select_orders)

def getOrder(storeOrderId):
    select_order = "SELECT date, address, id, customer_id FROM store_orders WHERE id = " + str(storeOrderId) + ";"
    res = Connection.connection.execute_query(select_order)
    if len(res) == 0:
        return None
    else:
        return res[0]

def addBasketItem(customerId,supplyId):
    insert_item = "INSERT INTO basket_items (customer_id,supply_id) VALUES (" + str(customerId) + "," + str(supplyId) + ");"
    Connection.connection.execute_query(insert_item)

def getBasketItems(customerId):
    select_items = "SELECT customer_id, supply_id, id FROM basket_items WHERE customer_id = " + str(customerId) + ";"
    return Connection.connection.execute_query(select_items)

def clearBasket(customerId):
    delete_items = "DELETE FROM basket_items WHERE customer_id = " + str(customerId) + ";"
    Connection.connection.execute_query(delete_items)