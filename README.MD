# The Useless Infrastructure
The sole purpose of this infrastructure is fun and education.

## Docker Containers
### Python producer
Creates fake blogposts and puts them on the Kafka `blog.new-blogpost` queue

### Python indexer
Reads `blog.new-blogpost` queue and sends entry to Opensearch for indexing

### Kafka
Queue

### Opensearch 
Search Index
