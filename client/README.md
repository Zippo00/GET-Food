# PWP SPRING 2025
# PROJECT NAME
# Group information
* Mikko Lempinen, mikko.lempinen@oulu.fi
* Mohamed Al-Ajily, malajily24@student.oulu.fi
* Lukas Hoffmann, lhoffman24@student.oulu.fi
* Student 4. Name and email


__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint, instructions on how to setup and run the client, instructions on how to setup and run the axiliary service and instructions on how to deploy the api in a production environment__


🚀 Setup Guide

🔹 Running the Flask Backend (Server)

1️⃣ Navigate to the Server Folder

Open a terminal or command prompt and move into the backend (server) folder:

cd server

2️⃣ Create and Activate a Virtual Environment

Python virtual environments help keep dependencies isolated.

🔹 On macOS & Linux

python3 -m venv venv
source venv/bin/activate

🔹 On Windows (Command Prompt)

python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies

Once the virtual environment is activated, install the required Python libraries:

pip install -r requirements.txt

4️⃣ Run the Flask Server

Start the Flask backend:

python app.py

By default, Flask runs at: http://127.0.0.1:5000/

⚛️ Running the React Frontend (Client)

1️⃣ Navigate to the Frontend Folder

Open a new terminal or command prompt and move into the React (client) folder:

cd client

2️⃣ Install Dependencies

Before running React, install the necessary Node.js packages:

npm install

3️⃣ Start the React Development Server

To launch the frontend, run:

npm start

This will start a development server at: http://localhost:3000/ (the browser should open automatically).
# Database
This app uses SQLAlchemy in Compbination with pysqlite3 as a database so it should generally be compatible with any sqlite database.

## Populating the Database
You can populate the Database with the provided script, the data for the population should be in an csv-file, with each row beeing an individual food item, it's properties being seperated by a comma and a semicolon indicating the corresponding pictures. You seperate the food items using a line break to indicate the next food item. 

For example a data.csv file containing the following:

Hamburger,10.99,A classic hamburger;hamburgerpicutre1,/path/to/hamburger1.jpg,hamburgerpicture2,/path/to/hamburger2.jpg
Cheesburger,12.99,A classic hamburger but with cheese,cheeseburgerpicture1,/path/to/cheeseburger1.jpg,cheeseburgerpicture2,path/to/cheeseburger2.jpg


You can run the script for populating the database using the following command (when in the project folder): python ./server/api/populate_db.py pat/to/data.csv
