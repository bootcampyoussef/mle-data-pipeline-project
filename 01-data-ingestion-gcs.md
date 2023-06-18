# Loading Data to GCS

We will load data with the help of a modified `data_ingestion.py` script from Monday into a GCS bucket. 

For that please create a service account with the following roles:
- Storage Admin
- Storage Object Admin

Create a service account key and download the JSON. We created a key on Tuesday if you want to have a guide.

## Create a GCS Bucket

In the cloud console go to the [Storage Browser](https://console.cloud.google.com/storage/browser) and create a new bucket. 

1. Give it a name
2. Region: europe-west3

The rest can be left as default.

## Upload the data

Have a look at the `data_ingestion.py` script. We will modify it to upload the data to GCS. With that script we are loading 3 months of data into the bucket.

```python
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = sa_path
client = storage.Client()
bucket = client.get_bucket(bucket)
bucket.blob(f'yellow_taxi/{file_name}').upload_from_string(df_taxi.to_parquet(), 'text/parquet')
```

This part allows us to connect to the bucket and upload the data.
