# Laporaja API
The main function of this API is:
- Send GET request to get all the _reports_ data from the database.
- Send GET request to get the _reports_ history of a user
- Send POST request to post the _request_ data to the database.
- Send POST request to post the _user_ data to the database.

This API is using Django as its framework and MySQL for its database.
There are no authentication feature yet in this API. 
We deploy the API on Google Cloud Run, but for testing purpose we suggest to use local environtment.
<br/><br/>
The database used in this API is actually a non-relational database. We suggest you use noSQL database like Firestore to store the data. Because the project's data structure is changed in the last minutes, we didn't have time to changed the database to noSQL database. 


## Local Configuration
1. **Clone the project**
    ```sh
    git clone https://github.com/B21-CAP0164/laporaja-api.git
    ```
2. Rename **settings.py** to **settings-cloud-run.py** and **settings-local.py** to **setting.py**
2. **Create virtual environment**<br/>
    Install pip
    ```sh
    sudo apt-get install python3-pip
    sudo pip3 install virtualenv
    ```
    Create virtual environment called "venv"
    ```sh
    virtualenv venv
    ```
    Activate the environment
    ```sh
    source venv/bin/activate
    ```
3. **Install dependencies**
    ```python
    pip install -r requirements.txt
    ```
4. **Create MySQL database and grant user**<br/>
    Login to MySQL database as root user
    ```sh
    mysql -u root -p
    ```
    Create database
    ```sh
    CREATE DATABASE dbname;
    ```
    Create user and grant its privileges
    ```sh
    CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
    GRANT ALL PRIVILEGES ON dbname . * TO 'newuser'@'localhost';
    ```
    Exit MySQL
    ```sh
    quit;
    ```
5. Fill the necessary information in laporaja-api/settings.py<br/>
    You need to fill **secret key** and **MySQL database connection** in the settings file.
    You can visit https://djecrety.ir/ to generate secret key. 

6. **Migrate** for the first time
    ```sh
    python manage.py migrate
    ```
7. **Create Admin account** for Django Admin page
    ```sh
    python manage.py createsuperuser
    ```
8. **Create migration** for Admin
    ```sh
    python manage.py makemigration
    ```
9. **Migrate** for the Admin migration
    ```sh
    python manage.py migrate
    ```
10. Run the server
    ```sh
    python manage.py runserver
    ```
    - Admin page : http://localhost:8000/admin
    - GET all report : http://localhost:8000/request
    - GET report history (for 1 user ID) : http://localhost:8000/request/[USER-ID]
    - POST report : http://localhost:8000/request/[USER-ID]/add
    - POST user : http://localhost:8000/user
    
