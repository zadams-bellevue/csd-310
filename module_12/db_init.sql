CREATE DATABASE whatabook;
USE whatabook;
CREATE USER 'whatabook_user'@'%' IDENTIFIED WITH mysql_native_password BY 'MySQL8IsGreat!';
GRANT ALL ON whatabook.* TO 'whatabook_user'@'%';
CREATE TABLE user (
	user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	first_name VARCHAR(75) NOT NULL,
	last_name VARCHAR(75) NOT NULL
);
CREATE TABLE book (
	book_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	book_name VARCHAR(200) NOT NULL,
	details VARCHAR(500) DEFAULT NULL,
	author VARCHAR(200) NOT NULL
);
CREATE TABLE wishlist (
	wishlist_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	user_id INT NOT NULL,
	book_id INT NOT NULL,
	FOREIGN KEY (user_id) REFERENCES user (user_id),
	FOREIGN KEY (book_id) REFERENCES book (book_id),
	UNIQUE KEY (user_id, book_id)
);
CREATE TABLE store (
	store_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	locale VARCHAR(500) NOT NULL
);


INSERT INTO store (locale) VALUES ('123 Nowhere Street, Nowhere, ZZ 00000');
INSERT INTO book (book_name, details, author) VALUES
	('Mistborn: The Final Empire', 'Mistborn Trilogy, Book 1', 'Brandon Sanderson'),
	('The Well of Ascension', 'Mistborn Trilogy, Book 2', 'Brandon Sanderson'),
	('The Hero of Ages', 'Mistborn Trilogy, Book 3', 'Brandon Sanderson'),
	('The Way of Kings', 'Stormlight Archive, Book 1', 'Brandon Sanderson'),
	('Words of Radiance', 'Stormlight Archive, Book 2', 'Brandon Sanderson'),
	('Oathbringer', 'Stormlight Archive, Book 3', 'Brandon Sanderson'),
	('Rhythm of War', 'Stormlight Archive, Book 4', 'Brandon Sanderson'),
	('The Name of the Wind', 'Kingkiller Chronicle, Book 1', 'Patrick Rothfuss'),
	('The Wise Man''s Fear', 'Kingkiller Chronicle, Book 2', 'Patrick Rothfuss')
;
INSERT INTO user (first_name, last_name) VALUES
	('Billy', 'Bob'),
	('John', 'Doe'),
	('Joe', 'Shmoe')
;
INSERT INTO wishlist (user_id, book_id)
SELECT u.user_id, b.book_id
FROM (SELECT ROW_NUMBER() OVER (ORDER BY user_id ASC) rn, user_id FROM user) u
INNER JOIN (SELECT ROW_NUMBER() OVER (ORDER BY book_id ASC) rn, book_id FROM book) b ON u.rn = b.rn;