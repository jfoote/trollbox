
has_wordnet = None
def wordnet_available():
    '''
    Returns True if wordnet is available, False otherwise.
    With poor-mans memoization.
    '''
    global has_wordnet
    if has_wordnet != None:
        return has_wordnet

    try:
        print "loading wordnet corpus"
        from nltk.corpus import wordnet as wn
        wn.synsets("dog")
        has_wordnet = True
    except ImportError:
        has_wordnet = False
        print "not expanding tags: couldn't load nltk"
    except LookupError as e:
        has_wordnet = False
        print"not expanding tags: found nltk, but couldn't load wordnet " +\
                "corpus. nltk error message follows"
        print str(e)
    return has_wordnet

def expand_tags(tags):
    if not wordnet_available():
        return tags
    
    from nltk.corpus import wordnet as wn
    # OK, let's get stupid
    expanded_tags = [t for t in tags]
    for tag in tags:
        for synset in wn.synsets(tag):
            for lemma in synset.lemma_names():
                for word in lemma.split("_"): # no support for phrases
                    expanded_tags.append(lemma)
    expanded_tags = list(set(expanded_tags))
    if len(expanded_tags) == len(tags):
        print "no expansion"
    else:
        print "expanded", tags, "-->", expanded_tags
    return expanded_tags

