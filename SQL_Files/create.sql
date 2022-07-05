DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS categories_description;
DROP TABLE IF EXISTS post_address_lookup CASCADE;
DROP TABLE IF EXISTS supplier CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS employees CASCADE;
DROP TABLE IF EXISTS territories CASCADE;
DROP TABLE IF EXISTS employee_territories CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS shippers CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS order_details CASCADE;

CREATE TABLE categories(
id int PRIMARY KEY,
name varchar(25) NOT NULL
);

CREATE TABLE categories_description (
category_id int REFERENCES categories(id) ON DELETE SET NULL ON UPDATE CASCADE,
description varchar(100)
);

CREATE TABLE post_address_lookup(
postal_code varchar(100),
country varchar(100), -- change
city varchar(100) NOT NULL,
PRIMARY KEY (postal_code, country)
);

CREATE TABLE supplier(
id int PRIMARY KEY,
company_name varchar(100) NOT NULL,
contact_name varchar(100) NOT NULL,
contact_title varchar(100),
postal_code varchar(100),
country varchar(100),
contact varchar(100) NOT NULL,
FOREIGN KEY (postal_code, country) REFERENCES post_address_lookup (postal_code, country) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE products(
id int PRIMARY KEY,
name varchar(255) NOT NULL,
supplier_id int REFERENCES supplier(id) ON DELETE SET NULL ON UPDATE CASCADE,
category_id int REFERENCES categories(id) ON DELETE SET NULL ON UPDATE CASCADE,
quantity_per_unit int NOT NULL,
unit_price float NOT NULL,
stock int NOT NULL DEFAULT 0,
discontinued BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE employees(
id int PRIMARY KEY,
last_name varchar(25) NOT NULL,
first_name varchar(25) NOT NULL,
title varchar(25),
birthdate DATE,
hire_date DATE DEFAULT CURRENT_DATE,
postal_code VARCHAR(100),
country varchar(100),
contact varchar(16) NOT NULL,
reports_to int REFERENCES employees(id) ON DELETE SET NULL ON UPDATE CASCADE,
FOREIGN KEY (postal_code, country) REFERENCES post_address_lookup (postal_code, country) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE territories(
id int PRIMARY KEY,
name varchar(100) NOT NULL 
);

CREATE TABLE employee_territories(
employee_id int REFERENCES employees(id) ON DELETE SET NULL ON UPDATE CASCADE,
territory_id int REFERENCES territories(id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE customers(
id varchar(10) PRIMARY KEY,
name varchar(50) NOT NULL,
contact_name varchar(100) NOT NULL,
title varchar(100),
postal_code varchar(100),
country varchar(100),
contact varchar(100) NOT NULL,
FOREIGN KEY (postal_code, country) REFERENCES post_address_lookup (postal_code, country) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE shippers(
id int PRIMARY KEY,
name varchar(25) NOT NULL,
contact varchar(16) NOT NULL
);

CREATE TABLE orders(
id int PRIMARY KEY,
customer_id varchar(10) REFERENCES customers(id) ON DELETE SET NULL ON UPDATE CASCADE,
employee_id int REFERENCES employees(id) ON DELETE SET NULL ON UPDATE CASCADE,
order_date DATE DEFAULT CURRENT_DATE,
delivery_date DATE,
shipped_date DATE,
shipper_id int REFERENCES shippers(id) ON DELETE SET NULL ON UPDATE CASCADE,
weight FLOAT,
ship_name VARCHAR(100),
ship_postal_code varchar(100),
ship_country varchar(100),
FOREIGN KEY (ship_postal_code, ship_country) REFERENCES post_address_lookup (postal_code, country) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE order_details(
order_id int REFERENCES orders(id) ON DELETE SET NULL ON UPDATE CASCADE,
product_id int REFERENCES products(id) ON DELETE SET NULL ON UPDATE CASCADE,
unit_price FLOAT NOT NULL,
quantity int not NULL,
discount FLOAT DEFAULT 0
);

CREATE INDEX orders_shipper_id ON orders (shipper_id);

CREATE INDEX orders_customer_id ON orders (customer_id);

CREATE INDEX orders_employee_id ON orders (employee_id);

CREATE INDEX order_details_order_id ON order_details (order_id);

CREATE INDEX order_details_product_id ON order_details (product_id);

CREATE INDEX products_category_id ON products (category_id);

CREATE INDEX products_supplier_id ON products (supplier_id);

CREATE OR REPLACE FUNCTION insert_random_territory()
  RETURNS trigger AS
$$
DECLARE
territory_id INTEGER;
BEGIN
		 SELECT into territory_id id FROM territories ORDER BY random() LIMIT 1;
		 
         INSERT INTO employee_territories
         VALUES(NEW.id, territory_id);
 
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';


CREATE TRIGGER employee_terriroty
  AFTER INSERT
  ON employees
  FOR EACH ROW
  EXECUTE PROCEDURE insert_random_territory();


-- pg_dump -U postgres -W -F p DMQL_Project > /Users/wizard/Desktop/DMQL_Project.sql