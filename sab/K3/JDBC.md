# JDBC

JDBC, which stands for Java Database Connectivity, is an API (Application Programming Interface) in the Java programming language that defines how a client may access a database. It provides methods for querying and updating data in a database. Here are some key points about JDBC:

1. **Purpose**: JDBC allows Java applications to interact with a wide range of databases (like MySQL, Oracle, SQL Server, etc.) in a standard way, without having to worry about database-specific details.

2. **Components**:
   - **JDBC Driver**: A software component that enables Java applications to interact with a database. Different databases require different drivers.
   - **Connection**: Represents a session with a specific database. Connections are used to send SQL statements to the database.
   - **Statement**: An interface that represents an SQL statement. It can be used to execute SQL queries against the database.
   - **ResultSet**: Represents the result set of a query. It maintains a cursor pointing to its current row of data.
   - **SQLException**: An exception that provides information on a database access error or other errors.

3. **Process**:
   - Load the JDBC driver.
   - Establish a connection to the database using `DriverManager`.
   - Create a `Statement` or `PreparedStatement` object to send SQL queries.
   - Execute queries and obtain results.
   - Process the results using `ResultSet`.
   - Close the `ResultSet`, `Statement`, and `Connection` objects to free resources.

4. **Advantages**:
   - **Platform Independence**: Since JDBC is part of the Java platform, it allows applications to be platform-independent.
   - **Wide Range of Database Support**: JDBC drivers are available for almost all popular databases.
   - **Simplicity and Flexibility**: The API is straightforward and provides powerful capabilities to manage database interactions.

## Primeri

### 1. Connecting to a Database

- In order to connect to the database we create the `DB.java` as follows:

    ```java
    package vezbe_jdbc_8;

    import java.sql.*;
    import java.util.logging.Level;
    import java.util.logging.Logger;

    public class DB {

        private static final String username = "new_user";  // SQL Server username
        private static final String password = "123";  // SQL Server password
        private static final String database = "Trznicentar";  // Database name 
        private static final int port = 1433; // Database port
        private static final String server = "localhost"; 

        private static final String connectionUrl
                = "jdbc:sqlserver://" + server + ":" + port
                + ";databaseName=" + database
                + ";encrypt=true"
                + ";trustServerCertificate=true";

        private Connection connection; // this class is a singleton, there can ever be one Connection object. 

        public Connection getConnection() {
            return connection;
        }

        private DB() {
            try {
                connection = DriverManager.getConnection(connectionUrl, username, password);
            } catch (SQLException ex) {
                Logger.getLogger(DB.class.getName()).log(Level.SEVERE, null, ex);
            }
        }

        private static DB db = null;

        public static DB getInstance() {
            if (db == null) {
                db = new DB();
            }
            return db;
        }
    }


    ```

- Lets test if we have established the connection

    ```java

    package vezbe_jdbc_8;

    /**
    *
    * @author ziga
    */
    import java.sql.*; // importing connection

    // Testing the connection with the database
    public class Primer1 {
        public static void main(String[] args) {
            Connection conn = DB.getInstance().getConnection();
            
            if (conn == null) {
                System.out.println("Connection could not be made!");
            } else {
                System.out.println("Connection established!");
            }
        }
    }


    ```

### 2. Priting out an entire table of data form the database, Radnik

- In this example we use a few new things. Statement, ResultSet, ResultSetMetaData
- ResultSet
  - Purpose: ResultSet is used to hold the data returned by a database query.
  - Usage: It acts as a pointer to one row of a set of results from a SQL query. The ResultSet object maintains a cursor pointing to its current row of data.
  - Navigation: You can move the cursor using methods like next(), previous(), first(), last(), etc.
- ResultSetMetaData
  - Purpose: ResultSetMetaData provides information about the types and properties of the columns in a ResultSet.
  - Usage: It is used to obtain information about the number, types, and properties of the columns in a ResultSet object.
  - Retrieving Metadata: You can get metadata information using methods such as getColumnCount(), getColumnName(), getColumnType(), etc.
