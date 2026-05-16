CREATE TABLE region (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region TEXT NOT NULL UNIQUE,
    code TEXT NOT NULL UNIQUE         
);

CREATE TABLE specialization (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    specialization TEXT NOT NULL                  
);

CREATE TABLE company (
    company_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    company_name TEXT NOT NULL,
    email TEXT NOT NULL,   
    INN INTEGER NOT NULL,                               
    KPP INTEGER NOT NULL,
    OGRN INTEGER NOT NULL                    
);

CREATE TABLE vacancy (
    id TEXT PRIMARY KEY,               
    name TEXT NOT NULL,                        
    data_create DATE NOT NULL,
    region_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,                     
    salary_before REAL NOT NULL,
    salary_after REAL NOT NULL,
    specialization_id INTEGER NOT NULL,

    FOREIGN KEY (region_id) REFERENCES region(id),
    FOREIGN KEY (company_id) REFERENCES company(company_id),
    FOREIGN KEY (specialization_id) REFERENCES specialization(id)                             
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,                        
    full_name TEXT NOT NULL,                   
    login TEXT NOT NULL UNIQUE,              
    password TEXT NOT NULL              
);
