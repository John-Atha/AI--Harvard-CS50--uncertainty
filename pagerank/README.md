# Harvard CS50's Introduction to Artificial Intelligence with Python 2021 course

### Project 2a - PageRank
* Two different implementations of the famous PageRank algorithm, used by google to rank the web pages according to their incoming links
* The algorithms implemented are the Random Surfer Algorithm and the Iterative Algorithm
* The functions `main` and `crawl` were implemented in the distribution code
* The aim was to implement the `transition_model`, `sample_pagerank` and `iterate_pagerank` functions
##### Random Surfer Algorithm
* Each page is considered as a state of a Markov Chain
* The pagerank value of each page is computed by the number of the times that it was visited
* In order to avoid sinks, we use a damping factor (0<=d=<1), to decide the next page
* We get a random number in the range(0, 1) and
    * if number < d:
        * we randomly select one of the outcoming links
    * else:
        * we randomly select one of all the states (including the current one)
* This way we take a sample of n pages
* The PRs of the pages are normalized so that they sum to 1

##### Iterative Algorithm
* We initialize the PR(p) of each page (p) as 1/#(pages)
* Again, we use a damping factor (0<=d=<1)
* We treat each page with no outcoming edges, as a page that has an outcoming link to every page (including itself)
* We iteratively update the PR(p) for each page (p) as the sum:
    * PR(p) = (1-d)/N + d * Σ((PR(i))/NumLinks(i)) for each page (i) that has an edge towards page (p)
* We keep on updating all the pages this way, until every PR(p) converges within 0.001

- - -

* Developer: Giannis Athanasiou
* Github Username: John-Atha
* Email: giannisj3@gmail.com