E-store Documentation

Project Contents
This project contains a Python implementation of an e-store using best OOP practices.
The project features both the system and tests that can be used to verify its correct behaviour.

How To Run
run "python3 main.py" to start up the command-line interface
run "python3 TestMain.py" to run the tests

System
This information systems implementation provides a command-line interface and persists data in a sql database.
I have utilized a three tier architecture for the systems implementation.
The three layers being the BusinessLayer, Datastore and Interface. Each layer has been developed in its own python package.
By separating these layers it becomes easier to make changes to one layer without needing to update the whole system.

Functionality Overview
There are 3 types of users in my system; customers, sellers and administrators.
The administrators are able to decide which products can be sold on the system as well as what promotions are available.
The sellers are able to stock any of the products which can be sold on the system.
Sellers can specify what delivery options they provide.
Once a seller has shipped a product they are able to let the system know so other users can see.
Customers are able to browse the available products and add them to their basket.
Customers can checkout their basket, creating new orders in the system.

Datastore Layer
The datastore is responsible for persisting the systems data.
The datastore encapsulates which technologies are used to achieve data persistence.
In my implementation I have used a SqlLite3 database to store data.
SqlLite3 was ideal for this task as it does not require the user to install a database on their machine.
The Datastore provides a simple interface of functions that can be found in the AccessLayer.py file.
Each function implements a type of CRUD(create,read,update,delete) operation.

I have used the Facade pattern to hide the complexities of the sqlLite3 database connection.
The class dbConnection creates a facade around the sqlLite3 connection class and provides conveniences such as automatically returning the inserted row id after an insert statement.
The use of Facade pattern hides the fact that sqlLite3 was used to implement the sql database and the same Facade could be used with a different sql library.

Business Layer
The business layer implements the classes identified during the system design phase.

I have chosen to make use of the Composite pattern in my implementation.
For example the Customer class uses the composite pattern to pass requests to fetch the customers orders to the Orders class.
The Orders class in turn turns to the database access layers to fulfill the request.

I have used the Adapter pattern to bridge the interface between the database layer and the business layer.
For example the StoreOrders class within the Orders module uses the orderArrToStoreOrder function to convert from the database type into the type the business layer can use.

I have made use of the Factory pattern for handling the creation and retrieval of many types of business objects.
For example the ProductListings class encapsulates the creation logic required to create ProductListing objects with data from the database.

I have made use of the Command pattern when completing the customers order.
The Basket class creates the order command. This order is then passed to the payment class which acts as the invoker.
The payment class can execute the order, placing the customers order and 'notifying' the sellers.

I have implemented the Payments method using an Inheritance structure.
Subclasses of the abstract PaymentMethod define the concrete implementations.
This design allows the Payment class to polymorphically call the chargeCustomer(amount) function without knowing exactly how it was implemented.
This design makes it easy to extended the system, adding new PaymentMethods without having to alter the Payment class.

Interface Layer
I have implemented the customer interface as a stack of states.
An interface state will present the user with options, and the option chosen by the user determines the next state to be instantiated.
Every state launched is added to the stack of states.
By implementing the interface with a stack I can return to the previous state at any time by popping the last state of the stack and running the new top state.
Each state must implement a 'run' function. This allows the interfaces Controller class to run the top state without knowing exactly what class is being called.

Tests
Testing Strategy
I have two types of tests for the system, BusinessLayer tests and Interface tests.
I wanted all of my tests to be independent of each other and not to cause any side effects that may interfere with the other tests.
To achieve this, before every test I reset the database ensuring it is empty.
I use a second database file for the testing, this ensures that running the tests will not affect data stored in the main system.

The BusinessLayer tests check the business objects correctly perform their functions and work together.
Testing the BusinessLayer also tests the Datastore layer as the BusinessLayer uses the Datastore Layer.
The business layer tests can be found in the Test/TestCase.py file.
My test strategy for these tests is to create and manipulate business objects. I then use other business objects to ensure that the right outcome was achieved.
I have defined the abstract class "TestCase", the interface of which all test cases must implement.
Since my test cases all implement the same interface I can iterate over a list of all test cases and polymorphically call each one.
The result of each test is printed to the output.

Here is an example of a test:
class AddSeller(TestCase):
    name = "AddSeller"
    def run(self):
        # create Sony seller
        sony = Seller("Sony")
        sellers = Sellers()
        sellers.addVendor(sony)
        #verify the seller has been stored
        seller = sellers.searchVendorByName("Sony")
        if seller.getName() == 'Sony':
            return True

My Interface test tests the command line interface.
This test is a full system test and tests the integration of all the layers.
The interface test executes a set of predefined 'user' inputs.
Because the inputted commands are known the result of the commands is also known and therefore can be verified.
To verify the commands have the correct impact on the system I access the business layer and check it is in the correct state after my 'fake' user inputs have been executed.

Here is an example of a sequence of inputs that creates a new user and navigates to the product search state:
"customer","n","Adam","search products"

Usage

For an example of usage please view the file: example-usage.txt

If you want to reset the data in the system uncomment the following line in main.py:
#resetData()
Uncommenting this lines before running the system will clear the database.
Re-comment the lines so the database is not cleared on the next run.

Note: Promotional codes are not stored in the database so will disappear when the system is restarted.

When running the interface you can type 'back' at any time to return to the previous state

Notes:

To demonstrate the system in action I have added a number of entitys to the system.

The system currently has a customer called Bob, a Seller called Tesco and three products.

The three products are a Phone, Car and Watch.

If you login as Bob you can search for the above products by name.

In Bobs account you can also 'view history' to see Bobs order history. 