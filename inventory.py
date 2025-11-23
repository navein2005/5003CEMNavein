# --- Step 1: Define Data Structures ---

class Product:
    """
    Represents a single product in the baby shop.
    This is the 'entity class' required by the assignment.

    Attributes:
        product_id (str): The unique identifier for the product (e.g., "P101").
                          This will be used as the KEY for our hash table.
        name (str): The display name of the product (e.g., "Baby Diapers").
        price (float): The retail price of the product.
        quantity (int): The current stock level.
    """

    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id  # str: Using string for flexibility (e.g., 'SKU-1001')
        self.name = name  # str: Product name
        self.price = price  # float: Allows for decimal values (e.g., 29.99)
        self.quantity = quantity  # int: Stock must be a whole number

    def __str__(self):
        """A helper method to easily print the product's details."""
        return f"ID: {self.product_id}, Name: {self.name}, Price: ${self.price:.2f}, Stock: {self.quantity}"



# --- THIS CLASS IS NOW UN-INDENTED ---
class Node:
    """
    Represents one link in our 'separate chain' (a linked list).
    Each node stores a key-value pair and a pointer to the next node.
    """

    def __init__(self, key, value):
        self.key = key  # The product_id
        self.value = value  # The entire Product object
        self.next = None  # The pointer to the next Node in the chain (or None)


# --- Step 2: Implement the Hash Table Class ---

# --- THIS CLASS IS NOW UN-INDENTED ---
class HashTable:
    """
    Implements a Hash Table using Separate Chaining for collision resolution.
    It will store Product objects, using the product_id as the key.
    """

    def __init__(self, size):
        """
        Initializes the hash table.

        Args:
            size (int): The number of buckets in the hash table.
        """
        self.size = size
        # Create an empty list (our buckets) of the given size
        # Each bucket is initialized to None

        self.buckets = [None] * self.size
        print(f"Hash Table created with {self.size} buckets.")

    def _hash(self, key):
        """
        A private helper method to calculate the bucket index for a given key.

        Args:
            key: The key to hash (e.g., "P101").

        Returns:
            int: The calculated bucket index (from 0 to self.size - 1).
        """
        # Use Python's built-in hash() function
        hash_value = hash(key)
        # Use the modulo operator to get an index within our bucket list size
        index = hash_value % self.size
        return index

    def insert(self, key, value):
        """
        Inserts a key-value pair into the hash table.
        Handles collisions by appending to the chain (linked list).

        Args:
            key: The key (product_id).
            value: The value (the entire Product object).
        """
        # 1. Find the bucket index
        index = self._hash(key)

        # 2. Create the new node to store the key and value
        # Now this will correctly find the 'Node' class
        new_node = Node(key, value)

        # 3. Check if the bucket at this index is empty
        if self.buckets[index] is None:
            # If empty, place the new node here
            self.buckets[index] = new_node
            # print(f"Inserted {key} at index {index} (empty bucket)")
        else:
            # 4. If not empty (a collision!), traverse the linked list
            current = self.buckets[index]

            # Check for duplicate keys. If found, update the existing entry.
            while current:
                if current.key == key:
                    # Found a duplicate key, update its value
                    current.value = value
                    # print(f"Updated {key} at index {index}")
                    return  # Exit the function

                # If we are at the end of the list, prepare to append
                if current.next is None:
                    break  # Exit loop to append

                # Move to the next node
                current = current.next

            # 5. We reached the end of the list (current.next is None)
            # Add the new node to the end of the chain
            current.next = new_node
            # print(f"Inserted {key} at index {index} (collision)")

    def search(self, key):
        """
        Searches for a value in the hash table using its key.

        Args:
            key: The key (product_id) to search for.

        Returns:
            Product: The Product object if found, otherwise None.
        """
        # 1. Find the bucket index
        index = self._hash(key)

        # 2. Get the head of the chain (if any) at that bucket
        current = self.buckets[index]

        # 3. Traverse the linked list in the bucket
        while current:
            # Check if the current node's key matches the search key
            if current.key == key:
                # Found it! Return the value (the Product object)
                return current.value

            # If not a match, move to the next node in the chain
            current = current.next

        # 4. If the loop finishes (current is None), the key was not found
        return None


# --- Step 4: Performance Comparison (Q1.4) ---

import time  # To measure execution time in nanoseconds
import random  # To generate random data
import string  # To help create random strings


def search_array(array, key):
    """
    A simple function to search for a product in a 1D array (list).
    This simulates the 'one-dimensional array' search.
    """
    for product in array:
        if product.product_id == key:
            return product
    return None


