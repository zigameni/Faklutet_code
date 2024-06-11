### date_time
```sql 
select month(getdate());

select year(CURRENT_TIMESTAMP)

select DATEDIFF(year, '01/07/2019', getdate());

```

### calculate your age
    input date is in the format: month/day/year
```sql

CREATE FUNCTION izracunajBrojGodina
(
	@DatumRodjenja Date
)
RETURNS int
AS
BEGIN
	declare @godina int
	set @godina = DATEDIFF(year, @DatumRodjenja, getdate());

	if(MONTH(getDate()) < MONTH(@DatumRodjenja) or 
	(month(getDate()) = MONTH(@DatumRodjenja) and day(getdate()) < day(@DatumRodjenja)))
		set @godina = @godina -1;

	return @godina;

END
GO

select dbo.izracunajBrojGodina('12/03/1997');

```