- Statement Interface
  -Purpose: The Statement interface is used for executing a static SQL statement and returning the results it produces.
  -Usage: It is created using a Connection object, and it can execute both queries that return results (like SELECT statements) and queries that modify data (like INSERT, UPDATE, DELETE statements).

    ```java

    package vezbe_jdbc_8;

    /**
     *
     * @author ziga
     */

    import java.sql.*;
    import java.util.logging.Level;
    import java.util.logging.Logger;

    // Printing an entire table from the database, ispisRadnika
    public class Primer2 {
        public static void main(String[] args) {
            // establishin connection
            Connection conn = DB.getInstance().getConnection();
            if(conn == null)System.out.println("Connection could not be made!");
            else System.out.println("Connection established!");
            
            try (Statement stmt = conn.createStatement();
                ResultSet rs = stmt.executeQuery("Select * from Radnik");){
                
                ResultSetMetaData rsmd = rs.getMetaData();
                int columnCount = rsmd.getColumnCount(); // get the number of coulmns for the table. 
                
            
                // Print table header
                for (int i = 1; i <= columnCount; i++) {
                    System.out.print(String.format("%-18s", rsmd.getColumnName(i)));
                }
                
                System.out.println();
                
                // Print data
                while(rs.next()){
                    for (int i = 1; i <= columnCount; i++) {
                        System.out.print(String.format("%-18s", rs.getObject(i).toString()));
                    }
                    System.out.println();
                }
            }catch (SQLException ex) {
                Logger.getLogger(DB.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }


    ```

### 3. Priting out a list of tables and columns in the database

- DatabaseMetaData
  - Purpose: DatabaseMetaData provides methods to get metadata about the database, including information about its structure, capabilities, and supported features.
  - Usage: It is typically used when you need to understand the database's characteristics, such as its supported SQL grammar, its stored procedures, and its tables and columns.

    ```java
    package vezbe_jdbc_8;

    /**
    *
    * @author ziga
    */

    import java.sql.*;
    import java.util.logging.Level;
    import java.util.logging.Logger;

    // Priting out a list of tables and columns in the database, using DatabaseMetaData
    public class Primer3 {
        
        public static void main(String[] args) {
            spisakTabela();
        }

        private static void spisakTabela() {
            Connection conn = DB.getInstance().getConnection();
            if(conn == null) System.out.println("Connection could not be made!");
            else System.out.println("Connection established!");
            
            try {
                // 1 - Get the database metadata
                // 2 - Get the tables list
                // 3 - Get the columns for that table
                DatabaseMetaData dbmd = conn.getMetaData();
                try(ResultSet rs = dbmd.getTables(null, "dbo", null, null);){
                    int i = 1;
                    
                    while(rs.next()){
                        // Get the table
                        String tableName = rs.getString("TABLE_NAME");
                        System.out.println(tableName);
                        
                        // Get the columns for that table
                        try (ResultSet rs2 = dbmd.getColumns(null, null, tableName, null);){
                            while(rs2.next()){
                                System.out.println("   - "+ rs2.getString("COLUMN_NAME"));
                            }
                        }}}                
            } catch (SQLException ex) {
                Logger.getLogger(Primer3.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }

    ```

### 4. This example demonstrates how to use DatabaseMetaData to list stored procedures and functions

- Get a list of all the stored procedures and functions in the database

    ```java
    package vezbe_jdbc_8;

    /**
    *
    * @author ziga
    */
    import java.sql.*;
    import java.util.logging.Level;
    import java.util.logging.Logger;

    public class Primer4 {
            
        public static void main(String[] args) {
            listofProceduresAndFunctions();
        }

        private static void listofProceduresAndFunctions() {
            Connection conn = DB.getInstance().getConnection();
            if(conn==null)System.out.println("Connection could not be established!");
            else System.out.println("Connection Established!");
            
            try {
                DatabaseMetaData dbmd = conn.getMetaData();
                try(ResultSet rs = dbmd.getProcedures(null, "dbo", null);){
                    while(rs.next()){
                        System.out.println(rs.getString("PROCEDURE_NAME"));
                    }
                }
            } catch (SQLException ex) {
                Logger.getLogger(DB.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }

    ```

### 5. This example shows how to insert data into a table and retrieve automatically generated keys

