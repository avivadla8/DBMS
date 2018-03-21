select count(*) from students;
select year(dob) as year from students group by year(dob) having count(*)>1 order by year(dob);
select name,sid from students where name LIKE 'S%' OR name LIKE 'A%' order by name,sid;
select name from students order by gpa desc limit 5;
select c.name,s.name from courses as c,student_courses as st,students as s where st.grade = "F" and c.cid=st.cid and s.sid = st.sid order by c.name,s.name;
select max(gpa)-min(gpa) as diff from students;
select s1.sid as S1,s2.sid as S2 from students s1,students s2 where abs(s1.gpa-s2.gpa)<1 and s1.sid<s2.sid order by s1.sid,s2.sid;
select name from students where (month(dob)=2 and day(dob)>=18) or (month(dob)=3 and day(dob)<=20) order by name;
select name from students where dayname(dob)="Friday" and week(dob)>26 and gpa>(select avg(gpa) from students) order by name;

