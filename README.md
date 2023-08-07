# django-prefect document

1. start the prefect local server  on
    local server: type prefect server start,
   or login prefect cloud :type  prefect cloud login
2. list of worker pool to start and befor run flow locally
    # article-process-pool 
     type : Process
    # my-process-pool
     type:Process
    # userflow-process-pool 
      type:Process
   # To start pool
      type prefect worker start --pool article-process-pool

   # custome block
   custom block are located at digital_ocean_block.py

   #flow function
   located at flow.py

   # Note
   run the same process with the article_flow repo

