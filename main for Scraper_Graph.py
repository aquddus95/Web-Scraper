import io
import sys
import time
import logging
import bs4 as bs
import urllib.request
from pip._vendor.distlib.compat import raw_input
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
    def find_movie_gross(self,movie):
        for edge in self.edges:
            if(edge[0] == movie):
                act_name=edge[1]
                for mvies in self.movie_actor_dict[act_name]:
                    if (mvies[0]== movie):
                        return mvies[2]
        return 0
    def find_actor_movies(self,actor_name):
        actor_movies=[]
        mvies=self.movie_actor_dict[actor_name]
        for mv in mvies:
            actor_movies.append(mv[0])
        return actor_movies
    def find_movies_actors(self, movie_name):
        cast_lis=[]
        for edge in self.edges:
            if(edge[0] == movie_name):
                cast_lis.append(edge[1])
        return cast_lis
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
    def movie_year(self, year):
        movies=[]
        for elem in self.movie_actor_dict.keys():
            actor_films=self.movie_actor_dict[elem]
            for film in actor_films:
                if(film[1] == year):
                    if(film[0] not in movies):
                        movies.append(film[0])
        return movies
    
    def actor_year(self, year):
        actor=[]
        for elem in self.movie_actor_dict.keys():
            actor_films=self.movie_actor_dict[elem]
            for film in actor_films:
                if(film[1] == year): 
                    if(elem not in actor):
                        actor.append(elem)
        return actor

#function gets movies that the actor took part in, checks for a table tag and links near Filmography span tag
def find_actor_movies(result,actor_has_info, movie_list,val):
    if(val == 0):
        movie_table=result.findNext('table')
    else:
        movie_table=result.findNext('ul')

    if((movie_table != None) and val == 0):
        #create actor node and movie table   
        movie_table= movie_table.findAll('tr')
        if(movie_table != None):
            actor_has_info+=1
            for row in movie_table:
                link=row.find('a')
                if(link != None):
                    try:
                        movie_name=str(link['href'])
                        movie_name_parsed=movie_name.split('/')
                        try:
                            movie_list.append(movie_name_parsed[2]) 
                        except:
                            logging.error(movie_name+" is an invalid link")
                    except:
                        logging.warning("Problem with a tag")
         
    
    elif(movie_table != None and val == 1):
        movie_table= movie_table.findAll('a')
        if(movie_table != None):
            actor_has_info+=1
            for link in movie_table:
                if(link != None):
                    try:
                        movie_name=str(link['href'])
                        movie_name_parsed=movie_name.split('/')
                        try:
                            movie_list.append(movie_name_parsed[2])
                        except:
                            logging.error(movie_name+" is an invalid link")
                    except:
                        logging.warning("Problem with a tag")
    
    return(actor_has_info,movie_list)


## the following checks if the actor has a valid wiki page
def film_link(page_link, some_name):
    page_formatted=None
    valid_url=True
    try: 
        html_page= urllib.request.urlopen(page_link).read()
        page_formatted=bs.BeautifulSoup(html_page,'lxml')
        
    except urllib.error.URLError as err:
        logging.info("Actor Movie Link For " + some_name + " Not Found")
        valid_url=False
    return (valid_url,page_formatted)


## general function thats calls all subfunctions to get actor info and his or her movies
def get_actor_info(some_name):
    actor_has_info=0
    val=0
    movie_list=[]
    seperate_film_page=False 
    head_link="https://en.wikipedia.org/wiki/"
    page_link=head_link+some_name
    is_valid= film_link(page_link, some_name)
          
    if(is_valid[0] == True):
        found_tags=False
        page_formatted=is_valid[1]
        result =page_formatted.find("span", { "id" : "Film" })

        if(result == None):
            result =page_formatted.find("span", { "id" : "Films" })

        if(result == None):
            result =page_formatted.find("span", { "id" : "Filmography" })
            if(result != None):
                val=1
                
        if(result == None):
            result =page_formatted.find("span", { "id" : "Selected_filmography" })
            if(result != None):
                val=1
                
        if(result == None):
            result =page_formatted.find("span", { "id" : "Filmography_(selected)" })
            if(result != None):
                val=1 
        
        if(result != None):
            found_tags=True
            
        if(found_tags != False):
            actor_info_movie_list=find_actor_movies(result,actor_has_info,movie_list,val)
            actor_has_info=actor_info_movie_list[0]
            movie_list=actor_info_movie_list[1]                                
            if(movie_list):
                actor_has_info+=1            
    if(actor_has_info==2):
        return(True,movie_list)
    else:
        return(False,[]) 

##function parses box office money amount string to get correct box office amount as an integer
def get_money(boxoffice):
    new_money=[]
    money=str(boxoffice.get_text())
    try:
        for i in money:
            if not(i.isdigit()):
                
                if(i == '['):
                    break
                if(i == ']'):
                    break
                if(i == '.'):
                    break
                if(i == ','):
                    continue
                else:    
                    continue
            else:
                new_money.append(i)
        new_money=''.join(new_money)
        if(new_money):
            new_money=int(new_money)
            if( money.find("million") != -1):
                new_money= new_money * 1000000

            elif( money.find("billion") != -1):    
                new_money= new_money * 1000000000
    except:
        new_money=[]
     
    if(type(new_money) is int):
        return new_money
    
    else:
        return 0
    
