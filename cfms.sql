CREATE TABLE IF NOT EXISTS user (
    username VARCHAR(50) NOT NULL PRIMARY KEY,
    password VARCHAR(50) NOT NULL,
    question VARCHAR(50) NOT NULL,
    answer VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS payment (
    adate DATE NOT NULL,
    rs INT(11) NOT NULL,
    remark TEXT NOT NULL,
    type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS clients (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    mobile INT(12) NOT NULL,
    phone INT(12) NOT NULL
);

CREATE TABLE IF NOT EXISTS expenses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    adate DATE NOT NULL,
    name TEXT NOT NULL,
    rs DOUBLE NOT NULL
);

CREATE TABLE IF NOT EXISTS ot (
    adate DATE NOT NULL,
    name TEXT NOT NULL,
    hour INT(2) NOT NULL
);

CREATE TABLE IF NOT EXISTS labour_payment (
    adate DATE NOT NULL,
    name TEXT NOT NULL,
    rs DECIMAL(10,0) NOT NULL,
    ot DECIMAL(10,0) NOT NULL,
    total DECIMAL(10,0) NOT NULL,
    shift INT(1) NOT NULL
);

CREATE TABLE IF NOT EXISTS labour_attendance (
    name TEXT NOT NULL,
    Jun TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS labour_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name TEXT NOT NULL,
    other TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS production (
    adate DATE NOT NULL,
    tf INT(11) NOT NULL,
    fh INT(11) NOT NULL,
    ts INT(11) NOT NULL
);

CREATE TABLE IF NOT EXISTS production_payas (
    adate DATE NOT NULL,
    tf INT(11) NOT NULL,
    fh INT(11) NOT NULL,
    ts INT(11) NOT NULL
);

CREATE TABLE IF NOT EXISTS production_oras (
    adate DATE NOT NULL,
    tf INT(11) NOT NULL,
    fh INT(11) NOT NULL,
    ts INT(11) NOT NULL
);

CREATE TABLE IF NOT EXISTS production_34gram (
    adate DATE NOT NULL,
    tf INT(11) NOT NULL,
    fh INT(11) NOT NULL,
    ts INT(11) NOT NULL
);

CREATE TABLE IF NOT EXISTS raw_material (
    id INT PRIMARY KEY AUTO_INCREMENT,
    adate DATE NOT NULL,
    raw TEXT NOT NULL,
    type TEXT NOT NULL,
    quantity INT(11) NOT NULL
);

CREATE TABLE IF NOT EXISTS raw_material_payas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    adate DATE NOT NULL,
    raw TEXT NOT NULL,
    type TEXT NOT NULL,
    quantity INT(11) NOT NULL
);

CREATE TABLE IF NOT EXISTS raw_material_oras (
    id INT PRIMARY KEY AUTO_INCREMENT,
    adate DATE NOT NULL,
    raw TEXT NOT NULL,
    type TEXT NOT NULL,
    quantity INT(11) NOT NULL
);

CREATE TABLE IF NOT EXISTS raw_material_34gram (
    id INT PRIMARY KEY AUTO_INCREMENT,
    adate DATE NOT NULL,
    raw TEXT NOT NULL,
    type TEXT NOT NULL,
    quantity INT(11) NOT NULL
);

CREATE TABLE IF NOT EXISTS sell (
    id INT PRIMARY KEY AUTO_INCREMENT,
    adate DATE NOT NULL,
    client TEXT NOT NULL,
    item TEXT NOT NULL,
    quantity INT(11) NOT NULL,
    rate DOUBLE NOT NULL,
    total DOUBLE NOT NULL,
    paid TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stock_maintenance (
    tf INT(11) NOT NULL,
    fh INT(11) NOT NULL,
    ts INT(11) NOT NULL,
    preform250 INT(11) NOT NULL,
    preform500 INT(11) NOT NULL,
    preform1000 INT(11) NOT NULL,
    lable250 INT(11) NOT NULL,
    lable500 INT(11) NOT NULL,
    lable1000 INT(11) NOT NULL,
    caps250 INT(11) NOT NULL,
    caps500 INT(11) NOT NULL,
    caps1000 INT(11) NOT NULL,
    boxes250 INT(11) NOT NULL,
    boxes500 INT(11) NOT NULL,
    boxes1000 INT(11) NOT NULL
);


CREATE TABLE IF NOT EXISTS stock_maintenance_payas (
    tf INT(11) NOT NULL,
    fh INT(11) NOT NULL,
    ts INT(11) NOT NULL,
    preform250 INT(11) NOT NULL,
    preform500 INT(11) NOT NULL,
    preform1000 INT(11) NOT NULL,
    lable250 INT(11) NOT NULL,
    lable500 INT(11) NOT NULL,
    lable1000 INT(11) NOT NULL,
    caps250 INT(11) NOT NULL,
    caps500 INT(11) NOT NULL,
    caps1000 INT(11) NOT NULL,
    boxes250 INT(11) NOT NULL,
    boxes500 INT(11) NOT NULL,
    boxes1000 INT(11) NOT NULL
);

CREATE TABLE IF NOT EXISTS stock_maintenance_oras (
    tf INT(11) NOT NULL,
    fh INT(11) NOT NULL,
    ts INT(11) NOT NULL,
    preform250 INT(11) NOT NULL,
    preform500 INT(11) NOT NULL,
    preform1000 INT(11) NOT NULL,
    lable250 INT(11) NOT NULL,
    lable500 INT(11) NOT NULL,
    lable1000 INT(11) NOT NULL,
    caps250 INT(11) NOT NULL,
    caps500 INT(11) NOT NULL,
    caps1000 INT(11) NOT NULL,
    boxes250 INT(11) NOT NULL,
    boxes500 INT(11) NOT NULL,
    boxes1000 INT(11) NOT NULL
);

CREATE TABLE IF NOT EXISTS stock_maintenance_34gram (
    tf INT(11) NOT NULL,
    fh INT(11) NOT NULL,
    ts INT(11) NOT NULL,
    preform250 INT(11) NOT NULL,
    preform500 INT(11) NOT NULL,
    preform1000 INT(11) NOT NULL,
    lable250 INT(11) NOT NULL,
    lable500 INT(11) NOT NULL,
    lable1000 INT(11) NOT NULL,
    caps250 INT(11) NOT NULL,
    caps500 INT(11) NOT NULL,
    caps1000 INT(11) NOT NULL,
    boxes250 INT(11) NOT NULL,
    boxes500 INT(11) NOT NULL,
    boxes1000 INT(11) NOT NULL
);
