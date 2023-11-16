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
            # Don't add links to itself
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

    # Initialize the probability distributions with 0
    prob_dist = dict()
    for corpus_page in corpus:
        prob_dist[corpus_page] = 0

    # Calculate the probabilities for each page
    if len(corpus[page]) > 0:
        for linked_page in corpus[page]:
            prob_dist[linked_page] += damping_factor / len(corpus[page])
        for random_page in corpus:
            prob_dist[random_page] += (1 - damping_factor) / len(corpus)
    else:
        for random_page in corpus:
            prob_dist[random_page] = 1 / len(corpus)

    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Initialize the page ranks with 0
    page_ranks = dict()
    for corpus_page in corpus:
        page_ranks[corpus_page] = 0

    # Start with a random page from the corpus
    page = random.choice(list(corpus.keys()))

    # Create samples
    for i in range(n):
        prob_dist = transition_model(corpus, page, damping_factor)
        page = random.choices(list(prob_dist.keys()),
                              list(prob_dist.values()))[0]
        page_ranks[page] += 1

    # Normalize the page ranks
    for rank_page in page_ranks:
        page_ranks[rank_page] /= n

    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Initialize the page ranks equally between all pages (1 / num. of pages)
    page_ranks = dict()
    for corpus_page in corpus:
        page_ranks[corpus_page] = 1 / len(corpus)

    # Calculate new rank values based on all of the current rank values until convergence
    max_diff = float('inf')
    while (max_diff > 0.001):
        max_diff = 0
        for page in page_ranks:
            # Store the current rank value of the page
            current_rank = page_ranks[page]

            # Calculate the sum of the probabilities that we were on a page and chose the link to the page
            sum = 0
            for i in corpus:
                if page in corpus[i]:
                    sum += page_ranks[i] / len(corpus[i])

            # Calculate the new rank value
            page_ranks[page] = (1 - damping_factor) / len(corpus) + damping_factor * sum

            # Compare the current rank value with the new rank value to determine the change
            change = abs(current_rank - page_ranks[page])
            if change > max_diff:
                max_diff = change

    return page_ranks


if __name__ == "__main__":
    main()
