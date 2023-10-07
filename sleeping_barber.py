# Based on code from https://github.com/Nohclu/Sleeping-Barber-Python-3.6-/blob/master/barber.py
import time
import random
import threading
from queue import Queue

CUSTOMERS_SEATS = 15        # Number of seats in BarberShop
BARBERS = 3                # Number of Barbers working
EVENT = threading.Event()   # Event flag, keeps track of Barber/Customer interactions
global Earnings
global SHOP_OPEN


class Customer(threading.Thread):       # Producer Thread
    def __init__(self, queue):          # Constructor passes Global Queue (all_customers) to Class
        threading.Thread.__init__(self)
        self.queue = queue
        self.rate = self.what_customer()

    @staticmethod
    def what_customer():
        customer_types = ["adult", "senior", "student", "child"]
        customer_rates = {"adult": 16,
                          "senior": 7,
                          "student": 10,
                          "child": 7}
        t = random.choice(customer_types)
        print(t + " rate.")
        return customer_rates[t]

    def run(self):
        if not self.queue.full():  # Check queue size
            EVENT.set()  # Sets EVENT flag to True i.e. Customer available in the Queue
            EVENT.clear()  # Alerts Barber that their is a Customer available in the Queue
        else:
            # If Queue is full, Customer leaves.
            print("Queue full, customer has left.")

    def trim(self):
        print("Customer haircut started.")
        a = 3 * random.random()  # Retrieves random number.
        time.sleep(a)
        payment = self.rate
        # Barber finished haircut.
        print("Haircut finished. Haircut took {}".format(a))
        global Earnings
        Earnings += payment


class Barber(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        global SHOP_OPEN
        while SHOP_OPEN:
            customer = self.queue.get()
            customer.trim()
            self.queue.task_done()


def wait():
    time.sleep(1 * random.random())


if __name__ == '__main__':
    Earnings = 0
    SHOP_OPEN = True
    barbers = []
    all_customers = Queue(CUSTOMERS_SEATS)  # A queue of size Customer Seats

    for b in range(BARBERS):
        b=Barber(all_customers)
        # Makes the Thread a super low priority thread allowing it to be terminated easier
        b.daemon = True
        b.start()   # Invokes the run method in the Barber Class
        # Adding the Barber Thread to an array for easy referencing later on.
        barbers.append(b)
    for c in range(10):  # Loop that creates infinite Customers
        print("----bahman",c)
        # Simple Tracker too see the qsize (NOT RELIABLE!)
        print(all_customers.qsize())
        wait()
        c = Customer(all_customers)  # Passing Queue object to Customer class
        all_customers.put(c)    # Puts the Customer Thread in the Queue
        c.start()
    all_customers.join()    # Terminates all Customer Threads
    print("Barbers payment total: " + str(Earnings))
    SHOP_OPEN = False
    for barber in barbers:
        barber.join()    # Terminates all Barbers
        # Program hangs due to infinite loop in Barber Class, use ctrl-z to exit.
