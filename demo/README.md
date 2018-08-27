# A flask service for semantic dependency parsing

## To run 
1. Clone the pyNeurboParser Repo
2. Run the pyNeurboParser container
```
    docker run -it -v path_to_repo:/data/ -p 5000:5000 abornst/py-neurbo-parser
```
3. In the container run the following command to start the service
```
    python /data/demo/app.py
```

4. Navigate to the localhost:5000/ in your browser of choice