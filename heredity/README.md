# Harvard CS50's Introduction to Artificial Intelligence with Python 2021 course

### Project 2b - Heredity
An AI to assess the likelihood that a person will have a particular genetic trait.

#### Background
* Each person carries two versions of a specific Gene, which, when mutated, can lead to hearing impairment
* Each person inherits one version from each one of his parents
* The more mutated genes you have, the more possible to have hearing impairment
* We model all of these relationships by forming a Bayesian Network of all the relevant variables, which considers a family of two parents and a single child.

#### Implementation
* The functions `main`, `load_data` and `powerset` were given as part of the distribution code
* The goal was to implement the rest of the functions
* The program calculates the probability for each person to bear zero, one or two copies of the gene and the probability to have a particular trait
* We calculate the conditional probabilities for each person by summing up all of the joint probabilities that satisfy the evidence, and then normalize those probabilities so that they each sum to 1.

#### Usage exmample
python3 heredity.py `data/family0.csv`
- - -

* Developer: Giannis Athanasiou
* Github Username: John-Atha
* Email: giannisj3@gmail.com