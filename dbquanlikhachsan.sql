CREATE DATABASE hotel_management_system; 
USE hotel_management_system;
create table rooms
(
    room_number int not Null UNIQUE PRIMARY KEY,
    room_type varchar(20) not NULL
);
insert into rooms (room_number, room_type)
VALUES
(101, 'Standard'),
(102, 'Standard'),
(201, 'Deluxe'),
(202, 'Deluxe'),
(301, 'Suite'),
(302, 'Suite');
create table customers
(
    customer_id int primary key,
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
drop DATABASE if EXISTS hotel_management_system;
CREATE VIEW all_bookings AS
SELECT customers.customer_name,
rooms.room_number, rooms.room_type, bookings.check_in_date, 
bookings.check_out_date FROM bookings
join customers on bookings.customer_id = customers.customer_id
join rooms on bookings.room_number = rooms.room_number;

CREATE View individual_booking AS
SELECT customers.customer_id, customers.customer_name,
rooms.room_number, rooms.room_type, bookings.check_in_date, 
bookings.check_out_date FROM bookings
join customers on bookings.customer_id = customers.customer_id
join rooms on bookings.room_number = rooms.room_number