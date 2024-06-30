## Step-by-Step Guide for Implementing the `SlobodnaProdajaUlaznica` Method in Java

This guide provides a step-by-step explanation of how to implement the `SlobodnaProdajaUlaznica` method in Java based on the provided SQL database schema and insert statements.

**1. Database Connection and Initialization**

* **`connection=DB.getInstance().getConnection();`**: This line establishes a connection to the database using the `DB` class (assumed to be provided). The connection object `connection` is used throughout the method to interact with the database. This is the first step as it's necessary to have a connection to the database before performing any operations.

**2. `AzuriranjeBaze` Method**

* **Purpose**: This private helper method updates the database after a successful ticket purchase.
* **Parameters**:
  * `SifD`: Event ID.
  * `sektor`: Sector ID.
  * `redBroj`: Row number.
  * `sediste`: Seat number.
  * `brojUlaznica`: Number of tickets purchased.
* **Logic**:
    1. **Update `ULAZNICA` Table**: Sets the `Status` of the purchased tickets to 'P' (purchased).

        ```java
        "UPDATE ULAZNICA SET Status='P' " +
                "WHERE SifU IN (SELECT SifU FROM VAZI WHERE SifD=?)  AND SedisteBr>=? AND  SedisteBr<? " +
                "AND SifR IN (SELECT SifR FROM Red WHERE SifS=? AND Broj=?)"
        ```

        * This SQL statement updates the `Status` of tickets in the `ULAZNICA` table. It selects tickets based on the event ID (`SifD`), sector ID (`SifS`), row number (`Broj`), and seat range (`SedisteBr`). The `Status` is set to 'P' for tickets that meet these criteria and belong to the event.
    2. **Update `Dogadjaj` Table**: Decreases the number of remaining tickets for the event.

        ```java
        "UPDATE Dogadjaj set BrojPreostalihUlaznica = BrojPreostalihUlaznica - ? WHERE SifD=?"
        ```

        * This SQL statement updates the `BrojPreostalihUlaznica` field in the `Dogadjaj` table, decreasing it by the number of tickets purchased.
    3. **Error Handling**: Includes a `try-catch` block to handle potential `SQLException` during database operations.
* **Implementation**:

    ```java
    private void AzuriranjeBaze(int SifD, int sektor, int redBroj, int sediste, int brojUlaznica){
        try(PreparedStatement stUpdate=connection.prepareStatement(
                "UPDATE ULAZNICA SET Status='P' " +
                        "WHERE SifU IN (SELECT SifU FROM VAZI WHERE SifD=?)  AND SedisteBr>=? AND  SedisteBr<? " +
                        "AND SifR IN (SELECT SifR FROM Red WHERE SifS=? AND Broj=?)");
                PreparedStatement stUpdateDogadjaj=connection.prepareStatement(
                        "UPDATE Dogadjaj set BrojPreostalihUlaznica = BrojPreostalihUlaznica - ? WHERE SifD=?")
        ){
            stUpdate.setInt(1,SifD);
            stUpdate.setInt(2,sediste);
            stUpdate.setInt(3,sediste+brojUlaznica);
            stUpdate.setInt(4,sektor);
            stUpdate.setInt(5,redBroj);
            stUpdate.executeUpdate();

            stUpdateDogadjaj.setInt(1,brojUlaznica);
            stUpdateDogadjaj.setInt(2,SifD);
            stUpdateDogadjaj.executeUpdate();
        }catch (SQLException s) {
            s.printStackTrace();
        }
    }
    ```

* **Explanation**: This method is implemented to update the database after a successful ticket purchase. It uses two prepared statements: one to update the `ULAZNICA` table and another to update the `Dogadjaj` table. The method sets the `Status` of the purchased tickets to 'P' and decreases the number of remaining tickets for the event in the database.

**3. `KupovinaKarataUJednomRedu` Method**

