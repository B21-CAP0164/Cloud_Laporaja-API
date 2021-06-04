# laporaja-api


## For Local Computer Use  
### 1. Git Clone Project  
` git clone https://github.com/B21-CAP0164/laporaja-api.git `  

### 2. Create Virtual Enviroment


## For Cloud Run Use  
### 1. Setup Variable 
#### Extract Project ID form gcloud
`export PROJECT_ID=$(gcloud info --format='value(config.project)')`
#### Get region
` REGION=$(gcloud config get-value compute/region)`

### 2. Git Clone Project  
` git clone https://github.com/B21-CAP0164/laporaja-api.git `  

### 3. Create SQL Instance  
Create SQL Instance from GCP Console ```Navigation > SQL ```, Our team is using MySQL.   

### 4. Create Database Inside SQL Instance  
Create a database that represent the aplication.  

### 5. Create User from Cloud Shell  
#### Connect to SQL  
` gcloud sql connect <SQL Instance Name> --user root`  
#### Create the user  
` CREATE USER '<user-name>'@'<host>' IDENTIFIED BY '<password>' `  

### 6. Give Privileges from Cloud Shell  
` GRANT ALL PRIVILEGES ON <database-name>.<table-name> TO '<user-name>'@'<host>' `  

### 7. Exit MySQL Instance from Cloud Shell  
``` Exit; ```

### 8. Create Cloud Storage Bucket  
` gsutil mb -l ${REGION} gs://${PROJECT_ID} `  

### 9. Create ```.env``` File  
` 
DATABASE_URL=mysql://<user-name>:<password>@/<db-name>?unix_socket=/cloudsql/${PROJECT_ID}:${REGION}:<instances-name> 
GS_BUCKET_NAME=${PROJECT_ID}
SECRET_KEY=(a random string, length 50)  
`

### 10. Store the Secret_Key to Secret Manager  
`
gcloud secrets create django_settings --replication-policy automatic  
`  

### 11. Add ```.env``` File  
`
gcloud secrets versions add django_settings --data-file .env  
`  

### 12.Confirm Creation of Secret
`
gcloud secrets describe django_settings  
`  

### 13. Get Note of The Project Number (PROJECTNUM)
`
projects/PROJECTNUM/secrets/django_settings
`  

### 14. Grant Access to Secret to Cloud Run Service Account  
`
gcloud secrets add-iam-policy-binding django_settings \
    --member serviceAccount:PROJECTNUM-compute@developer.gserviceaccount.com \
    --role roles/secretmanager.secretAccessor
`  

### 15. Grant Access to Secret to Cloud Build Service Account  
`
gcloud secrets add-iam-policy-binding django_settings \
    --member serviceAccount:PROJECTNUM@cloudbuild.gserviceaccount.com \
    --role roles/secretmanager.secretAccessor
`   

### 16. Create A New Secret, ```superuser_password```  
`
gcloud secrets create superuser_password --replication-policy automatic
`  

### 17. Generate Randow Password as A Version  
`
cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c30 > superuser_password

gcloud secrets versions add superuser_password --data-file superuser_password
`  

### 18. Grant Access to Secret to Cloud Build Service Account  
` 
gcloud secrets add-iam-policy-binding superuser_password \
    --member serviceAccount:PROJECTNUM@cloudbuild.gserviceaccount.com \
    --role roles/secretmanager.secretAccessor
`  

### 19. Grant Permission for Cloud Build to Access Cloud SQL  
`
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member serviceAccount:PROJECTNUM@cloudbuild.gserviceaccount.com \
    --role roles/cloudsql.client
`  

### 20. Use Cloud Build to Build the Image
`
gcloud builds submit --config cloudmigrate.yaml
    --substitutions _INSTANCE_NAME=INSTANCE_NAME,_REGION=REGION
`  

### 21. Deploy Cloud Run Service  
`
gcloud run deploy polls-service \
    --platform managed \
    --region ${REGION} \
    --image gcr.io/${PROJECT_ID}/api_service \
    --add-cloudsql-instances {PROJECT_ID}:${REGION}:INSTANCE_NAME \
    --allow-unauthenticated
`  