## function gets the year that the movie was released in
def get_year(release):
    year=1
    releaseinfo=release.find("span", {"class" :"bday dtstart published updated"})
    if(releaseinfo != None):
        releaseyear=str(releaseinfo.get_text())
        releaseyear_parsed=releaseyear.split('-')
        try:
            year=int(releaseyear_parsed[0])
        except:
            year=1
    return year
    

##finds if there is a box office value or release date span tag and then tries to locate the correct tag location
def box_office_release(txt,tag_id,page_formatted, found_tags, movie_name):
    tag=None
    try:
        tag =page_formatted.find(text=txt).findNext(tag_id)
    except:
        print(movie_name + " No " +txt)
        tag =None 

    if(tag != None):
        found_tags+=1
    return(tag,found_tags)


##general overall function for getting movie info
def get_movie_info(movie_name):
    valid_url=True
    found_tags=0
    page_link="https://en.wikipedia.org/wiki/"
    page_link=page_link+movie_name
    try: urllib.request.urlopen(page_link)
    except urllib.error.URLError as err:
        logging.error("Movie Link  Not Found")
        valid_url=False

    if(valid_url == True):
        box_office= "No Number"
        release_date= "No date"
        cast=[]
        html_page= urllib.request.urlopen(page_link).read()
        page_formatted=bs.BeautifulSoup(html_page,'lxml') 

        
        boxoffice=box_office_release("Box office",'td',page_formatted, found_tags,movie_name)
        found_tags=boxoffice[1]
        if(boxoffice[0] != None):
            box_office=get_money(boxoffice[0])
        
        else:
            box_office= None
        
        if(found_tags == 1):
            release=box_office_release("Release date",'li',page_formatted, found_tags, movie_name)
            found_tags=release[1]
            release_date=get_year(release[0])
            if(release_date == 1):
                release_date= None

        if(found_tags == 2):
            td_tag_starring=None
            try:
                td_tag_starring =page_formatted.find(text="Starring").findNext("div", { "class" : "plainlist" })
            except:
                print(movie_name+ " No Cast ")
                cast=[]
                
            if(td_tag_starring != None):
                cast_links=td_tag_starring.findAll('a')
                if(cast_links != None):
                    found_tags+=1
                    for actor in cast_links:
                        actor_movie=str(actor['href'])
                        actor_movie_parsed= actor_movie.split('/')
                        try:
                            cast.append(actor_movie_parsed[2]) 
                        except:
                            print(actor_movie+" is an invalid link")
                            
                            
    if(found_tags ==3):
        return(True,box_office,release_date,cast)
    else:
        return(False,None,None, [])






  actor_count=0
movie_count=0
movie_added=0
global_movie=[]
movies=[]

global_actor=[]
actor=[]
movie_actor={}

user_name=raw_input("Name of Actor ")
actor.append(user_name)

while(1 ):
    if(actor):
        actor_name=actor.pop(0)
        if(actor_name not in global_actor):
            actorvals=get_actor_info(actor_name)
            if(actorvals[0]):
                global_actor.append(actor_name)
                actor_count+=1
                if(movie_added < 1000):
                    for mv in actorvals[1]:
                        if mv not in movies:
                            movies.append(mv)
                            movie_added+=1
    if(movies):
        movie_name=movies.pop(0)
        if(movie_name not in global_movie):
            movievals=get_movie_info(movie_name)
            if(movievals[0]):
                global_movie.append(movie_name)
                movie_count+=1
                for act in movievals[3]:
            
                    if not(act in movie_actor.keys()):
                        movie_actor[act]= []
                        movie_actor[act].append((movie_name,movievals[2],movievals[1]))
                    else:
                         movie_actor[act].append((movie_name,movievals[2],movievals[1]))
                    
                    if act not in actor:
                        actor.append(act)
    if(movie_count > 125 and actor_count > 250):
        break
            
logging.info(global_movie) 
logging.info(global_actor)
logging.info(movies)
logging.info(actor)
print(movie_actor)
some_graph=Graph(movie_actor)
#print(some_graph.get_vertex())
#print(some_graph.get_edge())
movie=raw_input( "Give Movie Name for gross ")
print(some_graph.find_movie_gross(movie))
actor=raw_input( "Give Actor Name for his/her movies ")
print(some_graph.find_actor_movies(actor))
movie=raw_input( "Give Movie Name to find out the cast ")
print(some_graph.find_movies_actors(movie))

n=raw_input("top n gross actors give n val ")
print(some_graph.top_gross(int(n)))


n=raw_input("top n old actors give n val ")
print(some_graph.top_age(int(n)))


year=raw_input("movie year to find movies ")
print(some_graph.movie_year(int(year)))

year=raw_input("give year to find actors that had a movie in ")
print(some_graph.actor_year(int(year)))