def run_performance_test():
    """
    Runs the performance comparison between HashTable and Array search.
    This function will be called from our main menu.
    """
    print("\n--- Running Performance Comparison ---")

    NUM_PRODUCTS = 5000  # You can change this number (e.g., 1000, 5000)
    TABLE_SIZE = 100  # Size of the hash table (to ensure collisions)

    product_data = []  # To hold our generated product objects

    # 1. Generate a large set of test data
    print(f"Generating {NUM_PRODUCTS} product records...")
    for i in range(NUM_PRODUCTS):
        # Create a random product ID (e.g., "P_aB1xY")
        rand_id = "P_" + ''.join(random.choices(string.ascii_letters + string.digits, k=5))

        # Create the product
        product = Product(
            product_id=rand_id,
            name="Test Product",
            price=10.0,
            quantity=1
        )
        product_data.append(product)

    # We will search for the VERY LAST item added.
    # This is the "worst-case" scenario for the array search.
    search_key = product_data[-1].product_id
    print(f"Test complete. Will search for key: {search_key}\n")

    # --- 2. Test Hash Table Performance ---
    print("Testing Hash Table...")
    hash_table = HashTable(size=TABLE_SIZE)

    # Populate the hash table
    for product in product_data:
        hash_table.insert(product.product_id, product)

    # Time the search
    ht_start_time = time.time_ns()
    hash_table.search(search_key)
    ht_end_time = time.time_ns()

    ht_duration = ht_end_time - ht_start_time
    print(f"Hash Table Search Time: {ht_duration} nanoseconds")

    # --- 3. Test Array (List) Performance ---
    print("\nTesting 1D Array (List)...")
    array_storage = []

    # Populate the array
    for product in product_data:
        array_storage.append(product)

    # Time the search
    arr_start_time = time.time_ns()
    search_array(array_storage, search_key)
    arr_end_time = time.time_ns()

    arr_duration = arr_end_time - arr_start_time
    print(f"Array Search Time: {arr_duration} nanoseconds")

    # --- 4. Print Analysis ---
    print("\n--- Analysis ---")
    print(f"Hash Table was {arr_duration / ht_duration:.2f} times faster.")

# --- Step 3: Build the Inventory System (Q1.2 & Q1.3) ---

def main():
    """
    The main function to run the Baby Shop Inventory System.
    """

    # 1. Initialize the storage system
    # We choose a size for the hash table. 10 is good for this example.
    # Now this will correctly find the 'HashTable' class
    inventory = HashTable(size=10)

    # 2. Insert pre-defined records (as required by Q1.2)
    print("\n--- Pre-populating inventory ---")

    # Create some Product objects
    p1 = Product(product_id="D101", name="Premium Diapers (Size 3)", price=29.99, quantity=100)
    p2 = Product(product_id="F202", name="Organic Baby Formula", price=35.50, quantity=50)
    p3 = Product(product_id="W303", name="Sensitive Baby Wipes (Pack of 5)", price=14.99, quantity=200)
    p4 = Product(product_id="T404", name="Giraffe Teether Toy", price=8.99, quantity=75)

    # Insert them into the hash table
    inventory.insert(p1.product_id, p1)
    inventory.insert(p2.product_id, p2)
    inventory.insert(p3.product_id, p3)
    inventory.insert(p4.product_id, p4)

    print("Pre-population complete.\n")

    # 3. Create the command-line menu (as required by Q1.3)
    while True:
        print("========================================")
        print("  Baby Shop Inventory Management System ")
        print("========================================")
        print("1. Add New Product (Insert)")
        print("2. Search for Product")
        print("3. Run Performance Test (Q1.4)")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            # --- INSERT Function ---
            print("\n--- Add New Product ---")
            try:
                # Get input from the user
                p_id = input("Enter Product ID: ")
                p_name = input("Enter Product Name: ")
                p_price = float(input("Enter Price: "))
                p_quantity = int(input("Enter Quantity: "))

                # Create the new product object
                new_product = Product(p_id, p_name, p_price, p_quantity)

                # Insert it into the hash table
                inventory.insert(new_product.product_id, new_product)

                print(f"\nSUCCESS: Product '{new_product.name}' added to inventory.")

            except ValueError:
                print("\nERROR: Invalid input. Price must be a number and Quantity must be an integer.")
            except Exception as e:
                print(f"\nAn error occurred: {e}")

        elif choice == '2':
            # --- SEARCH Function ---
            print("\n--- Search for Product ---")
            key_to_search = input("Enter the Product ID to search for: ")

            # Call the search method
            found_product = inventory.search(key_to_search)

            if found_product:
                print("\n--- Product Found ---")
                print(found_product)  # Uses the __str__ method from the Product class
            else:
                print(f"\n--- No Product Found ---")
                print(f"No product with ID '{key_to_search}' exists in the inventory.")

        elif choice == '3':
            run_performance_test()

        elif choice == '4':
            # --- EXIT (changed to '4') ---
            print("\nExiting inventory system. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.")

        input("\nPress Enter to continue...")  # Pause screen


# This standard Python line checks if the script is being run directly
# If so, it calls the main() function.
if __name__ == "__main__":
    main()