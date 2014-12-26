
no_wordnet = False
def wordnet_available():
    '''
    Returns True if wordnet is available, False otherwise.
    With poor-mans memoization.
    '''
    global no_wordnet
    if no_wordnet:
        return False

    try:
        from nltk.corpus import wordnet as wn
    except ModuleError:
        no_wordnet = True
        print "not expanding tags: couldn't load nltk"
        return False

    try:
        wn.synsets("dog")
    except LookupError as e:
        no_wordnet = True
        print"not expanding tags: found nltk, but couldn't load wordnet " +\
                "corpus. nltk error message follows"
        print str(e)
        return False
    return True

def expand_tags(tags):
    if not wordnet_available():
        return tags
    
    from nltk.corpus import wordnet as wn
    # OK, let's get stupid
    expanded_tags = [t for t in tags]
    for tag in tags:
        for synset in wn.synsets(tag):
            for lemma in synset.lemma_names():
                expanded_tags.append(lemma)
    expanded_tags = list(set(expanded_tags))
    if len(expanded_tags) == len(tags):
        print "no expansion"
    else:
        print "expanded", tags, "-->", expanded_tags
    return expanded_tags