* **Purpose**: Attempts to purchase tickets within a single row.
* **Parameters**:
  * `SifD`: Event ID.
  * `BrojUlaznica`: Number of tickets to purchase.
* **Logic**:
    1. **Select Suitable Row**: Uses a `PreparedStatement` to select the top row (based on priority) that has enough consecutive available seats.

        ```java
        "SELECT TOP 1  S.SifS,  U.SifR,  R.Broj, U.SedisteBr " +
                "FROM VAZI V JOIN ULAZNICA U ON V.SifU=U.SifU JOIN RED R ON U.SifR=R.SifR JOIN SEKTOR S ON R.SifS=S.SifS " +
                "WHERE V.SifD=? AND ( " +
                "SELECT COUNT(*) FROM VAZI V2 JOIN ULAZNICA U2 ON V2.SifU=U2.SifU WHERE U2.SifR=U.SifR "+
                "AND V2.SifD=? AND U2.SedisteBr<U.SedisteBr+? AND U2.SedisteBr>=U.SedisteBr  AND U2.Status='S' " +
                ")=? ORDER BY S.FaktorS DESC, R.FaktorR DESC, U.SedisteBr DESC"
        ```

        * This SQL statement selects the top row that has enough consecutive available seats. It joins the `VAZI`, `ULAZNICA`, `RED`, and `SEKTOR` tables to retrieve relevant data. It filters for tickets belonging to the event (`SifD`) and checks if there are enough consecutive available seats (`Status='S'`) within the row. The results are ordered by sector priority (`FaktorS`), row priority (`FaktorR`), and seat number in descending order.
    2. **Update Database**: If a suitable row is found, calls the `AzuriranjeBaze` method to update the database.
* **Error Handling**: Includes `try-catch` blocks to handle potential `SQLException` during database operations.
* **Implementation**:

    ```java
    private boolean KupovinaKarataUJednomRedu(int SifD, int BrojUlaznica){
        try (PreparedStatement st = connection.prepareStatement(
                "SELECT TOP 1  S.SifS,  U.SifR,  R.Broj, U.SedisteBr " +
                        "FROM VAZI V JOIN ULAZNICA U ON V.SifU=U.SifU JOIN RED R ON U.SifR=R.SifR JOIN SEKTOR S ON R.SifS=S.SifS " +
                        "WHERE V.SifD=? AND ( " +
                        "SELECT COUNT(*) FROM VAZI V2 JOIN ULAZNICA U2 ON V2.SifU=U2.SifU WHERE U2.SifR=U.SifR "+
                        "AND V2.SifD=? AND U2.SedisteBr<U.SedisteBr+? AND U2.SedisteBr>=U.SedisteBr  AND U2.Status='S' " +
                        ")=? ORDER BY S.FaktorS DESC, R.FaktorR DESC, U.SedisteBr DESC")) {
            st.setInt(1,SifD);
            st.setInt(2,SifD);
            st.setInt(3,BrojUlaznica);
            st.setInt(4,BrojUlaznica);
            try(ResultSet rs=st.executeQuery()){
                if(rs.next()) {
                    AzuriranjeBaze(SifD, rs.getInt(1), rs.getInt(3), rs.getInt(4), BrojUlaznica);
                    return  true;
                }
            }catch (SQLException s) {
                s.printStackTrace();
            }
        } catch (SQLException s) {
            s.printStackTrace();
        }
        return false;
    }
    ```

* **Explanation**: This method attempts to purchase tickets within a single row. It first tries to find a suitable row with enough consecutive available seats using a prepared statement. If a suitable row is found, it calls the `AzuriranjeBaze` method to update the database and mark the tickets as purchased.

**4. `SlobodneUlaznice` Method**

* **Purpose**: Checks if a specific range of seats within a row is available.
* **Parameters**:
  * `SifD`: Event ID.
  * `sektor`: Sector ID.
  * `brojReda`: Row number.
  * `sediste`: Starting seat number.
  * `brojUlaznica`: Number of tickets to check.
