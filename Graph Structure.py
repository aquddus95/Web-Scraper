## this function gets all verticies and edges from the passed in dictionary of actors and his or her movies
## so this function will add the names of the actors/movies and then create edges between a pair of actor and his or her movie
def parse_names(special_dict):
    lis_vertex=[]
    lis_edges=[]
    for elem in special_dict.keys():
        actr_name=elem
        if (actr_name not in lis_vertex ):
            lis_vertex.append(actr_name)

        lis_movies=special_dict[elem]
        for mv in lis_movies:
            mvie_name=mv[0]
            if(mvie_name not in lis_vertex):
                lis_vertex.append(mvie_name)    
            if ((mvie_name,actr_name, mv[2]) not in lis_edges):
                lis_edges.append((mvie_name,actr_name, mv[2]))
    return (lis_vertex, lis_edges)                

## Graph class has verticies, edges and a dictionary for actors
## all query methods are inside this class
class Graph:
    def __init__(self,special_dict):
        vertex_edge=parse_names(special_dict)
        self.verticies=vertex_edge[0]
        self.edges=vertex_edge[1]
        self.movie_actor_dict=special_dict
    def get_vertex(self):
        return self.verticies
    def get_edge(self):
        return self.edges
    ## The following function gets the gross value of a particular movie
    def find_movie_gross(self,movie):
        for edge in self.edges:
            if(edge[0] == movie):
                act_name=edge[1]
                for mvies in self.movie_actor_dict[act_name]:
                    if (mvies[0]== movie):
                        return mvies[2]
        return 0
    ##The following function gets the movies of a particular actor
    def find_actor_movies(self,actor_name):
        actor_movies=[]
        mvies=self.movie_actor_dict[actor_name]
        for mv in mvies:
            actor_movies.append(mv[0])
        return actor_movies
    ##The following function gets actor names in a particular movie
    def find_movies_actors(self, movie_name):
        cast_lis=[]
        for edge in self.edges:
            if(edge[0] == movie_name):
                cast_lis.append(edge[1])
        return cast_lis
    ##The following function gets the actor's that have the top grossing value which is calculated by the movies they work in and the amount that each of their movie made
    def top_gross(self, n):
        grossvals=[]
        for elem in self.movie_actor_dict.keys():
            sum_gross=0
            actor_films=self.movie_actor_dict[elem]
            for film in actor_films:
                sum_gross+= film[2]
            grossvals.append((elem,sum_gross))
        grossvals=(sorted(grossvals, key=lambda x: x[1]))
        if(n <= len(grossvals)):
            list_len=len(grossvals)
            list_len=list_len-n
            return grossvals[(list_len):] 
        else:
            return []
     ##The following looks for an actors age by looking at his/her earliest film and then uses that as a judgement on how old or young the individual is and then returns the top oldest actors    
    def top_age(self, n):
        agevals=[]
        for elem in self.movie_actor_dict.keys():
            min_movie_year=2020
            actor_films=self.movie_actor_dict[elem]
            for film in actor_films:
                if(film[1] != None):
                    if(film[1] < min_movie_year): 
                        min_movie_year= film[1]
            agevals.append((elem,min_movie_year))
        agevals=(sorted(agevals, key=lambda x: x[1]))
        if(n <= len(agevals)):
            return agevals[:n] 
        else:
            return []
     # get movies that were released in a particular year    
    def movie_year(self, year):
        movies=[]
        for elem in self.movie_actor_dict.keys():
            actor_films=self.movie_actor_dict[elem]
            for film in actor_films:
                if(film[1] == year):
                    if(film[0] not in movies):
                        movies.append(film[0])
        return movies
    
    #get actors who were in a movie for a particular year
    def actor_year(self, year):
        actor=[]
        for elem in self.movie_actor_dict.keys():
            actor_films=self.movie_actor_dict[elem]
            for film in actor_films:
                if(film[1] == year): 
                    if(elem not in actor):
                        actor.append(elem)
        return actor
                

## The following our test cases, so the graph was construct based on a small sample data size run earlier on the scraper and with this little data we can determine the right answers to our query and check if the returns values from the function match up to our answers    
special_dict={'Susan_Sarandon': [('Thelma_%26_Louise', 1991, 45000000), ('The_January_Man', 1989, 4611062)], 'Geena_Davis': [('Thelma_%26_Louise', 1991, 45000000), ('Transylvania_6-5000_(1985_film)', 1985, 7196872), ('The_Fly_(1986_film)', 1986, 60000000)],'Jon_Bon_Jovi': [('U-571_(film)', 2000, 127000000)]}    
some_graph=Graph(special_dict)

correct_vertex=['Susan_Sarandon','The_Fly_(1986_film)', 'Jon_Bon_Jovi', 'U-571_(film)','Thelma_%26_Louise', 'The_January_Man', 'Geena_Davis', 'Transylvania_6-5000_(1985_film)']
if(set(correct_vertex) == set(some_graph.get_vertex())):
    print("List of Vertex is Correct")
    
correct_edges=[('Thelma_%26_Louise', 'Susan_Sarandon', 45000000), ('The_January_Man', 'Susan_Sarandon', 4611062), ('Thelma_%26_Louise', 'Geena_Davis', 45000000), ('Transylvania_6-5000_(1985_film)', 'Geena_Davis', 7196872), ('The_Fly_(1986_film)', 'Geena_Davis', 60000000), ('U-571_(film)', 'Jon_Bon_Jovi', 127000000)]
if(set(correct_edges) == set(some_graph.get_edge())):
    print("List of Edges is Correct")    

if(4611062==some_graph.find_movie_gross("The_January_Man")):
    print("Movie gross is correct") 
    
if(set(some_graph.find_actor_movies("Susan_Sarandon"))== set(['Thelma_%26_Louise','The_January_Man'])):
    print("Actor movies is correct")
    
if(set(some_graph.find_movies_actors('Thelma_%26_Louise')) == set(['Susan_Sarandon','Geena_Davis'])):
    print("Cast of a movies is correct")

if(set(some_graph.top_gross(2)) == set([('Jon_Bon_Jovi', 127000000),('Geena_Davis', 112196872)])):    
    print("Top n gross values correct")
    
if(set(some_graph.top_age(1)) == set([('Geena_Davis', 1985)])):
    print("Top n age values correct")
    
if(set(some_graph.movie_year(1991)) == set(['Thelma_%26_Louise'])):
    print("Movies for given year correct")
    
if(set(some_graph.actor_year(1991)) == set(['Geena_Davis','Susan_Sarandon'])):
    print("Actors for given year correct")
    