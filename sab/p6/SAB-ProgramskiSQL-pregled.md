# Programski SQL Predgled

## Kreiranje procedura

Na primer neka je potrebno dodati novog klijenta, a potom osvežiti informacije o dodeljenom prodavcu i ciljnoj kvoti, kao i osvežiti informacije koje se odnose na kancelariju tako da se ciljna prodaja podigne za odgovarajući iznos, i naravno potvrditi promene završavanjem transakcije.

```sql
INSERT INTO CUSTOMERS (CUST_NUM, COMPANY, CUST_REP, CREDIT_LIMIT)
 VALUES (2137, 'XYZ Corporation', 103, 30000.00);

UPDATE SALESREPS
 SET QUOTA = QUOTA + 50000.00
WHERE EMPL_NUM = 103;

UPDATE OFFICES
 SET TARGET = TARGET + 50000.00
WHERE CITY = 'Chicago';

COMMIT;
```

Ukoliko bi se napravila odgovarajuća procedura, onda bi bila pozivana sa:

```sql
ADD_CUST('XYZ Corporation', 2137, 30000.00, 50000.00, 103, 'Chicago');
```

Svi parametri procedure su ulazni, što se u nekim dijalektima naznačava pomoću ključne reči `IN`. Ovi parametri se mogu koristiti svuda u telu procedure gde je inače moguće da se pojavi konstanta. Moguća je upotreba i takozvanih izlaznih parametara (ključna reč `OUTPUT`, ili samo `OUT`) kada se očekuje da procedura vrati neku vrednost. Takođe, kod nekih implementacija postoje i ulazno-izlazni parametri (`INOUT`).

## Implementacija u ORACLE (PL/SQL)

```sql
/* Add a customer procedure */
CREATE PROCEDURE add_cust (
 c_name IN VARCHAR2, /* input customer name */
 c_num IN INTEGER, /* input customer number */
 cred_lim IN NUMBER, /* input credit limit */
 tgt_sls IN NUMBER, /* input target sales */
 c_rep IN INTEGER, /* input salesrep emp # */
 c_offc IN VARCHAR2) /* input office city */
AS 
BEGIN 
 /* Insert new row of CUSTOMERS table */
 INSERT INTO customers (cust_num, company, cust_rep, credit_limit)
 VALUES (c_num, c_name, c_rep, cred_lim);
 
 /* Update row of SALESREPS table */
 UPDATE salesreps
 SET quota = quota + tgt_sls
 WHERE empl_num = c_rep;

 /* Update row of OFFICES table */
 UPDATE offices
 SET target = target + tgt_sls
 WHERE city = c_offc;

 /* Commit transaction and we are done */
 COMMIT;
END;
```

Poziv procedure:

```sql
EXECUTE ADD_CUST('XYZ Corporation', 2137, 30000.00, 50000.00, 103, 'Chicago');
```

Ukoliko se poziva iz druge procedure onda može i samo `ADD_CUST(…)`, odnosno, bez reči `EXECUTE`.

```sql
EXECUTE ADD_CUST (c_name = 'XYZ Corporation',
 c_num = 2137,
 cred_lim = 30000.00,
 c_offc = 'Chicago',
 c_rep = 103,
 tgt_sales = 50000.00);
```

## Implementacija u SQL Server (T-SQL)

Ne koriste se zagrade u deklaraciji procedure, parametri se označavaju specijalnim karakterom `@`, a takođe čitava procedura je jedan SQL iskaz, pa ukoliko se želi nešto kompleksnije telo, onda se to navodi kao blok (`BEGIN-END`).

```sql
/* Add a customer procedure */
CREATE PROC add_cust
 @c_name VARCHAR(20), /* input customer name */
 @c_num INTEGER, /* input customer number */
 @cred_lim DECIMAL(9,2), /* input credit limit */
 @tgt_sls DECIMAL(9,2), /* input target sales */
 @c_rep INTEGER, /* input salesrep emp # */
 @c_offc VARCHAR(15) /* input office city */
AS
BEGIN
 /* Insert new row of CUSTOMERS table */
 INSERT INTO customers (cust_num, company, cust_rep, credit_limit)
 VALUES (@c_num, @c_name, @c_rep, @cred_lim);

 /* Update row of SALESREPS table */
 UPDATE salesreps
 SET quota = quota + quota + @tgt_sls
 WHERE empl_num = @c_rep;

 /* Update row of OFFICES table */
 UPDATE offices
 SET target = target + @tgt_sls
 WHERE city = @c_offc;

 /* Commit transaction and we are done */
 COMMIT TRAN;
END;
```