* **Logic**:
    1. **Count Available Seats**: Uses a `PreparedStatement` to count the number of available seats (`Status='S'`) within the specified sector, row, and seat range.

        ```java
        "SELECT COUNT(*) " +
                "FROM VAZI V JOIN ULAZNICA U ON V.SifU=U.SifU JOIN RED R ON U.SifR=R.SifR " +
                "WHERE V.SifD=? AND R.SifS=? AND R.Broj=?  AND U.SedisteBr>=? AND U.SedisteBr<?  AND U.Status='S'"
        ```

        * This SQL statement counts the number of available seats (`Status='S'`) within the specified sector, row, and seat range. It joins the `VAZI`, `ULAZNICA`, and `RED` tables to retrieve relevant data.
    2. **Compare Count**: Returns `true` if the count matches the requested number of tickets, indicating availability.
* **Error Handling**: Includes `try-catch` blocks to handle potential `SQLException` during database operations.
* **Implementation**:

    ```java
    public boolean SlobodneUlaznice(int SifD, int sektor, int brojReda, int sediste, int brojUlaznica){
        try (PreparedStatement st = connection.prepareStatement(
                "SELECT COUNT(*) " +
                        "FROM VAZI V JOIN ULAZNICA U ON V.SifU=U.SifU JOIN RED R ON U.SifR=R.SifR " +
                        "WHERE V.SifD=? AND R.SifS=? AND R.Broj=?  AND U.SedisteBr>=? AND U.SedisteBr<?  AND U.Status='S'")) {
            st.setInt(1,SifD);
            st.setInt(2,sektor);
            st.setInt(3,brojReda);
            st.setInt(4,sediste);
            st.setInt(5,sediste+brojUlaznica);
            try(ResultSet rs=st.executeQuery()){
                if(rs.next()) {
                    return  rs.getInt(1)==brojUlaznica;
                }
            }catch (SQLException s) {
                s.printStackTrace();
            }
        } catch (SQLException s) {
            s.printStackTrace();
        }
        return false;
    }
    ```

* **Explanation**: This method checks if a specific range of seats within a row is available. It counts the number of available seats within the specified sector, row, and seat range using a prepared statement. It returns `true` if the count matches the requested number of tickets, indicating availability.

**5. `KupovinaKarataUDvaReda` Method**

* **Purpose**: Attempts to purchase tickets across two adjacent rows.
* **Parameters**:
  * `SifD`: Event ID.
  * `BrojUlaznica`: Number of tickets to purchase.
* **Logic**:
    1. **Select Suitable Row**: Uses a `PreparedStatement` to select the top row (based on priority) that has enough consecutive available seats.
        * Similar to `KupovinaKarataUJednomRedu`, but selects only half the required number of tickets.
    2. **Check Adjacent Row**: For each selected row, checks if the adjacent row (above or below) has the remaining required seats using the `SlobodneUlaznice` method.
        * Handles both even and odd numbers of tickets, adjusting the seat range accordingly.
    3. **Update Database**: If suitable rows are found, calls the `AzuriranjeBaze` method twice to update the database for both rows.
