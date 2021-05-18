#HW2 Shrouq Trad Al-Fuqahaa 20208075  

WE want to use apache airflow implementation to extracts csv file from postgresql DataBase 
then send it to mongoDB as JSON file 

1- mkdir plugins dags data logs  
2- to initialize the workflow:  
`docker-compose up -d airflow-init`
3-we used sql "read_script" file to create a table in postgresql also copy a csv file to that table

4- `docker-compose up -d` # d : mean run in the background 
5- copy the sql read_script and data inside the container & execute the sql query
`docker cp ./read_script.sql de_postgres:/file.sql`
`docker cp ./INPUT.csv de_postgres:/file.csv`
`docker exec -u postgres de_postgres psql postgres postgres -f /file.sql `
`docker exec airflow mkdir -p /home/airflow/data`

6- check the dag [GAG_HW2](./dags/dag.py)

7- to access  airflow from (http://localhost:8080)
username/password shrouq/shrouq

8- click on trigger and run the dag [GAG_HW2]
9- now you have json file converted from csv file in data folder   
