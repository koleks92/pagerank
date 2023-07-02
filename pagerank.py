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


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    links = corpus[page]
    if links:
        prob_dist_dict = {}
        # Probability dampin_factor
        P1 = damping_factor/len(links)
        for link in links:
            prob_dist_dict[link] = P1
        # Probability 1 - damping factor
        P2 = round((1 - damping_factor) / (len(links) + 1), 3) # Get value from all links + source link
        for link in links:
            prob_dist_dict[link] = prob_dist_dict[link] + P2 # Add extra value to all the links
        # Add source link to the dictionary
        prob_dist_dict[page] = P2       
    
    #If page has no outgoin links
    else:
        prob_dist_dict = {}
        P1 = 1 / len(corpus)
        for link in corpus:
            prob_dist_dict[link] = P1

    return prob_dist_dict



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Empty dictionary
    page_rank = {}
    # Initiate each rank
    for link in corpus:
        page_rank[link] = 0.0

    # Generate first sample
    sample = random.choice(list(corpus.keys()))
    page_rank[sample] += (1 / n) # 1/n is a probability 1/n and n is number of samples 


    for i in range(n):

        prob_dist_dict = transition_model(corpus, sample, damping_factor)
        links = list(prob_dist_dict.keys())
        probabilities = list(prob_dist_dict.values())

        link = random.choices(links, probabilities)[0]
        page_rank[link] += (1 / n)

        sample = link


    return page_rank



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {}

    for link in corpus:
        page_rank[link] = 1 / len(corpus)

    print(page_rank)

if __name__ == "__main__":
    main()
