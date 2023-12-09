DROP DATABASE IF EXISTS sipngo; 
CREATE database sipngo;
CREATE USER 'sipngo'@'%' IDENTIFIED BY 'Password';

GRANT ALL PRIVILEGES ON sipngo.* TO 'sipngo'@'%'; 
