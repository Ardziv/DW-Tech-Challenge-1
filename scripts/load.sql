COPY nation FROM '/srv/data/nation.csv' WITH (FORMAT csv, DELIMITER '|');
COPY region FROM '/srv/data/region.csv' WITH (FORMAT csv, DELIMITER '|');
COPY part FROM '/srv/data/part.csv' WITH (FORMAT csv, DELIMITER '|');
COPY supplier FROM '/srv/data/supplier.csv' WITH (FORMAT csv, DELIMITER '|');
COPY partsupp FROM '/srv/data/partsupp.csv' WITH (FORMAT csv, DELIMITER '|');
COPY customer FROM '/srv/data/customer.csv' WITH (FORMAT csv, DELIMITER '|');
COPY orders FROM '/srv/data/orders.csv' WITH (FORMAT csv, DELIMITER '|');
COPY lineitem FROM '/srv/data/lineitem.csv' WITH (FORMAT csv, DELIMITER '|');
