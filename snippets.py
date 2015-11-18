import logging

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet):
    """
    Store a snippet with an associated name.

    Returns the name and the snippet
    """
    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    return name, snippet
    
    
def get(name):
  """Retrieve the snippet with a given name.
  
  If there no such snippet, throw an error to that affect.
  
  Returns the snippet.
  """
  
  logging.error("FIXME: Unimplemented - get{!r})".format(name))
  return ""
  

def edit(name):
  """Retrieve snippet text with a given name, allow user to replace it 
  with new text.
  
  If there is no such snippet, throw an error to that affect.
  
  Returns the snippet.
  """
  
  logging.error("FIXME: Unimplemented - edit{!r}".format(name))

def delete(name):
  """Delete snippent with a given name.
  
  If there is no such snippet, throw an error to that affect.
  
  Returns the deleted snippet.
  """
  
  logging.error("FIXME: Unimplemented - delete{!r}".format(name))
  
  