- dodaj Trzni Centar Sa Automatski Generisanim ID
    ```java
    package vezbe_jdbc_8;
    /**
    *
    * @author ziga
    */

    import java.sql.*;
    import java.util.logging.Level;
    import java.util.logging.Logger;

    public class Primer5 {
        
        public static void main(String[] args) {
            dodajTrzniCentarSaAutomatskiGenerisanimID("TrzniCentar 7", 
                    "09:00-21:00", 
                    8,
                    456.54,
                    "Beograd",
                    "Vojvode Stepe", 
                    "39");
        }

        private static void dodajTrzniCentarSaAutomatskiGenerisanimID(
                String ime, 
                String vreme, 
                int brojSpratova,
                double povrsina,
                String grad, 
                String ulica, 
                String broj
        ) {
            Connection conn = DB.getInstance().getConnection();
            if(conn == null) System.out.println("Connection could not be made!");
            else System.out.println("Connection established!");

            String query = "INSERT into TrzniCentar (Naziv, RadnoVreme, BrojSpratova, PovrsinaSprata," +
                    "Grad, Ulica, Broj) values(?, ?, ?, ?, ?, ?, ?)";

            
            try (PreparedStatement ps = conn.prepareStatement(query, PreparedStatement.RETURN_GENERATED_KEYS)){
                ps.setString(1, ime);
                ps.setString(2, vreme);
                ps.setInt(3, brojSpratova);
                ps.setDouble(4, povrsina);
                ps.setString(5, grad);
                ps.setString(6, ulica);
                ps.setString(7, broj);
                
                ps.executeUpdate();
                ResultSet rs = ps.getGeneratedKeys();
                
                if(rs.next()){
                    System.out.println("Kreiran je novi Trzni Centar kome je automatski dodeljen Id " + rs.getInt(1));
                }
            } catch (SQLException ex) {
                Logger.getLogger(Primer5.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }

    ```

### 6. This example demonstrates a more complex SELECT query with joins

- ispis Vlasnika
  
    ```java
    
 
    package vezbe_jdbc_8;

    /**
     *
    * @author ziga
    */
    import java.sql.*;
    import java.util.logging.Level;
    import java.util.logging.Logger;

    public class Primer6 {
        
        public static void main(String[] args) {
            ispisVlasnika();
        }

        private static void ispisVlasnika() {
            Connection conn = DB.getInstance().getConnection();
            if(conn == null) System.out.println("Connection could not be made!");
            else System.out.println("Connection established!");
            
            String query = "Select * from Radnik join Vlasnik on Radnik.BrLicneKarte=Vlasnik.RadnikId";
            
            try(
                PreparedStatement stmt = conn.prepareStatement(query);
                ResultSet rs = stmt.executeQuery();
                    ){
                System.out.println("Vlasnici");
                while(rs.next()){
                    System.out.println(rs.getString("Ime")+ rs.getString("Prezime")+ rs.getString("Ulica"));
                }
            }catch (SQLException ex) {
                Logger.getLogger(DB.class.getName()).log(Level.SEVERE, null, ex);
            }
            
        }
    }

    
    ```

### 7 - This example demonstrates calling a stored procedure that returns a ResultSet.

- radniciSaImenom

    ```java

    package vezbe_jdbc_8;

    /**
     *
     * @author ziga
     */

    import java.sql.*;
    import java.util.logging.Level;
    import java.util.logging.Logger;
    public class Primer7 {
        
        public static void main(String[] args) {
            radniciSaImenom("Ivan");
        }

        private static void radniciSaImenom(String ime) {
            Connection conn = DB.getInstance().getConnection();
            if(conn==null) System.out.println("Could not connect to DB!");
            else System.out.println("Connection to db established!");
            
            try {
                // Get a list of procedures
                DatabaseMetaData dbmd = conn.getMetaData();
                try(ResultSet rs=dbmd.getProcedures(null, "dbo", null);){
                    while(rs.next())
                        System.out.println(rs.getString("PROCEDURE_NAME"));
                }
                
                String query = "{ call SPRadniciSaImenom(?)}";
                try(CallableStatement cs = conn.prepareCall(query);)
                {
                    cs.setString(1, ime);
                    try(ResultSet rs3 = cs.executeQuery()){
                        System.out.println("Radnici sa imenom "+ ime);
                        while(rs3.next()){
                            System.out.println("BrLicneKarte: "+ rs3.getString("BrLicneKarte"));
                            System.out.println("Ime: "+ rs3.getString("Ime"));
                            System.out.println("Prezime: "+ rs3.getString("Prezime"));
                        }
                    }
                }
            } catch (SQLException ex) {
                Logger.getLogger(Primer7.class.getName()).log(Level.SEVERE, null, ex);
            }
            
            
            
        }
        
    }


    ```

