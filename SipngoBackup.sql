
DROP TABLE IF EXISTS `category`;

CREATE TABLE `category` (
  `id` int NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `imagePath` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ; 


INSERT INTO `category` VALUES (12,'Fresh juices',1,'static/FreshJuices.jpg'),(13,'Milkshakes',1,'static/milkshakes.jpg'),(14,'Thick shake',1,NULL),(15,'Detox juices',1,NULL),(16,'Bowls and sandwiches',1,'static/Sandwiches.jpeg'),(17,'Hot beverages ',1,'static/hotbeverages.jpeg'),(18,'Ice cream ',1,NULL),(19,'Combo',0,NULL),(20,'Add on',1,NULL),(21,'Breakfast fast',1,NULL),(22,'Protein shake ',1,NULL),(23,'Combo',0,NULL),(24,'Customized',1,NULL),(25,'Burger',1,NULL),(26,'Parcel ',1,NULL),(27,'Combos',1,NULL);

CREATE TABLE `day_tracker` (
  `location` varchar(256) DEFAULT NULL,
  `sub_id` varchar(256) DEFAULT NULL,
  `user_id` varchar(256) DEFAULT NULL,
  `order_date` date DEFAULT NULL,
  `STATUS` varchar(256) DEFAULT NULL
) ; 




CREATE TABLE `item` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `category` int NOT NULL,
  `price` int NOT NULL,
  `image_path` varchar(300) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
); 


INSERT INTO `item` VALUES (15,'Watermelon juice',12,60,'static/items/1000072417.jpg',1),(16,'Mosambi juice',12,60,'static/items/1000072436.jpg',1),(17,'Orange juice',12,65,'static/items/1000072437.jpg',1),(18,'Pineapple',12,70,'static/items/1000072438.jpg',1),(19,'Muskmelon juice',12,70,'static/items/1000072439.jpg',1),(20,'Pomogranate juice ',12,80,'static/items/1000072440.jpg',1),(21,'Apple juice ',12,80,'static/items/1000072441.jpg',1),(22,'Banana',13,60,'static/items/1000072442.jpg',1),(23,'Vanilla ',13,60,'static/items/1000072443.jpg',1),(24,'Chocolate ',13,70,'static/items/1000072444.jpg',1),(25,'Strawberry ',13,70,'static/items/1000072445.jpg',1),(26,'Mango',13,80,'static/items/1000072446.jpg',1),(27,'Chocolate ',14,80,'static/items/1000072444.jpg',1),(28,'Oreo',14,100,'static/items/1000072447.jpg',1),(29,'Kitkat',14,100,'static/items/1000072448.jpg',1),(30,'Belgian chocolate ',14,100,'static/items/1000072449.jpg',1),(31,'Strawberry ',14,100,'static/items/1000072450.jpg',1),(32,'Beetroot ',15,70,'static/items/1000072451.jpg',1),(33,'Carrot ',15,70,'static/items/1000072452.jpg',1),(34,'ABC',15,70,'static/items/1000072453.jpg',1),(35,'APC',15,70,'static/items/1000072454.webp',0),(36,'APC',15,70,'static/items/1000072455.jpg',1),(37,'Peanut butter sandwich ',16,50,'static/items/1000072458.jpg',1),(38,'Veg sandwich ',16,60,'static/items/1000072459.jpg',1),(40,'Paneer sandwich ',16,75,'static/items/1000072461.jpg',1),(41,'Hot chocolate fudge',17,80,'static/items/1000072462.jpg',1),(42,'Tea',17,15,'static/items/1000072463.jpg',1),(43,'Lemon tea',17,20,'static/items/1000072464.jpg',1),(44,'Gadbud bowl',18,80,'static/items/1000072465.jpg',1),(45,'One scoop',18,25,'static/items/1000072466.jpg',1),(46,'2 scoops',18,50,'static/items/1000072466.jpg',1),(47,'Paneer +mango ',19,140,'static/items/1000072461.jpg',1),(48,'Veg +juice',19,125,'static/items/1000072459.jpg',1),(49,'Cheese',20,15,'static/items/1000072756.jpg',1),(50,'Veg sandwich+pineapple ',21,115,'static/items/1000072459.jpg',1),(51,'Paneer sandwich+watermelon ',21,120,'static/items/1000072461.jpg',1),(52,'Peanut butter+protein ',21,155,'static/items/1000072458.jpg',1),(53,'Coffee',17,15,'static/items/1000072831.jpg',1),(54,'Cold coffee',13,60,'static/items/1000072449.jpg',1),(55,'One scoop',22,120,'static/items/1000073300.jpg',1),(56,'2 scoops',22,200,'static/items/1000073300.jpg',1),(57,'Normal tea',17,10,'static/items/desktop-wallpaper-krishna-cute-krishna.jpg',1),(58,'Oreo',13,80,'static/items/desktop-wallpaper-krishna-cute-krishna.jpg',1),(59,'Veg',23,105,'static/items/desktop-wallpaper-krishna-cute-krishna.jpg',0),(60,'Paneer',23,125,'static/items/sri_krishna-wallpaper.jpg',0),(61,'Juice',24,80,'static/items/IMG_20230622_003224.jpg',1),(62,'Veg burger',25,60,'static/items/desktop-wallpaper-krishna-cute-krishna.jpg',1),(63,'French fries ',16,50,'static/items/1000074447.jpg',1),(64,'Burger combo',23,170,'static/items/desktop-wallpaper-krishna-cute-krishna.jpg',0),(65,'Redvelvet',18,50,'static/items/download.jpeg',1),(66,'Parcel ',26,5,'static/items/1000075517.jpg',1),(67,'Paneer',23,140,'static/items/download.jpeg',0),(68,'Burger combo',23,115,'static/items/download.jpeg',0),(69,'Mango pulp',14,100,'static/items/images.jpeg',1),(70,'Fries combo',23,110,'static/items/images.jpeg',0),(71,'Veg',27,110,'static/items/download_2.jpeg',1),(72,'Paneer',27,135,'static/items/download_1.jpeg',1),(73,'Fries',27,100,'static/items/download_3.jpeg',1),(74,'Panzer mango',27,145,'static/items/download_1.jpeg',1);






CREATE TABLE `order_detail` (
  `sub_id` varchar(256) DEFAULT NULL,
  `user_id` varchar(64) DEFAULT NULL,
  `item_id` varchar(64) DEFAULT NULL,
  `cnt` int DEFAULT NULL,
  `amount` int DEFAULT NULL,
  `slot` varchar(20) DEFAULT NULL,
  `days` int DEFAULT NULL
); 







CREATE TABLE `subscription_tracker` (
  `user_id` varchar(64) DEFAULT NULL,
  `sub_id` varchar(256) DEFAULT NULL,
  `rem_days` int DEFAULT NULL,
  `order_placed` date DEFAULT NULL,
  `status` varchar(256) DEFAULT NULL,
  `total_amount` int DEFAULT NULL
);





CREATE TABLE `user_details` (
  `user_id` varchar(64) NOT NULL,
  `user_name` varchar(64) DEFAULT NULL,
  `user_email` varchar(64) DEFAULT NULL,
  `user_location` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
); 

CREATE TABLE UPI_TRANSACTIONS(transactionId VARCHAR(64) PRIMARY KEY, user_id VARCHAR(64) , date_of_transaction DATETIME , STATUS VARCHAR(64));

ALTER TABLE user_details ADD phone_no VARCHAR(64);


