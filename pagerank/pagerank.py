import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def share_prob_to_all(corpus, pages):
    p = dict()
    for temp_page in corpus:
        p[temp_page] = 1 / pages
    return p


"""
Return a probability distribution over which page to visit next,
given a current page.

With probability `damping_factor`, choose a link at random
linked to by `page`. With probability `1 - damping_factor`, choose
a link at random chosen from all pages in the corpus.
"""
def transition_model(corpus, page, damping_factor):
    pages = len(corpus)
    p = dict()
    neighbours = corpus.get(page)
    # if page does not have outcoming links
    if not neighbours:
        p = share_prob_to_all(corpus, pages)
    # if it has outcoming links, according to the damping factor, choose between
    else:
        # ignore self-edges
        if page in neighbours:
            neighbours.remove(page)
        # visiting one of the neighbours
        if random.random() < damping_factor:
            num = len(neighbours)
            for temp_page in corpus:
                if temp_page in neighbours:
                    p[temp_page] = 1 / num
                else:
                    p[temp_page] = 0
        # choosing one page randomly
        else:
            p = share_prob_to_all(corpus, pages)
    return p


"""
Return PageRank values for each page by sampling `n` pages
according to transition model, starting with a page at random.

Return a dictionary where keys are page names, and values are
their estimated PageRank value (a value between 0 and 1). All
PageRank values should sum to 1.
"""    
def sample_pagerank(corpus, damping_factor, n):
    # initialize PageRank (pg) dictionary and Probability to be visited (p) dictionary
    pages = len(corpus)
    pg = dict()
    p = dict()
    for page in corpus:
        pg[page] = 0
        p[page] = 1/pages

    for _ in range(n):
        curr = random.choices([page for page in p], weights = [p[page] for page in p], k=1)
        pg[curr[0]] += 1
        p = transition_model(corpus, curr[0], damping_factor)
    
    for page in pg:
        pg[page] /= n
    return pg


"""
Return PageRank values for each page by iteratively updating
PageRank values until convergence.

Return a dictionary where keys are page names, and values are
their estimated PageRank value (a value between 0 and 1). All
PageRank values should sum to 1.
"""
def iterate_pagerank(corpus, damping_factor):
    
    # keep a copy of corpus to not modify the original one
    curr_corpus = dict()
    for page in corpus:
        curr_corpus[page] = corpus[page].copy()

    pages = len(curr_corpus)

    # a page that has no links at all should be interpreted as having one link for every page in the corpus (including itself)
    for page in curr_corpus:
        if not len(curr_corpus[page]):
            curr_corpus[page] = set(curr_corpus.keys())

    # we keep an 'inverse' corpus to be able to iterate through
    # the pages that lead to each page
    inverse_corpus = dict()
    for page in curr_corpus:
        for target in curr_corpus[page]:
            if not inverse_corpus.get(target):
                inverse_corpus[target] = set()
            inverse_corpus[target].add(page)

    # we initialize the PR(p) for each p
    pr = dict()
    for page in curr_corpus:
        pr[page] = 1 / pages
    
    # we begin the iteration
    done = False
    while True:
        if done:
            break
        done = True
        old_pr = pr.copy()
        # for each page
        for page in curr_corpus:
            # compute and keep the sum
            any_page = (1-damping_factor) / pages
            summa = 0
            for source in inverse_corpus[page]:
                summa += old_pr[source] / len(curr_corpus[source])
            neighbours = damping_factor * summa
            pr[page] = any_page + neighbours
            # check the convergence
            if abs(old_pr[page]-pr[page])>0.001:
                done = False   
    return pr


if __name__ == "__main__":
    main()