### 8 - This example shows how to call a stored procedure that has an output parameter

- The procedure is as follows:

    ```sql
    USE [Trznicentar]
    GO
    /****** Object:  StoredProcedure [dbo].[SPBrojRadnikaSaImenom]    Script Date: 6/30/2024 9:22:33 PM ******/
    SET ANSI_NULLS ON
    GO
    SET QUOTED_IDENTIFIER ON
    GO

    ALTER PROCEDURE [dbo].[SPBrojRadnikaSaImenom]
        @ime VARCHAR(20),
        @brojRadnika INT OUTPUT
    AS
    BEGIN
        SET NOCOUNT ON;

        SELECT @brojRadnika = COUNT(*) 
        FROM Radnik 
        WHERE Ime = @ime;
    END;

    ```

    ```java
    package vezbe_jdbc_8;

    /**
     *
     * @author ziga
     */
    import java.sql.*;
    import java.util.logging.Level;
    import java.util.logging.Logger;

    public class Primer8 {
        public static void main(String[] args) {
            int brojRadnika = brojRadnikaSaImenom("Ivan");
            System.out.println(brojRadnika);
        }

        private static int brojRadnikaSaImenom(String ime) {
            
            Connection conn = DB.getInstance().getConnection();
            if(conn==null)System.out.println("Connection could not be established!");
            else System.out.println("Connection Established!");
            
            String query = "{ call SPBrojRadnikaSaImenom (?,?)}";
            
            try(CallableStatement cs = conn.prepareCall(query)){
                cs.setString(1, ime);
                cs.registerOutParameter(2, Types.INTEGER);
                cs.execute();
                return cs.getInt(2);
                
            }catch (SQLException ex) {
                Logger.getLogger(DB.class.getName()).log(Level.SEVERE, null, ex);
            }
            return 0;
        }
    }


    ```

### 9 - This example demonstrates updating rows in a ResultSet using an updatable ResultSet.

- izmenaAdreseVlasnika

```java


```


- [x] 1 -Testing connection

- [x] 2 - ispisRadnika

    This example demonstrates a basic SELECT query with simple data retrieval and output using a ResultSet.
    Concepts: Connection, Statement, ResultSet, ResultSetMetaData.

- [x] 3 - spisakTabela

    This example shows how to use DatabaseMetaData to list tables and columns in the database.
    Concepts: Connection, DatabaseMetaData, ResultSet.

- [x] 4 - spisakProceduraIFunkcija

    This example demonstrates how to use DatabaseMetaData to list stored procedures and functions.
    Concepts: Connection, DatabaseMetaData, ResultSet.

- [x] 5 - dodajTrzniCentarSaAutomatskiGenerisanimID

    This example shows how to insert data into a table and retrieve automatically generated keys.
    Concepts: Connection, PreparedStatement, executeUpdate, getGeneratedKeys.

- [x] 6 - ispisVlasnika

    This example demonstrates a more complex SELECT query with joins.
    Concepts: Connection, PreparedStatement, ResultSet.

- [x] radniciSaImenom

    This example demonstrates calling a stored procedure that returns a ResultSet.
    Concepts: Connection, CallableStatement, ResultSet.

- [x] brRadnikaSaImenom

    This example shows how to call a stored procedure that has an output parameter.
    Concepts: Connection, CallableStatement, registerOutParameter, execute.

- [ ] izmenaAdreseVlasnika

    This example demonstrates updating rows in a ResultSet using an updatable ResultSet.
    Concepts: Connection, PreparedStatement, ResultSet, ResultSet.TYPE_FORWARD_ONLY, ResultSet.CONCUR_UPDATABLE.

- [ ] dodajAdresuBezAutomatskiGenerisanogID

    This example combines checking for existing data and inserting new data if it doesn't exist.
    Concepts: Connection, PreparedStatement, ResultSet, executeQuery, executeUpdate.
