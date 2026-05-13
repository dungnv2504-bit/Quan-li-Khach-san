# Connect to MySQL database.
import mysql.connector
from datetime import datetime
connection = mysql.connector.connect(
    host = 'host',
    user = 'user',
    password = 'password',
    database = 'hotel_management_system'
)
cursor = connection.cursor()

def main(): #giao dien chinh cua phan mem truy cap
    print("This is the hotel management system. Please select an option:")
    while True:
        print("")
        print("1. Show available rooms")
        print("2. Add a customer, please add customer ID and name before booking")
        print("3. Create a booking")
        print("4. Show all bookings")
        print("5. Update individual info")
        print("6. Show individual booking")
        print("7. Remove customer")
        print("8. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            show_rooms()
        elif choice == "2":
            add_customer()
        elif choice == "3":
            create_booking()
        elif choice == "4":
            show_all_bookings()
        elif choice == "5":
            update_individual_info()
        elif choice == '6':
            show_individual_booking()
        elif choice == "7":
            cancel_booking()
        elif choice == "8":
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
    cursor.execute("""SELECT * from all_bookings""")
    bookings = cursor.fetchall()
    print("All bookings:")
    #tao bang
    print(f"{'Customer':<15}{'Room':<10}{'Room Type':<15}{'Check-in':<15}{'Check-out':<15}")
    for booking in bookings:
        check_in = str(booking[3])
        check_out = str(booking[4])
        print(f"{booking[0]:<15}{booking[1]:<10}{booking[2]:<15}{check_in:<15}{check_out:<15}")

def show_individual_booking(): #truy cap vao booking cua tung khach hang
    name = input("Enter customer name: ")
    Id = input("Enter customer ID: ")
    cursor.execute("""SELECT * from individual_booking
                   where customer_name = %s 
                   or customer_id = %s""", (name, Id))
    individual_booking = cursor.fetchall()
    #tao bang
    print(f"Customer: {name}")
    print(f"{'ID':<10}{'Customer':<15}{'Room':<10}{'Room Type':<15}{'Check-in':<15}{'Check-out':<15}")
    for booking in individual_booking:
        check_in = str(booking[4])
        check_out = str(booking[5])
        print(f"{booking[0]:<10}{booking[1]:<15}{booking[2]:<10}{booking[3]:<15}{check_in:<15}{check_out:<15}")

def update_individual_info(): #thay doi thong tin dat phong cua khach hang
    Id = input("Enter customer ID: ")
    check_customerID_query = """select customer_id from customers where customer_id = %s"""
    cursor.execute(check_customerID_query, (Id,))
    IDs = cursor.fetchone()
    if not IDs:
        print("Customer ID does not match. Please review customer ID.")
        return
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
                    where customer_id = %s""", (new_name, Id))
            connection.commit()
            print("Customer name updated successfully.")
        elif choice == "2": #doi phong cho khach
            new_room = input("Enter customer new room: ")
            cursor.execute("""Select room_number from rooms where room_number = %s""", (new_room,))
            room_exist = cursor.fetchone()
            if not room_exist:
                print("Invalid room choice")
                continue
            cursor.execute("""Update bookings
                           set room_number = %s
                           where customer_id = %s""", (new_room, Id))
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
                WHERE customer_id = %s""", (check_in_date, check_out_date, Id))
            connection.commit()
            print("Check-out date updated successfully.")
        elif choice == "4":
            print("Thank you for updating.")
            break
        else:
            print("Invalid choice. Please try again.")

def create_booking(): #dat phong
    #bookings
    room_number = input("Enter desired room number: ")
    check_room_query = """select room_number from rooms where room_number = %s"""
    cursor.execute(check_room_query, (room_number,))
    rooms = cursor.fetchone()
    if not rooms: #dam bao khach ko chon sai phong 
        print("The selected room does not exist. Please select room from the list.")
        return
    customer_id = input("Enter customer ID: ")
    check_customerID_query = """select customer_id from customers where customer_id = %s"""
    cursor.execute(check_customerID_query, (customer_id,))
    IDs = cursor.fetchone()
    if not IDs: #dam bao khach ko dien ID ca nhan khi chua dc them khach hang
        print("Customer ID does not match. Please review customer ID.")
        return
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

    check_date_overlap_query = """SELECT check_in_date, check_out_date 
                                    FROM bookings
                                    WHERE room_number = %s"""
    cursor.execute(check_date_overlap_query, (room_number,))
    existing_bookings = cursor.fetchall()
    for booking in existing_bookings:
        old_checkin = booking[0]
        old_checkout = booking[1]
        new_checkin = checkin
        new_checkout = checkout
        if (old_checkout > new_checkin and new_checkout > old_checkin): #dam bao là khach ko chon phong trong thoi gian ngkhac dg su dung
            print(f"Sorry, the room is unavailable from {old_checkin} to {old_checkout}. Please choose different dates or a different room.")
            return
    insert_bookings_query = """insert into bookings
    (customer_id, room_number, check_in_date, check_out_date)
    values (%s, %s, %s, %s)"""
    cursor.execute(insert_bookings_query, (customer_id, room_number, check_in_date, check_out_date))
    connection.commit()
    print(f"Booking created successfully for room {room_number} from {check_in_date} to {check_out_date}.")

def cancel_booking(): #huy phong
    customer_name = input("Enter customer name: ")
    customer_id = input("Enter customer ID: ")
    delete_query = """delete from bookings where customer_id = %s"""
    cursor.execute(delete_query, (customer_id,))
    connection.commit()
    print(f"Successfully remove customer {customer_name}.")

def add_customer(): #them khach hang
    #customers
    customer_id = input("Enter customer ID: ")
    customer_name = input("Enter customer name: ")
    try:
        insert_customers_query = """INSERT INTO customers (customer_id, customer_name) 
        VALUES (%s, %s)"""
        cursor.execute(insert_customers_query, (customer_id, customer_name))
        connection.commit()
        print("Customer added successfully.")
    except mysql.connector.Error:
        print("Customer already exists.")

if __name__ == "__main__":    
    main()

