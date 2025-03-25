# PWP SPRING 2025
# PROJECT NAME
# Group information
* Mikko Lempinen, mikko.lempinen@oulu.fi
* Mohamed Al-Ajily, malajily24@student.oulu.fi
* Lukas Hoffmann, lhoffman24@student.oulu.fi
* Student 4. Abu Roman, aroman24@student.oulu.fi


__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint, instructions on how to setup and run the client, instructions on how to setup and run the axiliary service and instructions on how to deploy the api in a production environment__

# <p align="center">Table of Contents</p>
- [Setup Guide](#setup)
    - [Running the Flask Backend (Server)](#backend)
    - [Running the React Frontend (Client)](#frontend)
- [Database](#database)
    - [Populating the Database](#populating)

<br><br><br><br>

# <p align="center">🚀 Setup Guide</p><a name="setup"></a>


## <p align="center">Running the Flask Backend (Server)</p><a name="backend"></a>

### 1️⃣ Create and activate a Python Virutal Environment

1. Create a Python venv in the root directory of the repository with the command:
    ```console
    python -m venv venv
    ```
2. Activate the created virtual environment.
    - On **macOS** & **Linux** with:
    ```console
    source venv/bin/activate
    ```
    - On **Windows** with:
    ```console
    source venv\Scripts\activate
    ```

### 2️⃣ Install Python Dependencies

Once the virtual environment is activated, install the required Python libraries with:
```console
pip install -r server/requirements.txt
```

### 3️⃣ Run the Flask Server
Start the Flask backend with:

```console
python server/app.py
```

> [!NOTE] 
> By default, Flask runs at: http://127.0.0.1:5000/


## <p align="center">⚛️ Running the React Frontend (Client)</p><a name="frontend"></a>


### 1️⃣ Navigate to the Frontend Folder

Open a new terminal or command prompt and move into the React (client) folder:

```console
cd client
```

### 2️⃣ Install Dependencies

Before running React, install the necessary Node.js packages:

```console
npm install
```

### 3️⃣ Start the React Development Server

To launch the frontend, run:

```console
npm start
```

> [!NOTE] 
> This will start a development server at: http://localhost:3000/ *(the browser should open automatically)*.

# <p align="center">Database</p><a name="database"></a>

This app uses `SQLAlchemy` in combination with `pysqlite3` as a database so it should generally be compatible with any sqlite database.

## <p align="center">Populating the Database</p><a name="populating"></a>

You can populate the Database with the provided script. The data for the population should be in an csv-file, with each row beeing an individual food item, its properties being seperated by a comma and a semicolon indicating the corresponding pictures. You seperate the food items using a line break to indicate the next food item. 

An example-file, `example_data.csv` with some images can be found in the `example_data` folder, you can populate the database with the example data by running the following *(when in the project folder)*:

```console
python ./server/api/populate_db.py ./example_data/example_data.csv
```

You can then accordingly run the script for populating the database using the following command *(when in the project folder)*: 

```console
python ./server/api/populate_db.py path/to/data.csv
```