Poziv procedure:

```sql
EXECUTE ADD_CUST 'XYZ Corporation', 2137, 30000.00, 50000.00, 103, 'Chicago';
EXEC ADD_CUST 'XYZ Corporation', 2137, 30000.00, 50000.00, 103, 'Chicago';
EXEC ADD_CUST @C_NAME = 'XYZ Corporation',
 @C_NUM = 2137,
 @CRED_LIM = 30000.00,
 @C_OFFC = 'Chicago',
 @C_REP = 103,
 @TGT_SLS = 50000.00;
```

## Implementacija u Informix

```sql
/* Add a customer procedure */
CREATE PROCEDURE add_cust (
 c_name VARCHAR(20), /* input customer name */
 c_num INTEGER, /* input customer number */
 cred_lim NUMERIC(16,2), /* input credit limit */
 tgt_sls NUMERIC(16,2), /* input target sales */
 c_rep INTEGER, /* input salesrep emp # */
 c_offc VARCHAR(15)) /* input office city */
AS
BEGIN
 /* Insert new row of CUSTOMERS table */
 INSERT INTO customers (cust_num, company, cust_rep, credit_limit)
 VALUES (c_num, c_name, c_rep, cred_lim);

 /* Update row of SALESREPS table */
 UPDATE salesreps
 SET quota = quota + quota + tgt_sls
 WHERE empl_num = c_rep;

 /* Update row of OFFICES table */
 UPDATE offices
 SET target = target + tgt_sls
 WHERE city = c_offc;

 /* Commit transaction and we are done */
 COMMIT WORK;
END PROCEDURE;
```

Poziv procedure:

```sql
EXECUTE PROCEDURE ADD_CUST('XYZ Corporation', 2137, 30000.00, 50000.00, 103, 'Chicago');
```

Ukoliko se poziva iz druge procedure onda može i sa:

```sql
CALL ADD_CUST('XYZ Corporation', 2137, 30000.00, 50000.00, 103, 'Chicago');
```

## Upotreba promenljivih

Svi dijalekti podržavaju upotrebu lokalnih promenljivih unutar tela procedure. Promenljive se deklarišu odmah nakon zaglavlja, a pre ostalih iskaza.

Na primer, deo procedure koji treba da izračuna ukupan iznos neplaćenih narudžbina za određenog klijenta, i postavljanje jedne od dve poruka u zavisnosti da li je taj iznos ispod ili iznad 30000.


## Implementacija u Oracle (PL/SQL)

Nazivi promenljivih su klasični SQL identifikatori, a dodela se obavlja kroz `SELECT…INTO` naredbu, odnosno koristeći format sličan Pascal programskom jeziku (`:=`).

```sql
/* Check order total for a customer */
CREATE PROCEDURE chk_tot (c_num IN NUMBER)
AS
 /* Declare two local variables */
 tot_ord NUMBER(16,2);
 msg_text VARCHAR(30);
BEGIN
 /* Calculate total orders for requested customer */
 SELECT SUM(amount) INTO tot_ord
 FROM orders
 WHERE cust = c_num;

 /* Load appropriate message, based on total */
 IF tot_ord < 30000.00 THEN
     msg_text := 'high order total';
 ELSE
     msg_text := 'low order total';
 END IF;

 /* Do other processing for message text */
 . . .
END;
```

## Implementacija u SQL Server (T-SQL)

Upotrebljava se `DECLARE` za deklaraciju. Naziv počinje specijalnim karakterom `@`, a dodela se obavlja kroz `SELECT` naredbu, odnosno `(SELECT @promenljiva = …)`.

```sql
/* Check order total for a customer */
CREATE PROC chk_tot
 @c_num INTEGER /* one input parameter */
AS
 /* Declare two local variables */
 DECLARE @tot_ord MONEY, @msg_text VARCHAR(30)
BEGIN
 /* Calculate total orders for customer */
 SELECT @tot_ord = SUM(amount)
 FROM orders
 WHERE cust = @c_num;

 /* Load appropriate message, based on total */
 IF tot_ord < 30000.00
     SELECT @msg_text = 'high order total'
 ELSE
     SELECT @msg_text = 'low order total';

 /* Do other processing for message text */
 . . .
END;
```

