# School NSTP Management System

A web-based NSTP (National Service Training Program) Management System designed to streamline the administration of NSTP activities in educational institutions.

![Repo Size](https://img.shields.io/github/repo-size/whoisdmathz/capstone-ug-2024-nstp-management.svg)

<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/26665b60-6980-424f-bc8e-f05e855b1203" width="300"/></td>
    <td><img src="https://github.com/user-attachments/assets/87512a4b-d488-4691-9e17-b148e9bc5040" width="300"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/47c65522-22e1-46d3-bd69-7ed14fcf0e06" width="300"/></td>
    <td><img src="https://github.com/user-attachments/assets/a9af9efc-7884-4d0b-96b5-ea11ab4eb604" width="300"/></td>
  </tr>
</table>

### Key Features 
- Admin Dashboard
    - Manage NSTP Heads
    - Oversee system-wide configurations
- NSTP Head Portal
    - Manage and monitor student lists
    - Record attendance, exams, and performance scores
- Student Portal
    - View enrollment status, NSTP progress, and grades

--- 

## ⚡ Run on windows

### Prerequisite
- Xampp
    - Apache (Running) 
    - MySQL/MariaDB (Running)
- Cloned project
- Composer

### Database Setup
- Run xampp control panel then start apache and mysql
- Open [PhpMyAdmin](http://localhost/phpmyadmin/) in your browser, then create new database name.
- Import the database from **<project_path>/db/** directory

### App Configurations 
- Open project in your preferred IDE(e.g., VS Code)
- Rename the file **.env.example** to **.env**
    - Update the MySQL credentials:
    ```bash
    database.tests.hostname = localhost
    database.tests.database = ci4_test
    database.tests.username = root
    database.tests.password = root
    database.tests.DBDriver = MySQLi
    database.tests.DBPrefix =
    database.tests.port = 3306
    ```
    - Update the Email Server credentials, you can get email server credentials using this [tutorial](https://youtu.be/sEUFIACn9cs):
    ```bash
    email.fromEmail = johndoe@gmail.com
    email.fromName = eBMWD
    email.protocol = smtp
    email.SMTPHost = smtp.gmail.com
    email.SMTPUser = johndoe@gmail.com
    email.SMTPPass = nqulaclmcjtlrkzk
    email.SMTPPort = 465
    email.mailType = html
    email.SMTPCrypto = ssl
    ```

### Run 
- Open terminal and change directory to the project
```bash
cd <project_path>
```
- Install libraries
```bash
composer install
```
- Run project
```bash
php spark serve --host 0.0.0.0
```
- You can now access the app through [localhost](http://localhost:8080) or using network **<computer_ipaddress>:8080**
- Log In using default admin account
    - Username: **admin**
    - Password: **123**

---
