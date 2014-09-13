Text_Search_Algorithms
======================

Built a functioning text-based mini search engine. The search engine will support both single term queries and phrase queries, as well as wild-card queries

Dataset used : http://courses.cse.tamu.edu/caverlee/csce670_2013/hw/books.zip. A small collection of plain text books from Project Guttenberg. 

-----------------------------
Part 1: Boolean Retrieval

Built an inverted index over documents.
Tokenize each document using whitespaces and punctuations as delimiters and did not remove stop words. 
Then, did case-folding and built an index.

Example queries:

joseph conrad

joseph conrad heart darkness

mark twain quixote

-----------------------------
Part 2: Phrase Queries

Built a positional index to support phrase queries. We use quotes in a query to tell the search engine this is a phrase query. Again, we do not explicitly type AND in queries and never use OR, NOT or parentheses.

Example queries:

"joseph conrad"

"joseph conrad" "heart of darkness"

"mark twain" quixote

-----------------------------

Part 3: Wild-card Queries

Finally, built either a k-gram index index to support wild-card queries.

Example queries:

*rk twain

quixo*

joseph co*d