## Implementacija u Informix

Upotrebljava se `DEFINE` za deklaraciju (ovaj primer pokazuje samo deo opcija koje postoje). Nazivi promenljivih su kao klasični SQL identifikatori. Dodela se obavlja kroz `SELECT…INTO` naredbu, ili koristeći `LET` iskaz.

```sql
/* Check order total for a customer */
CREATE PROCEDURE chk_tot (c_num INTEGER)
 /* Declare two local variables */
 DEFINE tot_ord NUMERIC(16,2);
 DEFINE msg_text VARCHAR(30);
BEGIN
 /* Calculate total orders for requested customer */
 SELECT SUM(amount) INTO tot_ord
 FROM orders
 WHERE cust = c_num;

 /* Load appropriate message, based on total */
 IF tot_ord < 30000.00 THEN
     LET msg_text = 'high order total';
 ELSE
     LET msg_text = 'low order total';
 END IF;

 /* Do other processing for message text */
 . . .
END PROCEDURE;
```

## Blokovi iskaza

Svi dijalekti podržavaju grupisanje sekvence iskaza u okviru jednog bloka.

## Implementacija u Oracle (PL/SQL)

Sve tri sekcije su opcione.

```sql
/* Oracle PL/SQL statement block */
/* Declaration of any local variables */
DECLARE 
 . . .
BEGIN 
 /* Specify the sequence of statements */
 . . .
EXCEPTION 
 /* Declare handling for exceptions */
 . . .
END;
```

## Implementacija u SQL Server (T-SQL)

Sekcija ima za cilj samo da grupiše iskaze, a ne utiče na doseg i vidljivost lokalnih promenljivih.

```sql
/* Transact-SQL block of statements */
BEGIN
 /* Sequence of SQL statements appears here */
 . . .
END;
```

## Implementacija u Informix

Blok iskaza u ovoj implementaciji ne sadrži samo sekvencu iskaza, već opcionu deklaraciju promenljivih vidljivih samo unutar bloka, kao i sekciju u kojoj se razrešavaju greške i izuzeci. Generalno kod Informix blokovi nisu tako često potrebni kao kod T-SQL zbog toga što su kontrolne strukture sa eksplicitnim krajem (`IF…END IF`, `WHILE…END WHILE`, `FOR…END FOR`), baš kao i kod PL/SQL.

```sql
/* Informix block of statements */
/* Declaration of any local variables */
DEFINE 
 . . .
/* Declare handling for exceptions */
ON EXCEPTION 
 . . .
/* Define the sequence of SQL statements */
BEGIN 
 . . .
END;
```

## Petlje

Svi dijalekti podržavaju razne vrste ponavljanja u izvršavanju.

## Implementacija u Oracle (PL/SQL)

```sql
/* Process each of ten items */
FOR item_num IN 1..10 LOOP
 /* Process this particular item */
 . . .
 /* Test whether to end the loop early */
 EXIT WHEN (item_num = special_item);
END LOOP;
```

## Implementacija u SQL Server (T-SQL)

SQL Server nema `FOR` petlje, ali se isto može postići upotrebom `WHILE` petlji.

```sql
/* Process each of ten items */
WHILE @item_num < 11
BEGIN
 SET @item_num = @item_num + 1;
 /* Process this particular item */
 . . .
 /* Test whether to end the loop early */
 IF (@item_num = special_item)
     BREAK;
 ELSE
     CONTINUE;
END;
```

## Implementacija u Informix

```sql
/* Process each of ten items */
FOR item_num = 1 TO 10 STEP 1
 /* Process this particular item */
 . . .
 /* Test whether to end the loop early */
 IF (item_num = special_item) THEN 
     EXIT FOR;
 END FOR;
```

Oracle i Informix, pored `FOR` poseduju i `WHILE` petlje.

## Ponavljanje koristeći kursore

