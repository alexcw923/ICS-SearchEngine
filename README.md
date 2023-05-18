
<br />
<div align="center">
  

  <h3 align="center">ICS Search Engine</h3>

  <p align="center">
    The ICS Search Engine provides convenient search and retrieval of information from the ICS (Information and Computer Sciences) Department Webpages in the University of   California, Irvine. Developed as a project within the ICS web databases course, this search engine enables users to explore and navigate through a vast collection of webpages related to the field of computer science.
    <br />
    <a href="https://github.com/alexcw923/ICS-SearchEngine"><strong>Explore the docs »</strong></a>
    <br />
    
  </p>
</div>


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