## Cloud Run Configuration
We follow the steps from [Google Cloud documentation](https://cloud.google.com/python/django/run) to deploy the API on Cloud Run.
To deploy [model service](https://github.com/B21-CAP0164/ML_Final-Project.git) using **Flask** framework just jump to the [Deploy](#deploy-to-cloud-run) step.

### Initialization
1. **Login** to GCP or [**create an account**](https://console.cloud.google.com/freetrial?_ga=2.79791191.1147108650.1623074813-999576286.1622490512). If you new you can activate free trial with the amount of $300 credits.
2. **Choose a project** or create one.
3. **Enable billing**. For more information about enabling billing, you can visit [here]( https://cloud.google.com/billing/docs/how-to/modify-project).
4. [**Enable API**](https://console.cloud.google.com/flows/enableapi?apiid=run.googleapis.com,sql-component.googleapis.com,sqladmin.googleapis.com,compute.googleapis.com,cloudbuild.googleapis.com,secretmanager.googleapis.com&_ga=2.118206409.1147108650.1623074813-999576286.1622490512&_gac=1.253091323.1623075296.Cj0KCQjwh_eFBhDZARIsALHjIKdof96Em5Zk67EaqR4GmjPsoKsXKBHSwcW2xWhYxw8IyGxNqAnHdsgaAqRDEALw_wcB) for Cloud SQL, Cloud Run, Cloud Build, Secret Manager, and Compute Engine API.
5. **Ensure sufficient permissions** are available. The minimum permission needed are below.
    - Cloud SQL Admin
    - Storage Admin
    - Cloud Run Admin
    - Secret Manager Admin

### Preparing the backend services
Detail information about services that we use.
Service | Usage
------- | ------
Cloud Storage | To save the API static files
Cloud SQL | For database
Secret Manager | To store secret key and password
Cloud Run | To deploy the API container

#### Create MySQL database and grant user on Cloud SQL
##### Create MySQL instances 
1. In GCP console, go to the **Cloud SQL** page.
2. Click **Create Instance**.
3. Choose **MySQL**.
4. Fill the necessary informations.
5. Click **Create**
##### Create database
1. Go to the **Instance page**.
2. Click **Instance name**.
3. Click **Create database**.
4. Fill the necessary informations.
5. Click **Create**
##### Create user and grant privileges
1. In the **cloud shell**, connect to the instances.
    ```sh
    gcloud sql connect [INSTANCE NAME] --user=root
    ```
2. Create user and grant privileges.<br/>
**WARNING!** Using **%** as host is the same as making the user to have root level access by granting access from all host.
    ```sh
    CREATE USER '[USER-NAME]'@'%' IDENTIFIED BY 'password';
    GRANT ALL PRIVILEGES ON [DB-NAME] . * TO '[USER-NAME]'@'localhost';
    ```
    
#### Grant Cloud Build to acess Clous SQL
1. Go to **IAM** page.
2. Edit role of PROJECTNUM@cloudbuild.gserviceaccount.com.
3. Click **Add another role**.
4. In the Select a role dialog, select **Cloud SQL Client**.
5. Click Save.

#### Create Cloud Storage bucket
In **cloud shell** type
```sh
gsutil mb -l REGION gs://PROJECT_ID-media
```

#### Save secret key and password with Secret Manager
##### Django Setting secret
1. Create **.env** with this value
    ```sh
    DATABASE_URL=mysql://[USER-NAME]:[PASSWORD]@/[DB-NAME]?unix_socket=/cloudsql/${PROJECT_ID}:${REGION}:<instances-name>
    GS_BUCKET_NAME=${PROJECT_ID} 
    SECRET_KEY=(a random string, length 50)
    ```
2. In cloud console go to **Secret Manager** page
3. Click **Create Secret**, and **upload the .env file**. 
4. Click **Create Secret**
5. In the right side of the screen click **Add Member**
6. In the **New Members** field, enter PROJECTNUM-compute@developer.gserviceaccount.com, and then press Enter.
7. In the **New Members** field, enter PROJECTNUM@cloudbuild.gserviceaccount.com, and then press Enter.
8. Set the role to **Secret Manager Secret Accessor**.
9. Click Save.
##### Django Admin password
1. In cloud console go to **Secret Manager** page
3. Click **Create Secret**, and insert random password in the value field. 
4. Click **Create Secret**
5. In the right side of the screen click **Add Member**
7. In the **New Members** field, enter PROJECTNUM@cloudbuild.gserviceaccount.com, and then press Enter.
8. Set the role to **Secret Manager Secret Accessor**.
9. Click Save.

### Deploy to Cloud Run
1. **Clone the project**.
    ```sh
    git clone https://github.com/B21-CAP0164/laporaja-api.git
    ```
2. **Run the cloudmigration.yaml file**. 
    ```sh
    gcloud builds submit --config cloudmigrate.yaml \
    --substitutions _INSTANCE_NAME=[INSTANCE-NAME],_REGION=[REGION]
    ```
3. **Deploy** to Cloud Run.
    ```sh
    gcloud run deploy [SERVICE-NAME] \
    --platform managed \
    --region [REGION] \
    --image gcr.io/[PROJECT_ID]/[SERVICE-NAME] \
    --add-cloudsql-instances [PROJECT_ID]:[REGION]:[INSTANCE_NAME] \
    --allow-unauthenticated
    ```
    - Admin page : url/admin
    - GET all report : url/request
    - GET report history (for 1 user ID) : url/request/[USER-ID]
    - POST report : url/request/[USER-ID]/add
    - POST user : url/user
