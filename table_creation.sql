create table customers(
customer_id int primary key auto_increment, 
customer_name varchar(25),
address varchar(100),
mobile varchar(100),
email varchar(30)
);

create table service_plans(
plan_id int primary key auto_increment,
plan_name varchar(20),
speed varchar(20),
data_limit varchar(20),
validity varchar(20),
price decimal(10,2)
);

create table subscription(
subscription_id int primary key auto_increment,
customer_id int,
plan_id int,
start_date date,
end_date date,
foreign key (customer_id) references customers(customer_id),
foreign key (plan_id) references service_plans(plan_id)
);

create table billing (
    bill_id INT PRIMARY KEY AUTO_INCREMENT,
    subscription_id INT,
    bill_date DATE,
    amount_due DECIMAL(10, 2),
    bill_status VARCHAR(20),
    FOREIGN KEY (subscription_id) REFERENCES subscription(subscription_id)
);

insert into customers (customer_name, address, mobile, email) 
values 
('John Doe', '1234 Elm Street, Springfield, IL', '555-1234', 'john.doe@example.com'),
('Jane Smith', '5678 Oak Avenue, Springfield, IL', '555-5678', 'jane.smith@example.com'),
('Alice Johnson', '9101 Pine Road, Decatur, IL', '555-9101', 'alice.johnson@example.com'),
('Bob Brown', '2345 Maple Drive, Peoria, IL', '555-2345', 'bob.brown@example.com'),
('Charlie Davis', '6789 Birch Lane, Bloomington, IL', '555-6789', 'charlie.davis@example.com'),
('Diana Wilson', '3456 Cedar Blvd, Champaign, IL', '555-3456', 'diana.wilson@example.com'),
('Edward Taylor', '7890 Redwood St, Urbana, IL', '555-7890', 'edward.taylor@example.com'),
('Fiona Martin', '2345 Elmwood Ave, Carbondale, IL', '555-2346', 'fiona.martin@example.com'),
('George Lee', '5678 Maple Dr, Normal, IL', '555-5679', 'george.lee@example.com'),
('Hannah White', '8910 Oakwood Ln, Peoria, IL', '555-8910', 'hannah.white@example.com');


INSERT INTO service_plans (plan_name, speed, data_limit, price,validity)
VALUES 
('Basic Plan', '50 Mbps', '500 GB', 29.99, '30 days'),
('Standard Plan', '100 Mbps', '1 TB', 49.99, '30 days'),
('Premium Plan', '200 Mbps', '2 TB', 79.99, '6 months'),
('Ultra Plan', '500 Mbps', '5 TB', 99.99, '6 months'),
('Gigabit Plan', '1 Gbps', 'Unlimited', 149.99, '12 months'),
('Family Plan', '200 Mbps', '3 TB', 89.99, '6 months'),
('Business Plan', '500 Mbps', 'Unlimited', 199.99, '12 months'),
('Student Plan', '50 Mbps', '300 GB', 19.99, '30 days'),
('Streaming Plan', '150 Mbps', '1 TB', 59.99, '3 months'),
('High Speed Plan', '300 Mbps', '1.5 TB', 69.99, '6 months');

INSERT INTO subscription (customer_id, plan_id, start_date, end_date, validity)
VALUES 
(1, 2, '2024-11-01', '2024-11-30', '30 days'),
(11, 3, '2024-11-05', '2025-05-05', '6 months'),
(12, 4, '2024-11-10', '2025-05-10', '6 months'),
(4, 1, '2024-11-12', '2024-12-12', '30 days'),
(5, 5, '2024-11-15', '2025-11-15', '12 months'),
(6, 6, '2024-11-20', '2025-05-20', '6 months'),
(7, 7, '2024-11-25', '2025-05-25', '12 months'),
(8, 8, '2024-11-28', '2024-12-28', '30 days'),
(9, 9, '2024-11-30', '2025-02-28', '3 months'),
(10, 10, '2024-12-01', '2025-06-01', '6 months');

INSERT INTO billing (subscription_id, bill_date, amount_due, bill_status)
VALUES 
(11, '2024-11-30', 29.99, 'Unpaid'),
(12, '2025-05-05', 49.99, 'Unpaid'),
(13, '2025-05-10', 79.99, 'Unpaid'),
(14, '2024-12-12', 29.99, 'Paid'),
(15, '2025-11-15', 149.99, 'Unpaid'),
(16, '2025-05-20', 89.99, 'Unpaid'),
(17, '2025-05-25', 199.99, 'Paid'),
(18, '2024-12-28', 59.99, 'Unpaid'),
(19, '2025-02-28', 69.99, 'Paid'),
(20, '2025-06-01', 69.99, 'Unpaid');


select * from customers;
select * from service_plans;
select * from billing;
select * from subscriptions;
