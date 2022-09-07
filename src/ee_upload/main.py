import ee
import google.auth
from google.auth import compute_engine

def gcs_to_ee(event, context):
  """Creates an Earth Engine asset from data in Cloud Storage.

  When an object is created in a specified Cloud Storage Bucket, an Earth Engine
  Task that creates an asset from that object.

  Args:
    event: Event payload.
  """
  # Get GCS location of file creation that triggered function
  project_id = "PROJECT_ID"
  file = event
  path = "gs://" + file["bucket"] + "/" + file["name"]
  file_title = file["name"].rsplit(".", 1)[0]

  # Set up auth
  scopes = [
    "https://www.googleapis.com/auth/earthengine"
   ]

  credentials = compute_engine.Credentials(scopes=scopes)
  ee.Initialize(credentials)

  # Create request id
  request_id = ee.data.newTaskId()
  request_id = request_id[0]

  # Create params for ingestion
  name = "projects/"+ project_id +"/assets/" + file_title
  sources = [
      {
          "uris": [path],
          "csvDelimiter": "|"
      },
  ]
  params = {"name": name, "sources": sources}

  # Start ingestion
  ee.data.startTableIngestion(
      request_id, params, allow_overwrite=True)