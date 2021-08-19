try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

#config=ConfigParser()

# instantiate
#class recipe():

config = ConfigParser() 

#def __init__(self, config = 0):
#     self.config = config
  
# getter method
#def get_config(self):
#    return self.config
  
# setter method
#def set_config(self):
#    self.config = ConfigParser() 
    
    
def open_ini(path):
    # parse existing file
    config.read(path)  
    
#def openstr(string):
#    try:
#        config.read_string(string)  
#        return True
#    except:
#        return False

def save_ini(p):
    # save to a file
    #config.write(path)
    #with open(path, 'w') as configfile:
    print(p)
    with open(p, 'w') as out:
        config.write(out)


def readint(header,item):    
    read=config.getint(header,item)
    return read

def readstr(header,item):    
    read=config.get(header,item)
    return read

def readfloat(header,item):    
    read=config.getfloat(header,item)
    return read
        
def set(header,item,value):
    config.set(header,item,str(value))
    



#and (item in dict(config.items(header)))


#print(open("Default.ini"))
#print(config)
#white_size=read_str("white_defects","white_local_size")    
#print(white_size)

# read values from a section
#string_val = config.get('section_a', 'string_val')
#bool_val = config.getboolean('section_a', 'bool_val')
#int_val = config.getint('section_a', 'int_val')
#float_val = config.getfloat('section_a', 'pi_val')

# update existing value
#config.set('section_a', 'string_val', 'world')


# add a new section and some values
#config.add_section('section_b')
#config.set('section_b', 'meal_val', 'spam')
#config.set('section_b', 'not_found_val', '404')

