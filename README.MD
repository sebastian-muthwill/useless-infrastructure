# The Useless Infrastructure
The sole purpose of this infrastructure is fun and education.
Do you know these [useless machines](https://en.wikipedia.org/wiki/Useless_machine) where you flip a switch, a lid opens, and the machine flips the switch back?
Well, this infrastructure has been inspired by the useless machine and is their software equivalent.

## What it does?
It simulates the implementation of a real-world use case and should be adaptable to other use cases as well.

We create fake blog posts which then shall be made searchable. What sounds easy can become difficult when it comes to scalability. Therefore, we make use of different tools to demonstrate how such a case can be implemented. 

The architecture consists of:
- a producer (blog post creation)
- a message queue (Kafka)
- an indexer (puts blog posts on the index)
- the index (OpenSearch)

All components are decoupled and run in their own docker containers. This should make it easy to run it locally.  

## Docker Containers
### Python producer
Creates fake blog posts and puts them on the Kafka `blog.new-blogpost` queue

### Python indexer
Reads the `blog.new-blogpost` queue and sends the entry to OpenSearch for indexing

### Kafka
Queue

### OpenSearch 
Search Index

### OpenSearch Dashboard
Easy access to the indexed data. 

## Installation
If you would like to play around with it, follow these steps:

1. Make sure you have Docker installed.
2. Clone the repo.
3. Run `docker compose build` from within the repo folder.
4. Run `docker compose up`.

Docker will now pull all the necessary images and run the whole thing. 

## WARNING!
Currently, there are no security measures implemented. There is no SSL, and passwords are defaults. 
Even if it should be obvious, don't run this on the internet. Use it only locally unless you know what you are doing.
