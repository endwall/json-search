# Simple Json Search
A Python Solution

## Design
- All search string are not tokenized
- and not further processing with stemming, etc
- indices are built in memory
- all tokens are lowercase

Data structues:
- TableName -> IndexName -> Token -> Hash of Document
- TableName -> Hash of Document -> Document

They are all implemented as Dict (in python) and sortedset which is to make sure to handle duplicated document indexing properly.

## Extensibility
- More indexing steps can be added. 
- More output formats can be added.

## Usage
In client/Makefile, Run
```
make
. venv/bin/activate
```

```
python jsearch/json-search.py --help
```

## Tests
Go to client, run
```
make tests
make lint
```
### Index
Allow inded json files
Example:
```
python jsearch/json_search.py index -t user -f files/users.json
```
Index data will be dumped to ```client/data``` directory

### List
Allow inspect index table schema to know which fields can be searched.

```
python jsearch/json_search.py list
```

### Search

Allow search by exact match and return either json or table
```
python jsearch/json_search.py search -t user -f organization_id -q 119 -o table 
```

## Potential Issues
### Design and operation
- Separate Query and Index (Refer to ELK)
- Split Index cross physical machines and add aggregation
- More complicated data structures to reduce memory footprint and query efficency


