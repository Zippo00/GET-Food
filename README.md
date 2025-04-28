# PWP SPRING 2025
# Northern Light
# Group information
* Mikko Lempinen, mikko.lempinen@oulu.fi
* Mohamed Al-Ajily, malajily24@student.oulu.fi
* Lukas Hoffmann, lhoffman24@student.oulu.fi
* Abu Roman, aroman24@student.oulu.fi


__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint, instructions on how to setup and run the client, instructions on how to setup and run the axiliary service and instructions on how to deploy the api in a production environment__

# <p align="center">Table of Contents</p>
- [Deployment in Production Environment](#production)
- [Local Deployment via Docker](#deployment)
- [Setup Guide for Direct Deployment](#setup)
    - [Running the Flask Backend (Server)](#backend)
    - [Running the React Frontend (Client)](#frontend)
- [API Documentations](#apidocs)
- [Database](#database)
    - [Populating the Database](#populating)
- [Unit tests](#unit-tests)
    - [Running API unit tests](#api-tests)

<br><br><br><br>
# <p align="center">Deployment in Production Environment</p><a name="deployment"></a>
The API and Client can be deployed in a production environment.

 Branch **`prod`** includes detailed instructions on how this can be done.

 The instructions described from here on are meant for local deployment only, and differ from the instructions found in `prod` branch.
<br><br><br>


# <p align="center">Local Deployment via Docker</p><a name="deployment"></a>
The application can be deployed with the latest version of Docker. Docker automatically sets up the server and client, as well as populates the database with the data found in `example_data/example_data.csv`.

To deploy the application locally:

1. While in the root directory of the repository, build the Docker environment with:
    ```console
    docker compose up -d
    ```
2. After Docker is finished building the environment, two containers should be up and running named **GET-Food-Server** and **GET-Food-Client**.

> [!NOTE] 
> **GET-Food-Client** container includes NGINX as a proxy server to serve the client on the default **HTTP** port 80.

3. Navigate to `http://localhost` in your browser and you should see the UI of the application.

# <p align="center">🚀 Setup Guide for Direct Deployment</p><a name="setup"></a>


## <p align="center">Running the Flask Backend (Server)</p><a name="backend"></a>

### 1️⃣ Create and activate a Python Virtual Environment

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

# <p align="center">API Documentations</p><a name="apidocs"></a>

The API documentations are done with [Swagger](https://swagger.io/docs/). After you have the Flask application running, you can find the documentations via a browser at *URL*/**apidocs**. 

For example, if you have the application running on localhost, you would find the API documentations at http://localhost/apidocs.


# <p align="center">Database</p><a name="database"></a>

This app uses `SQLAlchemy` in combination with `pysqlite3` as a database so it should generally be compatible with any sqlite database.

## <p align="center">Populating the Database</p><a name="populating"></a>

You can initially populate the Database with the provided script. The data for the population should be in an csv-file, with each row beeing an individual food item, its properties being seperated by a comma and a semicolon indicating the corresponding pictures. You seperate the food items using a line break to indicate the next food item. 

An example-file, `example_data.csv` with some images can be found in the `example_data` folder. Note that the path to the image is expected to be a relative path. You can populate the database with the example data by running the following *(when in the project folder)*:

```console
python ./server/populate_db.py ./example_data/example_data.csv
```

You can then accordingly run the script for populating the database using the following command *(when in the project folder)*: 

```console
python ./server/populate_db.py path/to/data.csv
```

# <p align="center">Unit tests</p><a name="unit-tests"></a>

The repository contains unit tests for testing the functionalitites of the **API endpoint**.

## <p align="center">Running API unit tests</p><a name="api-tests"></a>

After the backend (server) has been successfully set up, you can run the unit tests for the API and DB by:

1. Navigate to the `server` folder with:
    ```console
    cd GET-Food/server
    ```
2. Run the unit tests with:
    ```console
    pytest test_api.py
    ```
3. Run the database tests with 
    ```console
    pytest test_db.py
    ```