Svi dijalekti podržavaju upotrebu kursora u slučajevima kada je potrebno obraditi rezultate nekog upita. Kod svih je konceptualno isti niz koraka: deklaracija, otvaranje, dohvatanje, zatvaranje (`DECLARE CURSOR`, `OPEN CURSOR`, `FETCH`, `CLOSE CURSOR`).

## Implementacija u Oracle (PL/SQL)

Za dohvatanje rezultata upita iz kursora koristi se specijalna promenljiva koja je tipa `CURS_ROW` koja odgovara jednom redu kreiranog kursora.

```sql
CREATE PROCEDURE sort_orders()
/* Cursor for the query */
CURSOR o_cursor IS
    SELECT amount, company, name
    FROM orders, customers, salesreps
    WHERE cust = cust_num
      AND rep = empl_num;

/* Row variable to receive query results values */
curs_row o_cursor%ROWTYPE;
BEGIN
    /* Loop through each row of query results */
    FOR curs_row IN o_cursor LOOP
        /* Check for small orders and handle */
        IF curs_row.amount < 1000.00 THEN
            INSERT INTO smallorders
            VALUES (curs_row.name, curs_row.amount);
        /* Check for big orders and handle */
        ELSIF curs_row.amount > 10000.00 THEN
            INSERT INTO bigorders
            VALUES (curs_row.company, curs_row.amount);
        END IF;
    END LOOP;
    COMMIT;
END;
```

## Implementacija u SQL Server (T-SQL)

SQL Server nema specijalizovanu `FOR` petlju za rad sa kursorima, već se kontrola i ponavljanje izvršava proveravanjem sistemske promenljive `@@SQLSTATUS`, koja je ekvivalent standardnom SQLSTATE kodu.

```sql
CREATE PROC sort_orders()
AS
/* Local variables to hold query results */
DECLARE @ord_amt DECIMAL(16,2); /* order amount */
DECLARE @c_name VARCHAR(20);    /* customer name */
DECLARE @r_name VARCHAR(15);    /* salesrep name */

/* Declare cursor for the query */
DECLARE o_curs CURSOR FOR
    SELECT amount, company, name
    FROM orders, customers, salesreps
    WHERE cust = cust_num
      AND rep = empl_num;

BEGIN
    /* Open cursor and fetch first row of results */
    OPEN o_curs;
    FETCH o_curs INTO @ord_amt, @c_name, @r_name;

    /* If no rows, return immediately */
    IF (@@sqlstatus = 2) BEGIN
        CLOSE o_curs;
        RETURN;
    END;

    /* Loop through each row of query results */
    WHILE (@@sqlstatus = 0) BEGIN
        /* Check for small orders and handle */
        IF (@ord_amt < 1000.00) BEGIN
            INSERT INTO smallorders VALUES (@r_name, @ord_amt);
        /* Check for big orders and handle */
        ELSE IF (@ord_amt > 10000.00) BEGIN
            INSERT INTO bigorders VALUES (@c_name, @ord_amt);
        END;
        FETCH o_curs INTO @ord_amt, @c_name, @r_name;
    END;

    /* Done with results; close cursor and return */
    CLOSE o_curs;
END;
```

## Implementacija u Informix

```sql
CREATE PROCEDURE sort_orders()
/* Local variables to hold query results */
DEFINE ord_amt NUMERIC(16,2); /* order amount */
DEFINE c_name VARCHAR(20);    /* customer name */
DEFINE r_name VARCHAR(15);    /* salesrep name */

/* Execute query and process each results row */
FOREACH SELECT amount, company, name
    INTO ord_amt, c_name, r_name
    FROM orders, customers, salesreps
    WHERE cust = cust_num
      AND rep = empl_num
BEGIN
    /* Check for small orders and handle */
    IF (ord_amt < 1000.00) THEN
        INSERT INTO smallorders VALUES (r_name, ord_amt);
    /* Check for big orders and handle */
    ELSIF (ord_amt > 10000.00) THEN
        INSERT INTO bigorders VALUES (c_name, ord_amt);
    END IF;
END;
END FOREACH;
END PROCEDURE;
```

## Vraćanje vrednosti preko parametara

