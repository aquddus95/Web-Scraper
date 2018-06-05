#!flask/bin/python
from flask import Flask, jsonify, abort, make_response
from flask import request
import json
import sys

global actors_dict
global movies_dict 


with open("data.json") as data:
    sample_data= json.load(data)
    actors_dict=sample_data[0]
    movies_dict=sample_data[1]

app = Flask(__name__)


## cite: https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
## find actors with a given and operator
def filter_with_and(actor,age,gross, filter_actors):
    for key in actors_dict.keys():
            valid= True
            actor_json= actors_dict[key]
            
            if(actor != "None"):
                some_name=actor_json['name']
                actor=actor.replace("_", " ")
                substring=(actor in some_name)
                if(substring == False):
                    valid=False

            if(age != -100 and int(age) != int(actor_json['age'])):
                valid= False

            if(gross != -100  and int(gross) != actor_json['total_gross']):
                valid= False

            if(valid == True):
                filter_actors.append(actor_json)
    return(filter_actors)
## find actors with a given or operator
def filter_with_or(parse_string,filter_actors):
    vals=[]
    parse_string=parse_string.split('|')
    condition1= parse_string[0]
    vals.append(str(condition1))

    condition2= parse_string[1]
    condition2= condition2.split("=")
    vals.append(str(condition2[1]))

    for record in actors_dict.keys():
        valid= False
        actor_json= actors_dict[record]
        
        for possible_val in vals:
            some_name=actor_json['name']
            possible_val=possible_val.replace("_", " ")
            substring=(possible_val in some_name)

            if(substring == True):
                valid=True

            if( possible_val == str(actor_json['age'])):
                valid=True

            if( possible_val == str(actor_json['total_gross'])):
                valid=True
                
        if(valid==True):
            filter_actors.append(actor_json)
    return(filter_actors)


## find actors based on name/age/ or total gross value
@app.route('/actors', methods=['GET'])
def filter_actors():
    filter_actors= []
    try:
        actor=request.args['name']
    except:
        actor="None"
    try:
        age=request.args['age']
    except:
        age=-100
    try:
        gross=request.args['total_gross']
    except:
        gross=-100


    check_or=False
    parse_string= "None"
    if( actor != None):
        if (actor.find('|') != -1):
            check_or=True
            parse_string=actor

    if(age != -100):
        if (age.find('|') != -1):
            check_or=True
            parse_string=age


    if(gross != -100):
        if (gross.find('|') != -1):
            check_or=True
            parse_string=gross


    if(check_or == True):
        filter_actors=filter_with_or(parse_string,filter_actors)
    
    else:
        filter_actors=filter_with_and(actor,age,gross,filter_actors)

    if(filter_actors == []):
        abort(404)

    return jsonify({"result":filter_actors})

## find specific actor
@app.route('/actors/<string:actor_name>', methods=['GET'])
def get_actor_name(actor_name):

    actor_record=[]
    for record in actors_dict.keys():
        actor_json= actors_dict[record]
        some_name=actor_json['name']
        actor_name=actor_name.replace("_", " ")
        substring=(actor_name in some_name)
        if(substring):
            actor_record.append(actor_json)
            break

    if(actor_record == []):
        abort(404)        

    return jsonify({'result': actor_record})


## find specific movie
@app.route('/movies/<string:movie_name>', methods=['GET'])
def get_movie_name(movie_name):

    movie_record=[]
    for record in movies_dict.keys():
        movie_json= movies_dict[record]
        some_name=movie_json['name']
        movie_name=movie_name.replace("_", " ")
        substring=(movie_name in some_name)
        if(substring):
            movie_record.append(movie_json)
            break

    if(movie_record == []):
        abort(404)        
    return jsonify({'result': movie_record})


## and operator for querying for movies
def filter_with_and1(movie,age,gross, filter_movies):
    for key in movies_dict.keys():
            valid= True
            movie_json= movies_dict[key]
            
            if(movie != "None"):
                some_name=movie_json['name']
                movie=movie.replace("_", " ")
                substring=(movie in some_name)
                if(substring == False):
                    valid=False

            if(age != -100 and int(age) != int(movie_json['year'])):
                valid= False

            if(gross != -100  and int(gross) != movie_json['box_office']):
                valid= False

            if(valid == True):
                filter_movies.append(movie_json)
    return(filter_movies)

## or operator for querying movies
def filter_with_or1(parse_string,filter_movies):
    vals=[]
    parse_string=parse_string.split('|')
    condition1= parse_string[0]
    vals.append(str(condition1))

    condition2= parse_string[1]
    condition2= condition2.split("=")
    vals.append(str(condition2[1]))

    for record in movies_dict.keys():
        valid= False
        movie_json= movies_dict[record]
        
        for possible_val in vals:
            some_name=movie_json['name']
            possible_val=possible_val.replace("_", " ")
            substring=(possible_val in some_name)

            if(substring == True):
                valid=True

            if( possible_val == str(movie_json['year'])):
                valid=True

            if( possible_val == str(movie_json['box_office'])):
                valid=True
                
        if(valid==True):
            filter_movies.append(movie_json)
    return(filter_movies)

## get a list of movies based on name/year/box_office amount
@app.route('/movies', methods=['GET'])
def filter_movies():
    filter_movies= []
    try:
        movie=request.args['name']
    except:
        movie="None"
    try:
        age=request.args['year']
    except:
        age=-100
    try:
        gross=request.args['box_office']
    except:
        gross=-100


    check_or=False
    parse_string= "None"
    if(movie != None):
        if (movie.find('|') != -1):
            check_or=True
            parse_string=movie

    if(age != -100):
        if (age.find('|') != -1):
            check_or=True
            parse_string=age


    if(gross != -100):
        if (gross.find('|') != -1):
            check_or=True
            parse_string=gross


    if(check_or == True):
        filter_movies=filter_with_or1(parse_string,filter_movies)
    
    else:
        filter_movies=filter_with_and1(movie,age,gross,filter_movies)

    if(filter_movies == []):
        abort(404)

    return jsonify({"result":filter_movies})

