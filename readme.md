1. pip install flask
2. python ./app.py
3. 数据库说明

   数据库——zgllm

   数据表——student

   用户名——root

   密码——123456

   | id   | sid       | password | email     |
   | ---- | --------- | -------- | --------- |
   | 自增 | 学号 唯一 |          | 邮箱 唯一 |

   ```msysql
    CREATE TABLE student (
       id INT AUTO_INCREMENT PRIMARY KEY, 
       sid VARCHAR(50) UNIQUE NOT NULL, 
       email VARCHAR(100) UNIQUE, 
       password VARCHAR(255)
   );
   ```

   