Pored uskladištenih procedura, većina dijalekata podržava i uskladištene korisničke funkcije. Funkcije uvek vraćaju jednu stvar (vrednost, objekat, XML dokument) dok procedura ili ne vraća ništa ili vraća veći broj stvari. Funkcije se obično koriste unutar iskaza za kolone unutar `SELECT` klauzule upita, tako da bivaju pozvane po jednom za svaki red koji se obrađuje. Na primer, funkcija `GET_TOT_ORDS` bi mogla biti pozvana:

```sql
SELECT COMPANY, NAME
FROM CUSTOMERS, SALESREPS
WHERE CUST_REP = EMPL_NUM
  AND GET_TOT_ORDS(CUST_NUM) > 10000.00;
```

## Implementacija u Oracle (PL/SQL)

```sql
/* Return total order amount for a customer */
CREATE FUNCTION get_tot_ords(c_num IN NUMBER)
RETURN NUMBER
AS
/* Declare one local variable to hold the total */
tot_ord NUMBER(16,2);
BEGIN
    /* Simple single-row query to get total */
    SELECT SUM(amount) INTO tot_ord
    FROM orders
    WHERE cust = c_num;
    /* return the retrieved value as fcn value */
    RETURN tot_ord;
END;
```

## Implementacija u SQL Server (T-SQL)

SQL Server takođe ima podršku za funkcije, slično kao kod Oracle i Informix.

```sql
/* Return total order amount for a customer */
CREATE FUNCTION get_tot_ords(@c_num INT)
RETURNS DECIMAL(16,2)
AS
BEGIN
    /* Declare one local variable to hold the total */
    DECLARE @tot_ord DECIMAL(16,2);

    /* Simple single-row query to get total */
    SELECT @tot_ord = SUM(amount)
    FROM orders
    WHERE cust = @c_num;

    /* Return the retrieved value as fcn value */
    RETURN @tot_ord;
END;
```

## Implementacija u Informix

Umesto uvođenja izlaznih parametara, Informix proširuje definiciju funkcija time što omogućava veći broj povratnih vrednosti.

```sql
/* Return total order amount for a customer */
CREATE FUNCTION get_tot_ords(c_num IN INTEGER) RETURNING NUMERIC(16,2)
DEFINE tot_ord NUMERIC(16,2);
BEGIN
    /* Simple single-row query to get total */
    SELECT SUM(amount) INTO tot_ord
    FROM orders
    WHERE cust = c_num;
    /* Return the retrieved value as fcn value */
    RETURN tot_ord;
END FUNCTION;
```

## Vraćanje vrednosti preko parametara

Obično se u slučaju potrebe da se vrati jedna vrednost, koriste uskladištene korisničke funkcije. Međutim, u slučaju kada je potrebno vratiti više vrednosti, većina dijalekata predviđa izlazne parametre.

## Implementacija u Oracle (PL/SQL)

```sql
/* Get customer name, salesrep, and office */
CREATE PROCEDURE get_cust_info(
    c_num IN NUMBER,
    c_name OUT VARCHAR,
    r_name OUT VARCHAR,
    c_offc OUT VARCHAR)
AS
BEGIN
    /* Simple single-row query to get info */
    SELECT company, name, city
    INTO c_name, r_name, c_offc
    FROM customers, salesreps, offices
    WHERE cust_num = c_num
      AND empl_num = cust_rep
      AND office = rep_office;
END;
```

Primer jednog anonimnog bloka u kome se poziva ova procedura je:

```sql
/* Get the customer info for customer 2111 */
DECLARE 
    the_name VARCHAR(20);
    the_rep VARCHAR(15);
    the_city VARCHAR(15);

EXECUTE get_cust_info(2111, the_name, the_rep, the_city);
```
## Implementacija u SQL Server (T-SQL)

```sql
/* Get customer name, salesrep, and office */
CREATE PROCEDURE get_cust_info(
    @c_num INTEGER,
    @c_name VARCHAR(20) OUT,
    @r_name VARCHAR(15) OUT,
    @c_offc VARCHAR(15) OUT)
AS
BEGIN
    /* Simple single-row query to get info */
    SELECT @c_name = company,
           @c_offc = city
    FROM customers, salesreps, offices
    WHERE cust_num = @c_num
      AND empl_num = cust_rep
      AND office = rep_office;
END;
```

Prilikom poziva ovakve procedure, mora se naglasiti koji su parametri izlazni:

