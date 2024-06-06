import openai
from openai import OpenAI
import json
from graphviz import Digraph
from PIL import Image
from io import BytesIO
import ast
from treelib import Node, Tree
from graphviz import Graph, Digraph
import matplotlib.pyplot as plt
import networkx as nx
import mongo
from openai_response import get_openai_response

def get_static_answers(case):
    system_prompt = """
    I will be giving you a few witness statements about a crime. Your task is to answer the follow up questions in a clear and concise manner. The accuracy of this task is important and so, refrain from answering the questions whose answers are not mentioned in the statement.

    These are the questions that you must answer based on the witness statements. Please limit your answer to 3 words or less.

    What was the crime being discussed?
    What is the gender of the criminal?,
    What does the vehicle used in the crime look like?,
    What did the criminal look like?,
    What did the criminal wear?,
    What did the criminal use to commit the crime?,
    What was the criminal's ethnicity?,
    What was the criminal's age?,
    What did the victim look like?,
    What did the victim wear?,
    What was the victim's ethnicity?,
    What was the gender of the victim?,
    What was the age of the victim?

    Return the answer as a python list.\\
    If the answer to that question is not in the passage, leave it empty:

    """

    keys = ['crime', 'criminal gender', 'crime vehicle', 'criminal\'s appearance', 'criminal\'s clothes', 'criminal accessasory', 'crinimal\'s ethnicity', 'criminal\'s age', 'victim\'s appearance', 'victim\'s clothes', 'victim\'s ethnicity', 'victim\'s gender', 'victim\'s age']

    

    # content=""
    # path = 'C:/Users/nithy/Documents/GitHub/596-E-WitnessStatementProcessing/FrontEnd/reactapp/src/witnessstatements/'+ dir_name + '/'
    # with os.scandir(path) as dir_contents:
    #   for entry in dir_contents:
    #     filename = path + entry.name
    #     with open(filename) as f:
    #         lines = '\n'.join(f.readlines())
    #         # print(lines)
    #         content+=lines
    #         content+='\n'
    dict = mongo.show_mongodb_statements(case)
    statements = ""

    for key in dict.keys():
       statements+=dict[key]   
       statements+='\n'


    user_prompt = statements
    answers = []
    # for i in range(len(user_prompt)):
    response = get_openai_response(user_prompt, system_prompt)
    print(response)
    answer = ast.literal_eval(response)
    answers.append(answer)    

    description_of_the_crime = {}
    for k, v in zip(keys, answer):
        description_of_the_crime[k]=v
    
    nodes = []
    
    crime_desc = description_of_the_crime['crime']
    nodes.append(crime_desc)
    edges = []
    colours = ['white']
    for key in description_of_the_crime.keys():
        # edges.append()

        # s = key+":\n"+description_of_the_crime[key]
        if 'crime'==key:
            continue
        nodes.append(key)
        
        if len(description_of_the_crime[key])>0 and  "not mentioned" not in str.lower(description_of_the_crime[key]):
            # colours.append('white')
            nodes.append(description_of_the_crime[key])
            edges.append((key, description_of_the_crime[key]))
        
        if 'victim' in key:
            edges.append((key,crime_desc))
        else:
            edges.append((crime_desc, key))  

        if len(description_of_the_crime[key])<=0 or  "not mentioned" in str.lower(description_of_the_crime[key]):
           colours.append('red')
        else:
          if 'victim' in key:
            colours.append('blue')
            colours.append('white')
          else:
            colours.append('green')
            colours.append('white')


    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # Create Graphviz digraph for visualization
    dot = Digraph(comment='Tree Visualization')

    # Add nodes with colors
    for node, color in zip(nodes, colours):
        dot.node(str(node), str(node), color=color, style='filled')

    # Add edges (optionally set edge colors)
    for edge in edges:
        dot.edge(str(edge[0]), str(edge[1]), color='gray')

    # Generate and return the image
    dot_format = 'png'  # Choose the desired image format (e.g., png, pdf, svg, etc.)
    graph_bytes = dot.pipe(format=dot_format)

    graph_bytesio = BytesIO(graph_bytes)
    image = Image.open(graph_bytesio)
    img_stream = BytesIO()
    image.save(img_stream, format='PNG')
    img_stream.seek(0)

    # Serve the image to the front end
    return send_file(img_stream, mimetype='image/png')
