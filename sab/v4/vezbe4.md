#### Create database 
```sql
Create database proba2;
```


#### Change the name of the database

```sql
Alter database Proba2 Modify name = Proba2Izmenjeno

Execute sp_renamed 'Proba2', 'Proba2Izmenjeno'
```

#### Delete database

```sql 
Drop database Proba2Izmenjeno
```

#### Creating new Table

```sql 

USE [Proba]
go
Create table Pol (
    Id int Primary Key, 
    Tip varchar(5) Not NULL
)
```
```sql
Use [Proba] go - Defines the database where the queries will run. 
```








