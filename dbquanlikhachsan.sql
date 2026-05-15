CREATE DATABASE hotel_management_system; 
USE hotel_management_system;
create table rooms
(
    room_number int not Null UNIQUE PRIMARY KEY,
    room_type varchar(20) not NULL,
    price_per_night FLOAT not NULL
);
insert into rooms (room_number, room_type, price_per_night)
VALUES
(101, 'Standard', 30),
(102, 'Standard', 30),
(201, 'Deluxe', 100),
(202, 'Deluxe', 100),
(301, 'Suite', 200),
(302, 'Suite', 200);
create table customers
(
    customer_id int not null primary key AUTO_INCREMENT,
    customer_name varchar(50) not NULL
);
create table bookings
(
    booking_id int auto_increment primary key,
    customer_id int,
    room_number int,
    check_in_date date not NULL,
    check_out_date date not NULL,
    check (check_out_date > check_in_date),
    foreign key (customer_id) references customers(customer_id),
    foreign key (room_number) references rooms(room_number)
    
);

CREATE View all_booking AS
SELECT booking_id, customers.customer_name,
rooms.room_number, rooms.room_type, bookings.check_in_date, 
bookings.check_out_date FROM bookings
join customers on bookings.customer_id = customers.customer_id
join rooms on bookings.room_number = rooms.room_number
ORDER BY booking_id ASC

create view total_money AS
select bookings.booking_id, rooms.room_number, rooms.room_type, rooms.price_per_night, 
bookings.check_in_date, bookings.check_out_date,
DATEDIFF(check_out_date, check_in_date) AS days,
DATEDIFF(check_out_date, check_in_date) * rooms.price_per_night AS total
from bookings
join rooms on bookings.room_number = rooms.room_number
ORDER BY bookings.booking_id ASC