```sql
/* Get the customer info for customer 2111 */
DECLARE the_name VARCHAR(20);
DECLARE the_rep VARCHAR(15);
DECLARE the_city VARCHAR(15);

EXEC get_cust_info @c_num = 2111,
                   @c_name = the_name OUTPUT,
                   @r_name = the_rep OUTPUT,
                   @c_offc = the_city OUTPUT;
```

## Implementacija u Informix

Umesto uvođenja izlaznih parametara, Informix proširuje definiciju funkcija time što omogućava veći broj povratnih vrednosti.

```sql
/* Get customer name, salesrep, and office */
CREATE FUNCTION get_cust_info(c_num INTEGER)
RETURNING VARCHAR(20), VARCHAR(15), VARCHAR(15)
DEFINE c_name VARCHAR(20);
DEFINE r_name VARCHAR(15);
DEFINE c_offc VARCHAR(15);
BEGIN
    /* Simple single-row query to get info */
    SELECT company, name, city
    INTO c_name, r_name, c_offc
    FROM customers, salesreps, offices
    WHERE cust_num = c_num
      AND empl_num = cust_rep
      AND office = rep_office;

    /* Return the three values */
    RETURN c_name, r_name, c_offc;
END;
```

Prilikom poziva ovakve funkcije, mora se koristiti specijalna `RETURNING` klauzula.

```sql
/* Get the customer info for customer 2111 */
DEFINE the_name VARCHAR(20);
DEFINE the_rep VARCHAR(15);
DEFINE the_city VARCHAR(15);

CALL get_cust_info(2111) RETURNING the_name, the_rep, the_city;
```

## Obrada grešaka i izuzetaka

Svi dijalekti podržavaju neki način obrade grešaka i izuzetaka.

## Implementacija u Oracle (PL/SQL)

```sql
/* Return total order amount for a customer */
CREATE FUNCTION get_tot_ords(c_num IN NUMBER)
RETURN NUMBER
AS
    /* Declare one local variable to hold the total */
    tot_ord NUMBER(16,2);
BEGIN
    /* Simple single-row query to get total */
    SELECT SUM(amount)
    INTO tot_ord
    FROM orders
    WHERE cust = c_num;

    /* Return the retrieved value as fcn value */
    RETURN tot_ord;
EXCEPTION
    /* Handle the situation where no orders found */
    WHEN no_data_found THEN
        RAISE_APPLICATION_ERROR(-20123, 'Bad cust#');
    /* Handle any other exceptions */
    WHEN OTHERS THEN
        RAISE_APPLICATION_ERROR(-20199, 'Unknown error');
END;
```

## Implementacija u SQL Server (T-SQL)

SQL Server omogućava obradu grešaka upotrebom skupa globalnih promenljivih (njih par od preko 100 drugih globalnih promenljivih koje daju uvid u stanje čitavog servera, transakcija, otvorenih konekcija itd.). Najvažnije promenljive za obradu grešaka su `@@ERROR` koja sadrži status poslednje izvršenog niza iskaza, kao i `@@SQLSTATUS` koja sadrži status poslednje `FETCH` operacije.

## Implementacija u Informix

```sql
/* Return total order amount for a customer */
CREATE FUNCTION get_tot_ords(c_num IN INTEGER)
RETURNING NUMERIC(16,2)
DEFINE tot_ord NUMERIC(16,2);
/* Define exception handler for error #-123 and -121 */
ON EXCEPTION IN (-121, -123)
    /* Do whatever is appropriate here */
    . . .
END EXCEPTION;
ON EXCEPTION
    /* Handle any other exceptions in here */
    . . .
END EXCEPTION;
```

# Okidači

Svi dijalekti podržavaju definiciju okidača, ali se sintaksa i mogućnosti znatno razlikuju.

## Implementacija u Oracle (PL/SQL)

Oracle ima podršku za najraznovrsnije opcije okidača. Podržava `BEFORE` i `AFTER` okidače, kao i `INSTEAD OF` okidače, a sve to na nivou iskaza i na nivou reda. Podržava čak i okidače koji reaguju na događaje na nivou sistema (npr. kada se neki korisnik poveže na bazu, ili kada se izda neka određena komanda nad bazom itd.)

