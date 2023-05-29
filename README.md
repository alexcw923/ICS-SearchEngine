
<br />
<div align="center">
  

  <h3 align="center">ICS Search Engine</h3>

  
</div>

The ICS Search Engine provides convenient search and retrieval of information from the ICS (Information and Computer Sciences) Department Webpages at University of   California, Irvine. This search engine enables users to explore a vast collection of webpages within the ICS department, using algorithms such as TF-IDF scoring and PageRank algorithm to improve users' searching experience. 

## Getting Started

### Building Index

In order to build the inverted index for our corpus you will need to run this following command:

```
python main.py build
```

This will take a decent amount of time to run.        
    

### Searching with Console

To search after you built the inverted index use this following command:
```
python main.py search ""
```
Then you type in the query that you want after the Search text and press enter, (e.g query = machine learning) the console will look like this:
```
Search machine learning
```
Upon pressing enter the console will display the top 5 urls from the query


### Searching with GUI

To search after you built the inverted index on a GUI use this following command:
```
python searchPage.py
```
after doing this you should click on the localhost and there will a simple search interface