* **Error Handling**: Includes `try-catch` blocks to handle potential `SQLException` during database operations.
* **Implementation**:

    ```java
    private boolean KupovinaKarataUDvaReda(int SifD, int BrojUlaznica){
        try (PreparedStatement st = connection.prepareStatement(
                "SELECT S.SifS,  U.SifR,  R.Broj, U.SedisteBr " +
                        "FROM VAZI V JOIN ULAZNICA U ON V.SifU=U.SifU JOIN RED R ON U.SifR=R.SifR JOIN SEKTOR S ON R.SifS=S.SifS " +
                        "WHERE V.SifD=? AND ( " +
                        "SELECT COUNT(*) FROM VAZI V2 JOIN ULAZNICA U2 ON V2.SifU=U2.SifU WHERE U2.SifR=U.SifR "+
                        "AND V2.SifD=? AND U2.SedisteBr<U.SedisteBr+? AND U2.SedisteBr>=U.SedisteBr  AND U2.Status='S' " +
                        ")=? ORDER BY S.FaktorS DESC, R.FaktorR DESC, U.SedisteBr DESC")) {
            st.setInt(1,SifD);
            st.setInt(2,SifD);
            st.setInt(3,BrojUlaznica/2);
            st.setInt(4,BrojUlaznica/2);
            try(ResultSet rs=st.executeQuery()){
                while(rs.next()) {
                    int sektor=rs.getInt(1);
                    int redBroj=rs.getInt(3);
                    int sediste=rs.getInt(3);
                    if(BrojUlaznica%2==0){
                        if(SlobodneUlaznice(SifD,sektor, redBroj+1,sediste,BrojUlaznica/2)) {
                            AzuriranjeBaze(SifD, sektor, redBroj, sediste, BrojUlaznica / 2);
                            AzuriranjeBaze(SifD, sektor, redBroj+1, sediste, BrojUlaznica / 2);
                            return true;
                        }
                    }
                    else {
   int[][] test_red_sediste=new int[][]{
                            {redBroj+1,sediste},{redBroj+1,sediste-1},
                            {redBroj-1,sediste},{redBroj-1,sediste-1}};
                        for(int i=0; i<test_red_sediste.length; i++){
                            if(SlobodneUlaznice(SifD,sektor, test_red_sediste[i][0],test_red_sediste[i][1],(BrojUlaznica+1)/2)) {
                                AzuriranjeBaze(SifD, sektor, redBroj, sediste, BrojUlaznica / 2);
                                AzuriranjeBaze(SifD, sektor, test_red_sediste[i][0],test_red_sediste[i][1], (BrojUlaznica+1) / 2);
                                return true;
                            }
                        }
                    }
                }
            }catch (SQLException s) {
                s.printStackTrace();
            }
        } catch (SQLException s) {
            s.printStackTrace();
        }
        return false;
    }
    ```

* **Explanation**: This method attempts to purchase tickets across two adjacent rows. It first selects a suitable row with half the required number of tickets. Then, it checks if the adjacent row (above or below) has the remaining required seats using the `SlobodneUlaznice` method. If suitable rows are found, it updates the database for both rows using the `AzuriranjeBaze` method.

**6. `SlobodnaProdajaUlaznica` Method**

* **Purpose**: Main method for purchasing tickets.
* **Parameters**:
  * `NazivDogadjaja`: Event name.
  * `BrojUlaznica`: Number of tickets to purchase.
* **Logic**:
    1. **Retrieve Event ID**: Uses a `PreparedStatement` to retrieve the event ID (`SifD`) based on the event name and current date.

        ```java
        "SELECT TOP 1 SifD FROM DOGADJAJ WHERE Naziv=? AND Datum=CONVERT(DATE, GETDATE())"
        ```

        * This SQL statement retrieves the event ID (`SifD`) based on the event name and current date. It checks if the event exists and if the current date is the event date.
    2. **Check Event Availability**: If the event is not found or the date is not the event date, prints an error message and returns.
    3. **Attempt Purchase**: Calls the `KupovinaKarataUJednomRedu` method first. If successful, prints a success message and returns.
    4. **Attempt Purchase in Two Rows**: If the first attempt fails, calls the `KupovinaKarataUDvaReda` method. If successful, prints a success message and returns.
    5. **Handle Failure**: If both attempts fail, prints a failure message.