```sql
CREATE TRIGGER bef_upd_ord
BEFORE UPDATE ON orders
BEGIN
    /* Calculate order total before changes */
    old_total = add_orders();
END;

CREATE TRIGGER aft_upd_ord
AFTER UPDATE ON orders
BEGIN
    /* Calculate order total after changes */
    new_total = add_orders();
END;

CREATE TRIGGER dur_upd_ord
BEFORE UPDATE OF amount ON orders
REFERENCING OLD AS pre NEW AS post
/* Capture order increases and decreases */
FOR EACH ROW
WHEN (:post.amount != :pre.amount)
BEGIN
    IF post.amount != :pre.amount THEN
        IF (:post.amount < :pre.amount) THEN
            /* Write decrease data into table */
            INSERT INTO ord_less
            VALUES (:pre.cust, :pre.order_date, :pre.amount, :post.amount);
        ELSIF (:post.amount > :pre.amount) THEN
            /* Write increase data into table */
            INSERT INTO ord_more
            VALUES (:pre.cust, :pre.order_date, :pre.amount, :post.amount);
        END IF;
    END IF;
END;

CREATE OR REPLACE TRIGGER upd_tgt
/* Insert trigger for SALESREPS */
BEFORE INSERT ON salesreps
FOR EACH ROW
BEGIN
    IF :new.quota IS NOT NULL THEN
        UPDATE offices
        SET target = target + new.quota;
    END IF;
END;
```

## Implementacija u SQL Server (T-SQL)

SQL Server pruža podršku za `AFTER` i `INSTEAD OF` okidače, i to samo na nivou iskaza, ali se upotrebom globalne promenljive može proveriti da li je iskaz promenio jedan ili više redova.

```sql
CREATE TRIGGER upd_tgt
/* Insert trigger for SALESREPS */
ON salesreps
FOR INSERT
AS
BEGIN
    IF (@@ROWCOUNT = 1)
    BEGIN
        UPDATE offices
        SET target = target + inserted.quota
        FROM offices, inserted
        WHERE offices.office = inserted.rep_office;
    END
    ELSE
        RAISERROR 23456;
END;

CREATE TRIGGER chk_del_cust
/* Delete trigger for CUSTOMERS */
ON customers
FOR DELETE
AS
BEGIN
    /* Detect any orders for deleted cust #'s */
    IF (SELECT COUNT(*)
        FROM orders, deleted
        WHERE orders.cust = deleted.cust_num) > 0
    BEGIN
        ROLLBACK TRANSACTION;
        PRINT 'Cannot delete; still have orders';
        RAISERROR 31234;
    END;
END;

CREATE TRIGGER upd_reps
/* Update trigger for SALESREPS */
ON salesreps
FOR INSERT, UPDATE
AS
BEGIN
    IF UPDATE(quota)
    BEGIN
        /* Handle updates to quota column */
        . . .
    END;
    IF UPDATE(sales)
    BEGIN
        /* Handle updates to sales column */
        . . .
    END;
END;
```

## Implementacija u Informix

Informix pruža podršku za `BEFORE` i `AFTER` okidače, ali pored podrške za okidače na nivou iskaza, ima podršku i za okidače na nivou reda.

```sql
CREATE TRIGGER new_sls
INSERT ON salesreps . . .

CREATE TRIGGER del_cus_chk
DELETE ON customers . . .

CREATE TRIGGER ord_upd
UPDATE ON orders . . .

CREATE TRIGGER sls_upd
UPDATE OF quota, sales ON salesreps . . .

CREATE TRIGGER upd_ord
UPDATE OF amount ON orders
REFERENCING OLD AS pre NEW AS post
/* Calculate order total before changes */
BEFORE (EXECUTE PROCEDURE add_orders() INTO old_total)
/* Capture order increases and decreases */
FOR EACH ROW
WHEN (post.amount < pre.amount)
    /* Write decrease data into table */
    (INSERT INTO ord_less
     VALUES (pre.cust, pre.order_date, pre.amount, post.amount))
WHEN (post.amount > pre.amount)
    /* Write increase data into table */
    (INSERT INTO ord_more
     VALUES (pre.cust, pre.order_date, pre.amount, post.amount))
/* After changes, recalculate total */
AFTER (EXECUTE PROCEDURE add_orders() INTO new_total);
```
