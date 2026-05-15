# Connect to MySQL database.
import mysql.connector
from datetime import datetime, date, timedelta
import calendar
connection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'B2tydung',
    database = 'hotel_management_system'
)
cursor = connection.cursor()

def main(): #giao dien chinh cua phan mem truy cap
    print("This is the hotel management system. Please select an option:")
    while True:
        print("")
        print("1. Show available rooms")
        print("2. Create a booking")
        print("3. Show all bookings")
        print("4. Update individual info")
        print("5. Show individual booking")
        print("6. Print receipt")
        print("7. Calculate monthly revenue")
        print("8. Calculate yearly revenue")
        print("9. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            show_rooms()
        elif choice == "2":
            create_booking()
        elif choice == "3":
            show_all_bookings()
        elif choice == "4":
            update_individual_info()
        elif choice == '5':
            show_individual_booking()
        elif choice == '6':
            receipt()
        elif choice == '7':
            revenue_by_month()
        elif choice == '8':
            total_revenue_in_year()
        elif choice == "9":
            connection.close()
            print("Thank you for using the hotel management system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def show_rooms(): #cho xem cac phong khach san
    cursor.execute("SELECT * FROM rooms")
    rooms = cursor.fetchall()
    print("All rooms:")
    #tao bang
    print(f"{'Room':<10} {'Type':<15} ")
    for room in rooms:
        print(f"{room[0]:<10} {room[1]:<15} ")

def show_all_bookings(): #cho xem tat ca cac booking
    cursor.execute("""SELECT * from all_booking""")
    bookings = cursor.fetchall()
    print("All bookings:")
    #tao bang
    print(f"{'Booking ID':<15}{'Name':<10}{'Room':<10}{'Room Type':<15}{'Check-in':<15}{'Check-out':<15}")
    for booking in bookings:
        check_in = str(booking[4])
        check_out = str(booking[5])
        print(f"{booking[0]:<15}{booking[1]:<10}{booking[2]:<10}{booking[3]:<15}{check_in:<15}{check_out:<15}")
        
def show_individual_booking(): #truy cap vao booking cua tung khach hang
    name = input("Enter customer name: ")
    cursor.execute("""SELECT * from all_booking
                   where customer_name = %s 
                   """, (name,))
    bookings = cursor.fetchall()
    if bookings:
        print(f"Customer: {name}")
        print(f"{'Booking ID':<15}{'Name':<10}{'Room':<10}{'Room Type':<15}{'Check-in':<15}{'Check-out':<15}")
        for booking in bookings:
            check_in = str(booking[4])
            check_out = str(booking[5])
            print(f"{booking[0]:<15}{booking[1]:<10}{booking[2]:<10}{booking[3]:<15}{check_in:<15}{check_out:<15}")
    else:
        print("Customer is not found.")
    return name

def update_individual_info(): #thay doi thong tin dat phong cua khach hang
    while True: 
        show_individual_booking()
        select_bookingID = input("Please choose a booking id from the list to update information: ")
        cursor.execute('''select * from all_booking where booking_id = %s''', (select_bookingID,))
        bookingID = cursor.fetchall()
        if bookingID:
            print(f"{'Booking ID':<15}{'Name':<10}{'Room':<10}{'Room Type':<15}{'Check-in':<15}{'Check-out':<15}")
            for bookingid in bookingID:
                check_in = str(bookingid[4])
                check_out = str(bookingid[5])
                print(f"{bookingid[0]:<15}{bookingid[1]:<10}{bookingid[2]:<10}{bookingid[3]:<15}{check_in:<15}{check_out:<15}")
            selected_booking = bookingID[0]
            booking_id = selected_booking[0]
            check_in_old = selected_booking[4]
            check_out_old = selected_booking[5]
            break
        else:
            print("Booking ID does not exist. Please choose again.")
    print("To update customer/room/booking information, please select:")
    while True:
        print("1. Customer name")
        print("2. Room number")
        print("3. Booking date")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1": #doi ten khach hang
            new_name = input("Enter customer new name: ")
            cursor.execute("""Update customers
                    set customer_name = %s
                    where customer_id = (select customer_id from bookings where booking_id =%s)""", (new_name, booking_id))
            connection.commit()
            print("Customer name updated successfully.")
        elif choice == "2": #doi phong cho khach
            check_room = '''select room_number, room_type from rooms
                            where room_number not in (select room_number from bookings
                            where (%s < check_out_date and %s > check_in_date)
                            and booking_id <> %s)'''
            cursor.execute(check_room, (check_in_old, check_out_old, booking_id))
            availableROOM = cursor.fetchall()
            if not availableROOM:
                print("Sorry, there is no other room during this time.")
                return
            print(f"Available room from {check_in_old} to {check_out_old}")
            for room in availableROOM:
                print(f"{room[0]} - {room[1]}")
            while True:
                new_room = input("Enter a new room from the list: ")
                if new_room in [str(room[0]) for room in availableROOM]:
                    break
                else: 
                    print("Invalid room selection. Please try again.")
            cursor.execute("""Update bookings
                            set room_number = %s
                            where booking_id = %s""", (new_room, booking_id))
            connection.commit()
            print("Room updated successfully.")
        elif choice == "3":  #doi ngay check in, check out cho khach
            while True:
                try:
                    check_in_date = input("Enter new check-in date (YYYY-MM-DD): ")
                    checkin = datetime.strptime(check_in_date, "%Y-%m-%d").date()
                    check_out_date = input("Enter new check-out date (YYYY-MM-DD): ")
                    checkout = datetime.strptime(check_out_date, "%Y-%m-%d").date()
                    if checkin >= checkout: #dam bao la khach ko nhap sai ngay
                        print("Check-out date must be after check-in date. Please try again.")
                    else:
                        break
                except ValueError: #dam bao khach ko nhap sai hinh thuc cua ngay
                    print("Invalid format of date. Please enter in form (YYYY-MM-DD).")
            cursor.execute("""UPDATE bookings
                SET check_in_date = %s,
                check_out_date = %s
                WHERE booking_id = %s""", (check_in_date, check_out_date, select_bookingID))
            connection.commit()
            print("Check-out date updated successfully.")
        elif choice == "4":
            print("Thank you for updating.")
            break
        else:
            print("Invalid choice. Please try again.")

def create_booking(): #dat phong
    print("Customers list:")
    cursor.execute("select * from customers")
    customers = cursor.fetchall()
    if customers:
        for customer in customers:
            print(f"{customer[0]} - {customer[1]}")
    else:
        print("No customer found.")
    print("If customer existed, enter customer ID. " \
    "If customer is not found, type 'new' to add new customer")
    while True:
        choice = input("Your choice: ").lower()
        if choice == 'new':
            name = input("Enter customer name: ")
            cursor.execute('''select customer_id from customers where customer_name = %s''', (name,))
            existing_name = cursor.fetchone()
            if existing_name:
                print("Customer already exists.")
                customer_id = existing_name[0]
            else:
                cursor.execute('''insert into customers (customer_name)
                        values (%s)''', (name,))
                connection.commit()
                customer_id = cursor.lastrowid
                print(f"New customer is created with ID: {customer_id} - {name}")
            break
        else:
            cursor.execute('''Select * from customers where customer_id = %s''', (choice,))
            result = cursor.fetchone()
            if result:
                customer_id = result[0]
                break
            else: print("Customer not found.")
            customer_id = choice
    while True:
        try:
            check_in_date = input("Enter check-in date (YYYY-MM-DD): ")
            checkin = datetime.strptime(check_in_date, "%Y-%m-%d").date()
            check_out_date = input("Enter check-out date (YYYY-MM-DD): ")
            checkout = datetime.strptime(check_out_date, "%Y-%m-%d").date()
            if checkin >= checkout:
                print("Check-out date must be after check-in date. Please try again.")
            else:
                break
        except ValueError:
            print("Invalid format of date. Please enter in form (YYYY-MM-DD).")
    select_available_room_query = '''select room_number, room_type from rooms
                                        where room_number not in 
                                        (select room_number from bookings 
                                        where (%s < check_out_date) and (%s > check_in_date))'''
    cursor.execute(select_available_room_query, (checkin, checkout))
    available_room = cursor.fetchall()
    if not available_room:
        print("There is no available room during this time.")
        return
    print(f"Available rooms from {checkin} to {checkout}")
    for room in available_room:
        print(f"Room: {room[0]} - Type: {room[1]}")
    while True:
        room_number = input("Choose a room from the list: ")
        if room_number in [str(room[0]) for room in available_room]:
            break
        else: print("Invalid room selection. Please try again.")
    cursor.execute('''Insert into bookings 
                   (customer_id, room_number, check_in_date, check_out_date)     
                   values (%s, %s, %s, %s)''', (customer_id, room_number, checkin, checkout))
    connection.commit()
    print(f"Booking created successfully for room {room_number} from {checkin} to {checkout}.")

def receipt():
    while True:
        name = show_individual_booking()
        print("Please select customer booking id to print out receipt of customer's stay.")
        bookingid = input("Booking id: ")
        cursor.execute('''select * from total_money where booking_id = %s''', (bookingid,))
        receipts = cursor.fetchall()
        if receipts:
            print(f"Customer {name}'s receipt:")
            for receipt in receipts:
                print(f"Booking ID: {receipt[0]}\n"
                    f"Room number: {receipt[1]}\n"
                    f"Room type: {receipt[2]}\n"
                    f"Price per night: ${str(receipt[3])}/night\n"
                    f"Chek in date: {str(receipt[4])}\n"
                    f"Check out date: {str(receipt[5])}\n"
                    f"Staying duration: {str(receipt[6])} days\n"
                    f"Total amount: ${str(receipt[7])}")
            print("Thank you!")
            break
        else:
            print("Wrong booking ID. Please try again.")

def revenue_by_month():
    cursor.execute('''select booking_id, room_number, price_per_night,
                   check_in_date, check_out_date from total_money''')
    show_bookings = cursor.fetchall()
    print("All bookings:")
    print(f"{'Booking ID':<15}{'Room':<10}{'Price/night($)':<20}{'Check-in':<15}{'Check-out':<15}")
    for show_booking in show_bookings:
        check_in = str(show_booking[3])
        check_out = str(show_booking[4])
        print(f"{show_booking[0]:<15}{show_booking[1]:<10}{show_booking[2]:<20}{check_in:<15}{check_out:<15}")
    print("To calculate month revenue:")
    choose_month = int(input("Enter a month in number: "))
    choose_year = int(input("Enter a year: "))
    first_day = date(choose_year, choose_month, 1)
    last_day = date(choose_year, choose_month, calendar.monthrange(choose_year, choose_month)[1])
    cursor.execute('''select price_per_night, check_in_date, check_out_date
                   from total_money''')
    bookings = cursor.fetchall()
    total_revenue = 0
    for booking in bookings:
        price_per_night, check_in_date, check_out_date = booking
        last_night_stay = check_out_date - timedelta(days = 1)
        start = max(check_in_date, first_day)
        end = min(last_night_stay, last_day)
        if start <= end:
            nights = (end-start).days + 1
            total_revenue += nights*price_per_night
    print(f"Total revenue in month {choose_month} is ${float(total_revenue)}")

def total_revenue_in_year():
    print("To calculate revenue of a year")
    year = int(input("Enter a year: "))
    startyear = date(year, 1, 1)
    endyear = date(year, 12, 31)
    cursor.execute('''select price_per_night, check_in_date, check_out_date
                   from total_money''')
    bookings = cursor.fetchall()
    total_revenue = 0
    for booking in bookings:
        price_per_night, check_in_date, check_out_date = booking
        last_night_stay = check_out_date - timedelta(days = 1)
        start = max(check_in_date, startyear)
        end = min(last_night_stay, endyear)
        if start <= end:
            nights = (end-start).days + 1
            total_revenue += nights*price_per_night
    print(f"Total revenue in year {year} is ${float(total_revenue)}")
    
if __name__ == "__main__":    
    main()

