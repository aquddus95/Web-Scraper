import io
import time
import bs4 as bs
import urllib.request
## Helper function tries to locate a table or list of movies that the actor acted in the specific actor Wikipedia Page
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
                            print(movie_name+" is an invalid link")
                    except:
                        print("Problem with a tag")
         
    
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
                            print(movie_name+" is an invalid link")
                    except:
                        print("Problem with a tag")
    
    return(actor_has_info,movie_list)

## Helper Function makes sure there is a valid Wikipedia Page for an actor
def film_link(page_link, some_name):
    page_formatted=None
    valid_url=True
    try: 
        html_page= urllib.request.urlopen(page_link).read()
        page_formatted=bs.BeautifulSoup(html_page,'lxml')
        
    except urllib.error.URLError as err:
        print("Actor Movie Link For " + some_name + " Not Found")
        valid_url=False
    return (valid_url,page_formatted)

#After verifying that an actor has a Wikipedia Page, the function finds the portion of the Page that has the names of the movies that the actor acted in
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
## The following is a helper function that parses the box office amount of a movie which is given in a forum of a string and has abbreviations for its amount (millions instead of 000,000,000 and billions instead of 000,000,000,000)
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
## The following is a helper function that looks for the year for which the movie was released in    
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

## The main helper function that makes calls to both the box office helper function and get_year of a movie helper function
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


## Overall movie function that validates a movie wikipedia page and then parses the required information (release date/box office) using the helper functions mentioned above
def get_movie_info(movie_name):
    valid_url=True
    found_tags=0
    page_link="https://en.wikipedia.org/wiki/"
    page_link=page_link+movie_name
    try: urllib.request.urlopen(page_link)
    except urllib.error.URLError as err:
        print("Movie Link  Not Found")
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

    
## Main portion of the code where the Scraper initially starts at Harrison Ford and then continues to scrape movie and actor information
## until limits of 125 and 250 are hit for movie count and actor count
actor_count=0
movie_count=0
movie_added=0
global_movie=[]
movies=[]

global_actor=[]
actor=[]
movie_actor={}

actor.append("Harrison_Ford")

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
            
print(global_movie) 
print(global_actor)
print(movies)
print(actor)
print(movie_actor)
