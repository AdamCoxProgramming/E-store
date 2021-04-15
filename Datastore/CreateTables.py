from .Connection import Connection

def test():
    print(Connection.connection.execute_query("SELECT * FROM product_supplies;"))


def dropAllTables():
    """This function removes all the tables from the database.
     If a new table is added make sure to update this function"""
    Connection.connection.execute_query("DROP TABLE IF EXISTS customers;")
    Connection.connection.execute_query("DROP TABLE IF EXISTS sellers;")
    Connection.connection.execute_query("DROP TABLE IF EXISTS product_listings;")
    Connection.connection.execute_query("DROP TABLE IF EXISTS product_listing_tags;")
    Connection.connection.execute_query("DROP TABLE IF EXISTS product_supplies;")
    Connection.connection.execute_query("DROP TABLE IF EXISTS delivery_options;")
    Connection.connection.execute_query("DROP TABLE IF EXISTS ordered_items;")
    Connection.connection.execute_query("DROP TABLE IF EXISTS store_orders;")
    Connection.connection.execute_query("DROP TABLE IF EXISTS basket_items;")

def createTables():
    """This function adds all the tables from the database.
    pre-condition:Make sure the database is empty before calling this function.
    Call this before inserting or selecting any data.
    post-condition:All the required tables are created"""

    create_customers_table = """
    CREATE TABLE IF NOT EXISTS customers (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL
    );
    """
    Connection.connection.execute_query(create_customers_table)

    create_customers_table = """
    CREATE TABLE IF NOT EXISTS sellers (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL
    );
    """
    Connection.connection.execute_query(create_customers_table)

    create_product_listings_table = """
        CREATE TABLE IF NOT EXISTS product_listings (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL          
        );
        """
    Connection.connection.execute_query(create_product_listings_table)

    create_product_tags_table = """
        CREATE TABLE IF NOT EXISTS product_listing_tags (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          product_id INTEGER NOT NULL,
          tag TEXT NOT NULL          
        );
        """
    Connection.connection.execute_query(create_product_tags_table)

    create_product_supplies_table = """
        CREATE TABLE IF NOT EXISTS product_supplies (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          price INTEGER NOT NULL,
          seller_id INTEGER NOT NULL,
          product_id INTEGER NOT NULL,
          quantity INTEGER NOT NULL          
        );
        """
    Connection.connection.execute_query(create_product_supplies_table)

    create_delivery_options_table = """
        CREATE TABLE IF NOT EXISTS delivery_options (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          seller_id INTEGER NOT NULL,
          price INTEGER NOT NULL         
        );
        """
    Connection.connection.execute_query(create_delivery_options_table)

    create_ordered_items_table = """
        CREATE TABLE IF NOT EXISTS ordered_items (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          supply_id INTEGER NOT NULL,
          state TEXT NOT NULL,
          delivery_option_id INTEGER NOT NULL,
          store_order_id INTEGER NOT NULL,
          seller_id  INTEGER NOT NULL        
        );
        """
    Connection.connection.execute_query(create_ordered_items_table)

    create_store_orders_table = """
        CREATE TABLE IF NOT EXISTS store_orders (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          customer_id INTEGER NOT NULL,
          date DATETIME DEFAULT CURRENT_TIMESTAMP ,
          address TEXT NOT NULL     
        );
        """
    Connection.connection.execute_query(create_store_orders_table)

    create_basket_table = """
        CREATE TABLE IF NOT EXISTS basket_items (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          supply_id INTEGER NOT NULL,
          customer_id INTEGER NOT NULL
        );
        """
    Connection.connection.execute_query(create_basket_table)