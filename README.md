# Simple Json Search Demo

This is a demo for json documents indexed and searched.
There are 2 parts
- Client: A simple json search application
- Server: An ELK docker stack (only to show a scalable solution)

## Solution
search can be very complicated. Things need to be considered at least:
- Natural Langurage Processing
- Information Retrival
It is a combination of engineering and algorithms.

Here this is a super simple solution.
### Index
It uses inverted index which is a map between tokens and document. As it is the simplest solution, there is no tokenizaton, stemming, lemmatization steps. The whole json key's value will be used as the token.

Index is implemented as a dict.
Here are the internal data structure.
- TableName -> IndexName -> Token -> Hash of Document
- TableName -> Hash of Document -> Document

### Search
Given a query, search against a search Table and Index.

## Client
[Json-search](client/README.md)

## Server
[ELK Search](server/README.md)

This is a ELK docker solution. 
logstash config has been changed so that it can index organization/user/ticket json files.

Reference: [ELK docker-compose](https://github.com/deviantony/docker-elk)
