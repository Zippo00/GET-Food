# YOU ARE IN THE PRODUCTION BRANCH. FOR LOCAL USAGE/DEPLOYMENT, SEE `MAIN` BRANCH.
<br><br><br>

# PWP SPRING 2025
# PROJECT NAME
# Group information
* Mikko Lempinen, mikko.lempinen@oulu.fi
* Mohamed Al-Ajily, malajily24@student.oulu.fi
* Lukas Hoffmann, lhoffman24@student.oulu.fi
* Student 4. Name and email


__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint, instructions on how to setup and run the client, instructions on how to setup and run the axiliary service and instructions on how to deploy the api in a production environment__

# <p align="center">Table of Contents</p>
- [Deployment via Docker](#deployment)
    - [Deploy the API server](#deploy-api)
    - [Deploy the Client](#deploy-client)
<br><br><br><br>

# <p align="center">Deployment via Docker</p><a name="deployment"></a>
The application can be deployed with the latest version of Docker. Docker automatically sets up the server and client, as well as populates the database with the data found in `example_data/example_data.csv`.

## <p align="center">1. Deploy the API server</p><a name="deploy-api"></a>

The production version of the API is configured to use a combination of [gunicorn](https://gunicorn.org/) and [nginx](https://nginx.org/) to serve the API.

1. Clone this repository to the machine you wish to deploy the API server on.

2. Navigate to the `api-prod` directory with: 
    ```console
    cd GET-Food/api-prod
    ```

3. Modify the `server_name` and `proxy_set_header` variables on lines **7** and **11** in the `default.conf` file to the IP or domain name you wish to deploy the API on.

4. Build the Docker environment with:
    ```console
    docker build compose up -d
    ```

5. Docker should build the containerized environment succesfully, and you can now use the API through the IP or domain you set up in the `api-prod/default.conf` file.

## <p align="center">1. Deploy the Client</p><a name="deploy-client"></a>

1. Clone this repository on the machine you wish to deploy the client on.

2. There's quite a few hard-coded URLs that need to be changed in the JavaScript files found in `GET-Food/client-prod/src`.

    Go through each of the JS files in `GET-Food/client-prod/src/components/`, `GET-Food/client-prod/src/pages/`, and `GET-Food/client-prod/src/services/` and change each instance of 'http://195.148.30.99' you find to the corresponding IP or domain name you set up in the [Deploy the API](#deploy-api) section.

3. Similarly as in the API deployment section, you need to change the IPs in `client-prod/compose.yaml` and `nginx.conf` to reflect the IPs of the machine you are deploying the client on.

    - Change the **line 9** in `client-prod/compose.yaml` to the internal IP-address of your machine.

    - Change the `server_name` variable on **line 14** of the `client-prod/nginx.conf` file to the public IP address or domain name you are deploying the client on.

4. After the files are modified, navigate to the `client-prod` directory with:
    ```console
    cd GET-Food/client-prod
    ```

5. Build the Docker environment with:
    ```console
    docker compose up -d
    ```

6. Docker should build the containerized environment succesfully, and you can now use the client through the IP or domain you set up in the `client-prod/nginx.conf` file.