## Post actor and correlating information into the JSON document
@app.route('/actors', methods=['POST'])
def create_actor():
    if(not request.json):
        abort(400)

    if(not("name" in request.json)):
        name="None"
    else:
        name=request.json['name']    

    if(not("age" in request.json)):
        age=-1
    else:
        age=request.json['age']

    if(not("total_gross" in request.json)):
        total_gross=0
    else:
        total_gross=request.json['total_gross']

    if(not("movies" in request.json)):
        movies=[]
    else:
        movies=request.json['movies']
    
    actor = {
    'json_class': "Actor",
    'name': name,
    'age': age,
    'total_gross': total_gross,
    'movies': movies
    }

    
    actors_dict[name]=actor
    return jsonify({'result': actor}), 201

## Post movie and correlating information into the JSON document
@app.route('/movies', methods=['POST'])
def create_movie():
    if(not request.json):
        abort(400)

    if(not("name" in request.json)):
        name="None"
    else:
        name=request.json['name']    

    if(not("wiki_page" in request.json)):
        wiki_page="None"
    else:
        wiki_page=request.json['wiki_page']  

    if(not("year" in request.json)):
        year=-1
    else:
        year=request.json['year']

    if(not("box_office" in request.json)):
        box_office=0
    else:
        box_office=request.json['box_office']

    if(not("actors" in request.json)):
        actors=[]
    else:
        actors=request.json['actors']
    
    movie = {
    'json_class': "Movie",
    'wiki_page':wiki_page,
    'name': name,
    'year': year,
    'box_office': box_office,
    'actors': actors
    }

    
    movies_dict[name]=movie
    return jsonify({'result': movie}), 201


## Edit information of an actor listed in the JSON document
@app.route('/actors/<string:actor_name>', methods=['PUT'])
def update_actor(actor_name):


    actor_name= actor_name.replace("_"," ")
    actor_json= None
    try:
        actor_json=actors_dict[actor_name]
    except:
        abort(400)
    if not request.json:
        abort(400)
    
    if(("age" in request.json)):
        age=request.json['age']
        actor_json['age']=age

    if(("total_gross" in request.json)):
        total_gross=request.json['total_gross']
        actor_json['total_gross']=total_gross

    if(("movies" in request.json)):
        movies=request.json['movies']
        lis=actor_json["movies"]
        for mv in movies:
            lis.append(mv)
        actor_json["movies"]=lis

    return jsonify({'result': actor_json}), 

## Edit information of a movie listed in the JSON document
@app.route('/movies/<string:movie_name>', methods=['PUT'])
def update_movie(movie_name):


    movie_name= movie_name.replace("_"," ")
    movie_json= None
    try:
        movie_json=movies_dict[movie_name]
    except:
        abort(400)
    if not request.json:
        abort(400)
    
    if(("year" in request.json)):
        year=request.json['year']
        movie_json['year']=year

    if(("wiki_page" in request.json)):
        wiki_page=request.json['wiki_page']
        movie_json['wiki_page']=wiki_page    

    if(("box_office" in request.json)):
        box_office=request.json['box_office']
        movie_json['box_office']=box_office

    if(("actors" in request.json)):
        actors=request.json['actors']
        lis=movie_json["actors"]
        for ac in actors:
            lis.append(ac)
        movie_json["actors"]=lis

    return jsonify({'result': movie_json}), 

## Delete information relating to an actor in the JSON document
@app.route('/actors/<string:actor_name>', methods=['DELETE'])
def delete_actor(actor_name):

    actor_name= actor_name.replace("_"," ")
    actor_json= None
    try:
        actor_json=actors_dict[actor_name]
    except:
        abort(400)


    del actors_dict[actor_name]
    return jsonify({'result': True})

## Delete information relating to a movie in the JSON document
@app.route('/movies/<string:movie_name>', methods=['DELETE'])
def delete_movie(movie_name):

    movie_name= movie_name.replace("_"," ")
    movie_json= None
    try:
        movie_json=movies_dict[movie_name]
    except:
        abort(400)


    del movies_dict[movie_name]
    return jsonify({'result': True})


## TEST CASES
@app.route('/test1/', methods=['GET'])
def test1():
    filter_names=[]
    filter_names=filter_with_and("Bruce",-100,-100,filter_names)
    return jsonify({'result': filter_names})

@app.route('/test2/', methods=['GET'])
def test2():
    filter_names=[]
    filter_names=filter_with_and("Bruce",61,-100,filter_names)
    return jsonify({'result': filter_names})

@app.route('/test3/', methods=['GET'])
def test3():
    filter_names=[]
    filter_names=filter_with_and("Bruce",-100, 58397890,filter_names)
    return jsonify({'result': filter_names})


@app.route('/test4/', methods=['GET'])
def test4():
    filter_names=[]
    filter_names=filter_with_or("name=Bruce|age=50",filter_names)
    return jsonify({'result': filter_names})


@app.route('/test5/', methods=['GET'])
def test5():
    filter_names=[]
    filter_names=filter_with_or("name=Bruce|age=50",filter_names)
    return jsonify({'result': filter_names})



@app.route('/test6/', methods=['GET'])
def test6():
    return get_movie_name("The First Deadly Sin")

@app.route('/test7/', methods=['GET'])
def test7():
    filter_names=[]
    filter_names=filter_with_and1("None",2000,-100,filter_names)
    return jsonify({'result': filter_names})


if __name__ == '__main__':
    app.run(debug=True)
