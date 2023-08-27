CREATE TABLE order_detail(
	order_id VARCHAR(64),
	user_id  VARCHAR(64),
	item_id  VARCHAR(64),
	cnt INT,
	amount INT , 
	slot VARCHAR(20)
);

ALTER TABLE order_detail ADD days INT;
 ALTER TABLE order_detail MODIFY order_id VARCHAR(256);
 ALTER TABLE order_detail RENAME COLUMN order_id TO sub_id;
