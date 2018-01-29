# MiniSql Engine 

## Input format:
* run 201501164.sh using following ways:
	* bash 201501164.sh 
	* ./201501164.sh
* entire sql statements -- only select, from , where are only feasible
* exit :-- used to terminate minisql shell
* Data in database can only be integers to be able to satisfy all the functions

## Bash features
* set -f  :--- helps in avoiding interpretation of special characters like * for ls expansion"


## Types of queries

* project records​ : ​ select * from table_name;
* Aggregrate Functions: simple aggregrate functions like sum,avg,min,max,count.
* Select/project with distinct from one table​ : ​ select distinct col1, col2 from table_name;
* where conditions are allowed.