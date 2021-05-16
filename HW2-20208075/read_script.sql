create table table1
(
    id        int,
    year int,
    annual_inc     int,
    income_cat int,
    loan_amount   int,
    recoveries  float);

COPY table1(id, year, annual_inc, income_cat ,loan_amount,recoveries)
    FROM '/file.csv'
    DELIMITER ','
    CSV HEADER;
