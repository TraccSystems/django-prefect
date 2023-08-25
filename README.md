# django-prefect document

1. start the prefect local server : type prefect server start,
   or login prefect cloud :type  prefect cloud login
   
   # create new worker process pool
   type  prefect work-pool create --type process my-process-pool

   # create new deployment
3. list of avaliable worker pool to start and before run flow locally or with prefect cloud
    # article-process-pool 
     type : Process
    # my-process-pool
     type:Process
    # userflow-process-pool 
      type:Process
   
   # create new worker pool
   type  prefect work-pool create --type process my-process-pool
   
   # To start new worker  pool
      type prefect worker start --pool article-process-pool
   
 

   # create new deployment
   cd  into flowapp
   
    # list of flow name to add to existing work pool
   1. pull_data_from_s3_write_to_postgress
   2. write_data_to_postgress
   3. download_file_from_s3_upload_to_postgres
      all flow are in flow.py
  # to deploy 
    type prefect deploy flow.py:download_file_from_s3_upload_to_postgres -n my-deployment -p userflow-process-pool 
   
   


   # custome block
   custom block are located at digital_ocean_block.py

   #flow function
   located at flow.py

   # Note
   run the same process with the article_flow repo

