import os,sys,datetime,re,psycopg2,matplotlib
import matplotlib.pyplot as plt

class Restaurent :
    
    food_items={}   #{item number : price}
    ordered_item={} #{item name : quantity}

    def __init__(self) :
        
        self.dbname = "RestaurentManagementSystem"
        self.user = "postgres"
        self.password = "**********" # enter your pswd here
        self.host = "localhost"
        self.port = 5432

        try :
            # Establishing the connection
            self.conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host ,port=self.port)

            # Creating a cursor object using the connection
            self.cur = self.conn.cursor()

            # Execute a query to fetch all menu items
            self.cur.execute("SELECT * FROM menu_items")

            # Fetch all rows from the query
            self.rows = self.cur.fetchall() # returns list of tuples

            for row in self.rows:
                item_number, item_name, price = row
                Restaurent.food_items[item_number] = price

            self.menu()

        except Exception as e :
                print(f'Error : {e}')
                
           
    def refresh_database(self):
            
            Restaurent.food_items={}

            # Establishing the connection
            self.conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host ,port=self.port)

            # Creating a cursor object using the connection
            self.cur = self.conn.cursor()

            # Execute a query to fetch all menu items
            self.cur.execute("SELECT * FROM menu_items")

            # Fetch all rows from the query
            self.rows = self.cur.fetchall()

            for row in self.rows:
                item_number, item_name, price = row
                Restaurent.food_items[item_number] = price


    def get_item_name_by_id(self,item_id):

        try :

            query = "SELECT item_name FROM menu_items WHERE id = %s;"
            self.cur.execute(query, (item_id,)) # accepts tuple as its 2nd parameter

            result = self.cur.fetchone()
            
            if result :
                return result[0]
        except Exception as e :
            print(f'Error :{e}')


    def get_item_price_by_name(self,item_name) :

        try :
            query = "SELECT price FROM menu_items WHERE item_name = %s;"
            self.cur.execute(query, (item_name,))
            result = self.cur.fetchone()

            if result :
                return result[0]
            
        except Exception as e :
            print(f'Error : {e}')


    def order_food(self) :

        self.view_data()

        while True :
            
            try :
                ch=input("\n\nEnter food item number \nor\ntype exit to go back to the Main Menu :")

                if ch.lower()=='exit' :
                    print("\n\nTaking you back to the Main Menu")
                    self.menu()
                    break
                elif self.get_item_name_by_id(int(ch)) in self.ordered_item :
                    qnty=0
                    try : 
                        qnty=int(input("Please Enter the Quantity :"))
                        Restaurent.ordered_item[self.get_item_name_by_id(int(ch))]=qnty
                        print(f'Item :{self.get_item_name_by_id(int(ch))} Qnty:{qnty} ordered successfully.')
                    except :
                        print(f'Error : Quantity cant be in decimal')
                    if qnty>0 :
                        self.ordered_item[self.get_item_name_by_id(int(ch))]+=qnty
                else :
                    if int(ch) in Restaurent.food_items :
                        try : 
                            qnty=int(input("Please Enter the Quantity :"))
                            Restaurent.ordered_item[self.get_item_name_by_id(int(ch))]=qnty
                            print(f'Item :{self.get_item_name_by_id(int(ch))} Qnty:{qnty} ordered successfully.')
                        except :
                            print(f'Error : Quantity cant be in decimal')
                    else :
                        print("Please enter valid food item number.The item number which you had selected isn't available!!")
            except Exception as e :
                print("Only numbers and exit is allowed")
        

    def view_data(self) :

        if self.rows:
            print(f"{'Item Number':<12} {'Item Name':<30} {'Price':>6}")
            print('-' * 48)
        
        # Loop through each row and print formatted output
            for row in self.rows:
                item_number, item_name, price = row
                print(f"{item_number:<12} {item_name:<30} Rs. {price:>6}")
        else:
            print("No items found in the database.")


    def generate_bill(self) :

        total_price=0
        
        if Restaurent.ordered_item :
            print(Restaurent.ordered_item)

            print(format('','-^70'))
            for i,j in Restaurent.ordered_item.items() :
                print(f'{i:20} x{j}   -Rs per item.{self.get_item_price_by_name(i):10} Total:-{self.get_item_price_by_name(i)*j:15}')
                total_price+=self.get_item_price_by_name(i)*j
            print(format('','-^70'))
            print(format('Total Price :','^20'),total_price)


            while True :
                print('''\n\ndo you want to make any changes ?
                1) To edit cart
                2) Pay and generate Bill
                3) Main Menu
                ''')

                ch=input("Enter your choice :")

                if ch=='1' :
                    p=input("Enter product name which you want to edit :")
                    p=p.title().strip()

                    if p in Restaurent.ordered_item.keys() :

                        while True :
                            print('''Do you want to edit quantity or want to remove item ?
                            1) remove item
                            2) Edit Quantity      
                            ''')

                            opt=input("Enter you choice :")

                            if opt=='1' :
                                del Restaurent.ordered_item[p]
                                print("Item removed successfully")
                                break

                            elif opt=='2' :

                                while True :
                                    try :
                                        new_qnt=int(input("Enter new Quantity :"))
                                        break
                                    except :
                                        print(f'Quantity cant be in decimal')
                                Restaurent.ordered_item[p]=new_qnt
                                print("Quantity Updated Successfully")
                                break

                            else :
                                print("Enter valid choice")
                    else :
                        print(f'Item :{p} isnt available in your cart')
                        
                elif ch=='2' :

                    def get_valid_mobile_number():
                         while True:
                            mob = input("Enter mobile number (10 digits without spaces or any other characters): ")
                            if re.fullmatch(r"\d{10}", mob):
                                return mob
                            else:
                                print("Invalid format. Please ensure the number is exactly 10 digits long.")

                    mob = get_valid_mobile_number()

                    bill_id=datetime.datetime.now().strftime("%Y_%m_%d %H-%M-%S")

                    bill_content=f'''Bill ID : {bill_id}
Date    : {datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")}
Mobile  : {mob}

----------------------------------------------------------------------------------                               
ITEM NAME                 Qnty       Unit Price      Total Price
----------------------------------------------------------------------------------
'''
                        
                    for i,j in Restaurent.ordered_item.items() :
                            bill_content+=f'''
{i:20} {j:8} {self.get_item_price_by_name(i):15} {self.get_item_price_by_name(i)*j:15} 
'''

                    bill_content+=f'''
----------------------------------------------------------------------------------
                          Gst : {0.18*total_price}
                          Total Price : {total_price + 0.18*total_price}
'''
                    print(bill_content)

                    bill_name=mob+' '+bill_id+'.txt'

                    try :
                        os.chdir("D:\\College Python\\Restaurent Management System\\Bill Records")
                        with open(bill_name,'w') as f :
                            f.write(bill_content)

                    except Exception as e:
                        print(e)

                    

                    print("Thank you for dining in!! Visit Again")

                    data_to_insert = []
                    current_date = datetime.datetime.now().strftime("%Y-%m-%d")  # Use current date for sale_date

                    for item_name, quantity in Restaurent.ordered_item.items():
                        unit_price = self.get_item_price_by_name(item_name)
                        total_price_for_item = unit_price * quantity
                        data_to_insert.append((current_date, item_name, quantity, total_price_for_item))



                    try :

                        # SQL query to insert data
                        query = """
                        INSERT INTO food_sales (sale_date, food_item_name, quantity_sold, price)
                        VALUES (%s, %s, %s, %s)
                        """

                        # Executing the query with multiple sets of data
                        self.cur.executemany(query, data_to_insert)

                        # Committing the transaction to the database
                        self.conn.commit()
                    except Exception as e:
                        print(f"An error occurred: {e}")
                    
                    finally :
                        if self.cur:
                            self.cur.close()
                        if self.conn:
                            self.conn.close()
                    # Closing the cursor and connection
                    
                    sys.exit(0)

                elif ch=='3' :
                    self.menu()
                    break
                
                else :
                    print("Enter valid choice only")

        else :
            print("Please add food items in your cart to Generate Bill")
            self.menu()
        


    def menu(self) :
        
        while True :
            
            print(format('','-<18'),format('Restaurant Management System','^40'),format('','->18'))
            print('''\n\n\nPlease select your choice :
                  
        1)Order Food
        2)See Your Cart
        3)Make Payment & Generate Bill
        4)See Monthly Sales
        5)Add product
        6)Remove product
        7)Update price
        8)Exit\n\n
        ''')
            
            try :
                choice = int(input("Enter your choice :"))
            except Exception as e :
                print("Only digits 1-8 are allowed")
                self.menu()
                
            if choice==1 :
                self.order_food()

            elif choice==2 :
                if Restaurent.ordered_item :
                    print(format('','=^50'))
                    print("\nItmes available in your cart is :\n\n")
                    for i,j in Restaurent.ordered_item.items() :
                        print(f'{i:20}  x{j} -{self.get_item_price_by_name(i)*j:15}')
                    print(format('','=^50'))
                else :
                    print("You hadnt added anything yet\n\n\n\n\n\n")
                
                self.menu()

            elif choice==3 :
                self.generate_bill()

            elif choice==4 :
               
               try :

                    query = """
        SELECT 
            EXTRACT(YEAR FROM sale_date) AS sale_year, 
            EXTRACT(MONTH FROM sale_date) AS sale_month, 
            food_item_name, 
            SUM(quantity_sold) AS total_quantity,
            SUM(price) AS total_cost
        FROM 
            food_sales
        GROUP BY 
            sale_year, sale_month, food_item_name
        ORDER BY 
            sale_year, sale_month, food_item_name;
        """
                    
                    # Executing the query
                    self.cur.execute(query)

                    # Fetching all rows
                    rows = self.cur.fetchall()
                    
                    data = {} # empty dict

                    for row in rows:
                        year_month = f"{int(row[0])}-{int(row[1]):02d}"  # Format: YYYY-MM
                        if year_month not in data:
                            data[year_month] = {} # nested dict inside data 
                        data[year_month][row[2]] = (row[3],row[4])  # {food_item_name : total_quantity,total_cost}

                    # print(data)
                    # {'2024-03': {'Pav Bhaji': (2, 220)}


                    def get_month_year_input():
                        pattern = r'^\d{4}-(0[1-9]|1[0-2])$'
                        while True:
                            user_input = input("Enter a date in YYYY-MM format: ")
                            if re.match(pattern, user_input):
                                return user_input
                            else:
                                print("Invalid format. Please enter the date in YYYY-MM format.")

                    year_month=get_month_year_input()

                    if year_month in sorted(data.keys()):
                        # Extracting food items, their quantities, and total costs
                        food_items = [i for i in data[year_month].keys()]
                        quantities = [i[0] for i in data[year_month].values()]  # Total quantities
                        total_costs = [i[1] for i in data[year_month].values()]  # Total costs
                        monthly_cost=sum(i for i in total_costs)

                        # Preparing custom labels: 'Item Name - RsTotalCost'
                        labels = [f"{item} - Rs{cost:.2f}" for item, cost in zip(food_items, total_costs)]

                        def get_n_color_names(n):
                            color_names = list(matplotlib.colors.cnames.keys())  # Get a list of color names
                            return color_names[:n]  # Return the first n color names
                        
                        colors=get_n_color_names(len(food_items))

                        # Create bar plot
                        plt.figure(figsize=(10, 6))
                        plt.bar([i for i in food_items], quantities,tick_label=labels,color=colors)
                        plt.xlabel('Food Item and Total Price')
                        plt.ylabel('Quantity Sold')
                        plt.title(f'Sales Data for {year_month} : Total income-{monthly_cost}')
                        plt.xticks(rotation=90)
                        plt.tight_layout() # Adjusts the plots to fit into the figure area.
                        plt.show()
                        
                    else:
                        print(f'No data exist for {year_month}')
                    

               except Exception as e :
                   print(f"An error occurred: {e}")
                   

            elif choice==5 :

                print("Your current data is :")
                self.view_data()
                print('\n\n')

                def insert_if_not_exists(item_name, item_price):

                    query="""
                    INSERT INTO menu_items (item_name, price)
                    SELECT %s, %s
                    WHERE NOT EXISTS (
                        SELECT 1 FROM menu_items WHERE item_name = %s
                    );
                    """

                    self.cur.execute(query,(item_name, item_price, item_name))

                    if self.cur.rowcount > 0:
                        print(f"Item '{item_name}' inserted successfully.")
                        self.conn.commit()
                        self.refresh_database()
                    else:
                        print(f"Item '{item_name}' already exists. No new record added.")

                pattern = r'^[a-zA-Z]+(?:\s+[a-zA-Z]+)*$'
                while True :
                    name=input("Enter item name or type exit to return to main menu:")

                    if name.lower()=='exit' :
                        print("\n\nTaking you back to the Main Menu")
                        self.menu()
                        break
                    else :
                        if re.match(pattern, name):
                            break
                        else :
                            print("Only alphabets are allowed ...")

                name=name.title().strip()
                price=0
                while True :
                    try :
                        price=float(input("Enter Price :"))
                        break
                    except :
                        print(f'Price must be in number')

                insert_if_not_exists(name,price)

            elif choice==6 :

                print("Your current data is :")
                self.view_data()
                print('\n\n')

                def remove_product_by_item_number(item_number):
                    query = "DELETE FROM menu_items WHERE id = %s;"

                    self.cur.execute(query,(item_number,)) #to make it tuple

                    if self.cur.rowcount > 0:
                        print(f"Product with item number {item_number} removed successfully.")
                        self.conn.commit()
                        self.refresh_database()
                    else:
                        print(f"No product found with item number {item_number}. No changes made.")

                no=0

                while True :
                    try :
                       no=input("Enter item number to delete or type exit to return to main menu:")
                       if no.lower()=='exit' :
                        print("\n\nTaking you back to the Main Menu")
                        self.menu()
                        break
                       else :
                        no=int(no)
                        break
                    except :
                        print("Item number must be non-decimal number ...")

                remove_product_by_item_number(no)
                

            elif choice==7 :

                print("Your current data is :")
                self.view_data()
                print('\n\n')

                def update_item_price(item_number, new_price):

                    query = "UPDATE menu_items SET price = %s WHERE id = %s"

                    self.cur.execute(query, (new_price, item_number))

                    if self.cur.rowcount > 0:
                        print(f"Successfully updated the price of item number {item_number}.")
                        self.conn.commit()
                        self.refresh_database()
                    else:
                        print(f"No item found with item number {item_number}. No update performed.")

                no=0
                price=0
                while True :
                    try :
                       no=input("Enter item number to update or type exit to return to main menu:")
                       if no.lower()=='exit' :
                        print("\n\nTaking you back to the Main Menu")
                        self.menu()
                        break
                       else :
                        no=int(no)   
                        break
                    except :
                        print("Item number must be non-decimal number ...")
                while True :
                    try :
                        price=float(input("Enter Price :"))
                        break
                    except :
                        print(f'Price must be in number')

                update_item_price(no,price)


            elif choice==8 :
                print('\n\nGoodBye!! Visit again.')
                self.cur.close()
                self.conn.close()
                sys.exit(0)
            else :
                print("Enter valid choice only")


obj = Restaurent()


    
'''
CREATE TABLE food_sales (
    sale_date DATE NOT NULL,
    food_item_name VARCHAR(255) NOT NULL,
    quantity_sold INT NOT NULL,
    price NUMERIC(10, 2) NOT NULL
);

CREATE TABLE menu_items (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    price INTEGER NOT NULL
);

'''