* **Error Handling**: Includes `try-catch` blocks to handle potential `SQLException` during database operations.
* **Implementation**:

    ```java
    public void SlobodnaProdajaUlaznica(String NazivDogadjaja, int BrojUlaznica){
        int SifD=-1;
        try (PreparedStatement st = connection.prepareStatement(
                "SELECT TOP 1 SifD FROM DOGADJAJ WHERE Naziv=? AND Datum=CONVERT(DATE, GETDATE())")) {
            st.setString(1,NazivDogadjaja);
            try(ResultSet rs=st.executeQuery()){
                if(rs.next())
                    SifD=rs.getInt(1);
                else {
                    System.out.println("Karte za dogadjaj "+NazivDogadjaja+" nisu u prodaji");
                    return;
                }
            }catch (SQLException s) {
                s.printStackTrace();
            }
        } catch (SQLException s) {
            s.printStackTrace();
        }

        if (KupovinaKarataUJednomRedu(SifD,BrojUlaznica)){
            System.out.println("Karte za dogadjaj "+NazivDogadjaja+" su kupljene u jednom redu");
            return;
        }
        if (KupovinaKarataUDvaReda(SifD,BrojUlaznica)){
            System.out.println("Karte za dogadjaj "+NazivDogadjaja+" su kupljene u dva reda");
            return;
        }
        System.out.println("Karte za dogadjaj "+NazivDogadjaja+" nisu kupljene");
    }
    ```

* **Explanation**: This method is the main method for purchasing tickets. It first retrieves the event ID based on the event name and current date. Then, it attempts to purchase the tickets using the `KupovinaKarataUJednomRedu` method. If this fails, it attempts to purchase the tickets using the `KupovinaKarataUDvaReda` method. The method prints messages indicating the success or failure of the ticket purchase.

**7. `main` Method**

* **Purpose**: Contains test code for the `SlobodnaProdajaUlaznica` method.
* **Logic**:
  * Creates an instance of the `Ispit_jun` class.
  * Calls the `SlobodnaProdajaUlaznica` method with the event name "D1" and the number of tickets "3".
* **Implementation**:

    ```java
    public static void main(String[] args) {
       (new Ispit_jun()).SlobodnaProdajaUlaznica("D1",3);
    }
    ```

* **Explanation**: This method is provided for testing purposes. It creates an instance of the `Ispit_jun` class and calls the `SlobodnaProdajaUlaznica` method with the event name "D1" and the number of tickets "3".

**Implementation Order**

1. **Database Connection and Initialization**: This is the first step as it's necessary to have a connection to the database before performing any operations.
2. **`AzuriranjeBaze` Method**: Implement this method first as it's a helper method used by other methods.
3. **`SlobodneUlaznice` Method**: Implement this method as it's used by the `KupovinaKarataUDvaReda` method.
4. **`KupovinaKarataUJednomRedu` Method**: Implement this method before `KupovinaKarataUDvaReda` as it's a simpler approach to purchasing tickets.
5. **`KupovinaKarataUDvaReda` Method**: Implement this method after `KupovinaKarataUJednomRedu` as it's a more complex approach that relies on the `SlobodneUlaznice` method.
6. **`SlobodnaProdajaUlaznica` Method**: Implement this method last as it's the main method that calls other methods for ticket purchase.
7. **`main` Method**: Implement this method at the end for testing purposes.

**Explanation of the Logic**

The `SlobodnaProdajaUlaznica` method implements the following logic:

1. **Event Validation**: Checks if the event exists and if the current date is the event date.
2. **Ticket Purchase**: Attempts to purchase tickets in the following order:
    * **Single Row**: Tries to find a row with enough consecutive available seats.
    * **Two Rows**: If a single row is not available, tries to find two adjacent rows with enough seats.
3. **Database Update**: If a suitable seat arrangement is found, updates the database to mark the tickets as purchased and decrease the remaining ticket count for the event.
4. **Output**: Prints messages indicating the success or failure of the ticket purchase.

**Important Notes**

* The `DB` class is assumed to be provided and handles database connection details.
* The code includes error handling using `try-catch` blocks to handle potential `SQLException`.
* The `main` method is provided for testing purposes and can be modified to test different scenarios.

This step-by-step guide provides a comprehensive understanding of the `SlobodnaProdajaUlaznica` method implementation. By following these steps, you can successfully implement the method and achieve the desired functionality.
