from io import BytesIO
import base64
import matplotlib.pyplot as plt
from collections import Counter
from recipes.models import Recipe       # to connect to Recipe model parameters
import pandas as pd

# function to get recipe name from the ID, shouldn't need for graphs
#def get_recipename_from_id(val):
   # recipename=Recipe.objects.get(id=val)
    # and the name is returned
  #  return recipename

# this is done only once (per project)
def get_graph():
    # create a BytesIO buffer for the image
    buffer = BytesIO()
    # create a plot with a bytesIO object as a file-like object. Set format to png
    plt.savefig(buffer, format='png')
    # set cursor to the beginning of the stream
    buffer.seek(0)
    # retrieve the content of the file
    image_png=buffer.getvalue()
    # encode the bytes-like object
    graph=base64.b64encode(image_png)
    # decode the string as output
    graph=graph.decode('utf-8')
    # free up the memory of buffer
    buffer.close()
    # return the image/graph
    return graph

# chart_type: user input for type of chart
def get_chart(chart_type, data, **kwargs):
    # switch plot backend to AGG (Anti-Grain Geometry) - to write file. AGG is preferred for png files.
    plt.switch_backend('AGG')

    # specify figure size
    fig=plt.figure(figsize=(7,5))
    fig.set_facecolor('#7b8d6a')

    if data.empty:
        plt.text(0.5, 0.5, "No data available", ha='center', va='center', fontsize=12)
        plt.axis('off')
        return get_graph()

    if chart_type == '#1': # bar chart to display most popular ingredients
        # put all ingredients in a list
        all_ingredients = []
        # get all ingredients from all recipes
        for ingredients in data['ingredients']:
            if isinstance(ingredients, str):
                ingredients_list = [ingredient.strip().capitalize() for ingredient in ingredients.split(',')]
                all_ingredients.extend(ingredients_list)

        # count occurances of each ingredient
        ingredient_counts = Counter(all_ingredients)
        most_common = ingredient_counts.most_common(5) # top 5 ingredients

        if most_common:
            ingredients, counts = zip(*most_common)
            # create bar chart
            plt.bar(ingredients, counts, color='lightblue')
            plt.xlabel('Ingredients')
            plt.ylabel('Number of Recipes')
            plt.title('Most Popular Ingredients')
            plt.xticks(rotation=45, ha="right") # rotate labels for readability

    elif chart_type == '#2': # pie chart to display recipe difficulties percentage        
            difficulties = [recipe.calculate_difficulty() for recipe in Recipe.objects.all()]          
            difficulty_counts = Counter(difficulties)

            labels = list(difficulty_counts.keys())
            sizes = list(difficulty_counts.values())
            colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']

            plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
            plt.title("Recipe Difficulty")

    elif chart_type == '#3': # line chart to show cooking time distribution
            cooking_times = [recipe.cooking_time for recipe in Recipe.objects.all()]
            cooking_time_counts = Counter(cooking_times)
            sorted_times = sorted(cooking_time_counts.keys())    

            counts = [cooking_time_counts[time] for time in sorted_times]       
            
            plt.plot(sorted_times, counts, marker='o', linestyle='-', color='purple')
            plt.xlabel('Cooking Time (minutes)')
            plt.ylabel('Number of Recipes')
            plt.title('Cooking Time Distribution')
            plt.grid(True)

    plt.tight_layout()
    return get_graph()
        