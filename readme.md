<h1 style="display: flex; align-items: center; justify-content: center;">
<img src="software_icon.ico" alt="App Icon" width="40">
<span>Online Examinator</span>
</h1>

## 📝 Description
This program is intended for undertaking *online MCQ examinations in a networked environment* with efficiency.
The main features and working process is as follows:

### 📌 User Registration

System administer allows registering a number of users by giving them unique user IDs and passwords.
These credentials provide rights to only select users to enable access on the hosting of the question paper.

### 📌 Question Paper Creation & Hosting

Make and host a question paper with the help of the software. Through the local IP address and credentials provided to users they can logon. Users do not even have to install any software or sign up for an account. Just give them the logon accounts that have already been made and the local IP address of the host so that they can take part of the test.

### 📌 Result Management

The moment the user completed and submitted, results are automatically saved for that particular user.

It enables the printing and distribution of individual marksheets with HTML format to allow A4 pages printing also it allows exporting the overall results of all the participants in Excel or csv format for analysis.

### 📌 Automatic Exam cut-off

A timer can also be added while starting the exam so that as soon as times up exam gets turned off and the users who haven't submitted will got screen of *times up*.

### 📌 Resubmittion Control

While starting the exam or even while its running you can control weather a user can resubmit there answer or not.

## 🎬 Screenshots
> Home Tab
![Home Page](/screenshots/A.png)

> Paper Hosting Tab
![Home Page](/screenshots/B.png)

> Create Question Paper Tab
![Home Page](/screenshots/C.png)

> Edit Question Paper Tab
![Home Page](/screenshots/D.png)

> Register Users Tab
![Home Page](/screenshots/E.png)

## ✨ Features
- Question paper import from text file.
- To make user registration simple this software allows to import data of students from external excel file.
- Nearly all the data is editable.
- Result of any perticular user can be exported in HTML format which can later be printed.
- Overall result of all user with an excel file can also be exported.
- All the data of software is stored in JSON format so that person having even little knowledge of programming can understand and change it.
- No user need to install any software to participate in exam, admin will just host exam through this system over there network and they can attend the exam using web browser.
- While hosting exam admin has full control over `allowing resubmittion` and `auto stop if timer ends`
- Logs of each submittion can be traced.

## ⚙️ Installation
🚀 [Download](https://drive.google.com/file/d/1VZKQHKW-CWbZ8IPhOLnZjjiXlbHmAcsp/view?usp=sharing) installer for windows 10 or higher.

## 🌐 Technologies Used
### 📌 Programming Languages
- Python
- HTML, CSS
- JavaScript
- React
### 📌 Frameworks and libraries
- Flask
- Pandas
- React JS
- Flask-SocketIO
- Tkinter
- os
- json
- Iconir
### 📌 Data Formats
- Excel
- CSV
- JSON
### 📌 Web Technologies
- HTTP protocol
- Websockets
- Fetch API

## 🗐 File Structure
```
> 📂 assets
Assets folder contains icons, HTML layouts (specially for result in version 1) etc.
```
```
> 📂 frontend
Its react's project folder having all the frontend that user sees when they attempt exam using web browser.
```
```
> 📂 json_files
This folder contains json files regarding (subjects for now) which software uses in runtime but not writes in these files (read only), in feature planned to add more if needed.
```
```
> 📄 main.py
This main code file serves as the core of the application.

To maintain a clean and organized structure, I have divided the application into multiple Python files, each handling a specific window or functionality. Initially, I considered coding everything in a single file, but as the application grew, it became too messy to manage.

To address this, I adopted an object-oriented programming (OOP) approach and modularized the code into separate files. This not only improved readability but also made the application easier to maintain and extend.

The code for qp_window might seem a bit complex or unorganized because it was the first window I developed for this software before refining my approach to use OOP and modularization.
```

## 🛠 Process of EXE formation
If you have downloaded my code and like to create exe by your self so please note that if you directly created EXE and tried to run so it will cause error.

Follow the following steps to generate EXE properly:-
1. Create a new folder on desktop or where ever you like.
2. Go in frontend folder and open CMD there (I am assuming that you have react js setup on your PC) and run command `npm run build`
3. This will create build folder, copy all the content of build folder and paste it in the folder created in step 1
4. Then come the folder where main.py and open cmd there and run the following commands:-
    - `pip install gevent gevent-websocket`
    - `PyInstaller --icon=software_icon.ico --onefile main.py`
    - `pip uninstall gevent gevent-websocket -y`
5. You will get dist folder, go there and copy the main.exe and paste it in folder created in step 1.
6. Copy assets, json_files, software_icon.ico in the folder created in step 1.
7. Run the exe just copied and you are good to go.

## 🔑 License
This project is licensed under the [MIT License](LICENSE.txt).  
See the `LICENSE` file for more details.

## 💬 Contact
> <a href='https://www.instagram.com/powerpizza67695/'><img src="https://img.icons8.com/?size=100&id=32323&format=png&color=000000" alt="App Icon" width="40"></a>

> <a href='https://www.youtube.com/@Code2EXE'><img src="https://img.icons8.com/?size=100&id=19318&format=png&color=000000" alt="App Icon" width="40"></a>

> <a href='https://github.com/powerpizza'><img src="https://img.icons8.com/?size=100&id=AZOZNnY73haj&format=png&color=000000" alt="App Icon" width="40"></a>