--**Query #1**<br><br>
Find the longest ongoing project for each department.
```sql
    SELECT name, 
    	   AGE(end_date,start_date) as Duration
    FROM projects
    ORDER BY Duration DESC;
```

| name            | duration        |
| --------------- | --------------- |
| IT Project 1    | [object Object] |
| Sales Project 1 | [object Object] |
| HR Project 1    | [object Object] |

--------------------------------------------------------------------------------------------
--**Query #2**<br><br>
Find all employees who are not managers.
```sql
    SELECT name, 
    	   job_title
    FROM employees
    WHERE job_title NOT LIKE '%Manager';
```

| name          | job_title       |
| ------------- | --------------- |
| Bob Miller    | HR Associate    |
| Charlie Brown | IT Associate    |
| Dave Davis    | Sales Associate |

--------------------------------------------------------------------------------------------
--**Query #3**<br><br>
Find all employees who have been hired after the start of a project in their department.
```sql
    SELECT employees.name, 
    	   employees.hire_date
    FROM employees
    JOIN projects ON
    employees.department_id = projects.department_id
    WHERE employees.hire_date > projects.start_date;
```

| name       | hire_date                |
| ---------- | ------------------------ |
| Dave Davis | 2023-03-15T00:00:00.000Z |

--------------------------------------------------------------------------------------------
--**Query #4**<br><br>
Rank employees within each department based on their hire date (earliest hire gets the highest rank).
```sql
    SELECT name, 
    	   department_id,
    	   job_title,
           RANK() OVER (PARTITION BY department_id ORDER BY hire_date)
    FROM employees;
```

| name          | department_id | job_title       | rank |
| ------------- | ------------- | --------------- | ---- |
| John Doe      | 1             | HR Manager      | 1    |
| Bob Miller    | 1             | HR Associate    | 2    |
| Jane Smith    | 2             | IT Manager      | 1    |
| Charlie Brown | 2             | IT Associate    | 2    |
| Alice Johnson | 3             | Sales Manager   | 1    |
| Dave Davis    | 3             | Sales Associate | 2    |

--------------------------------------------------------------------------------------------
--**Query #5**<br><br>
Find the duration between the hire date of each employee and the hire date of the next employee hired in the same department.
```sql
    SELECT e1.id, e1.name, e1.hire_date, (MIN(e2.hire_date) - e1.hire_date) as Duration
    FROM employees AS e1
    JOIN employees AS e2 ON
    e1.department_id = e2.department_id AND
    e1.hire_date < e2.hire_date
    GROUP BY e1.id, e1.name, e1.hire_date
    ORDER BY e1.id;
```

| id  | name          | hire_date                | duration |
| --- | ------------- | ------------------------ | -------- |
| 1   | John Doe      | 2018-06-20T00:00:00.000Z | 1045     |
| 2   | Jane Smith    | 2019-07-15T00:00:00.000Z | 1174     |
| 3   | Alice Johnson | 2020-01-10T00:00:00.000Z | 1160     |

---

[View on DB Fiddle](https://www.db-fiddle.com/f/xckGL9ZW73A6FWhsmPogm7/6)
