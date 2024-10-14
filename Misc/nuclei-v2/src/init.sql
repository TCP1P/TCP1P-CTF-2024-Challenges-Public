USE loginapp; 

CREATE TABLE accounts (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL
); 

INSERT INTO accounts VALUES (NULL, 'admin', 'admin@mail.com', 'DappaIngpo_33441');
INSERT INTO accounts VALUES (NULL, 'guest', 'guest@mail.com', 'guest');