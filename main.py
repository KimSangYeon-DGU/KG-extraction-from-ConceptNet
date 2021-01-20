import requests

def remove_stopword(words):
    import nltk
    from nltk.corpus import stopwords  
    from nltk.tokenize import word_tokenize
    
    stop_words = set(stopwords.words('english'))

    word_tokens = word_tokenize(words)
    filtered_words = ' '.join([w for w in word_tokens if not w in stop_words])

    return filtered_words

def draw_graph(triples, root_node_name):
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.MultiDiGraph()

    for triple in triples:
        G.add_edge(triple['head'], triple['tail'], weight=triple['weight'])
        #G.add_edge(triple['head'], triple['tail'])
    
    weights = list(nx.get_edge_attributes(G,'weight').values())
    scaled_weights = [w*1.2 for w in weights]
    edge_labels = {(triple['head'], triple['tail']): triple['relation'] for triple in triples}
    plt.figure(figsize=(16,10))
    pos = nx.spring_layout(G, k=1)
    nx.draw(G, pos, with_labels = True, edge_color = 'grey', width=scaled_weights, linewidths=2, node_size=2500, node_color='lightpink', alpha=0.8)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    #plt.show()
    plt.savefig('./KG_samples/{0}.png'.format(root_node_name))

#root_node_names = ['high_jump', 'long_jump', 'triple_jump', 'pole_vault', 'discus_throw', 'hammer_throw', 'javelin_throw', 
# 'shot_put', 'lay_up', 'bowling', 'tennis', 'diving', 'springboard', 'snatch', 'clean_and_jerk', 'gymnastics']
root_node_names = ['gymnastics']
triples = []

for root_node_name in root_node_names:
    obj = requests.get('http://api.conceptnet.io/c/en/{0}'.format(root_node_name)).json()
    keys = obj.keys()

    edge_len = len(obj['edges'])

    for edge in obj['edges']:
        
        if edge['rel']['label'] != 'ExternalURL' and edge['rel']['label'] != 'SymbolOf' and edge['start']['language'] == 'en' and edge['end']['language'] == 'en':
            #print(edge['start']['label'], ' ', edge['rel']['label'], ' ', edge['end']['label'], ' ', edge['weight'])

            head_words = remove_stopword(edge['start']['label'].lower())
            tail_words = remove_stopword(edge['end']['label'].lower())

            triples.append({'head': head_words, 'relation': edge['rel']['label'], 'tail': tail_words, 'weight': edge['weight']})

draw_graph(triples=triples, root_node_name=root_node_names[0])
