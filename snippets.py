import argparse
import logging
import psycopg2
import sys


# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

# Initialize postgres connection
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect(database="snippets")
logging.debug("Database connection established.")

# TODO: alphabetize methods

def catalog():
  """List snippet keywords (names)
  
  Returns snippet names.
  """
  with connection, connection.cursor() as cursor:
    cursor.execute("select keyword from snippets where not hidden order by keyword")
    keywords = cursor.fetchall()
  return keywords
  
  
def put(name, snippet, hidden=False):
    """Store a snippet with an associated name.

    Returns the name and the snippet
    """
    cursor = connection.cursor()
    try:
      cursor.execute("insert into snippets values (%s, %s, %s)", (name, snippet, hidden))
    except psycopg2.IntegrityError as e:
      connection.rollback()
      cursor.execute("update snippets set message=%s, hidden=%s where keyword=%s", (snippet, hidden, name))

    connection.commit()
    logging.debug("Snippet {} stored successfully.".format(name))
    
    return name, snippet
    
    
def get(name):
  """Retrieve the snippet with a given name.
  
  If there no such snippet, throw an error to that affect.
  
  Returns the snippet.
  """
  with connection, connection.cursor() as cursor:
    cursor.execute("select keyword, message from snippets where keyword = %s and not hidden", (name, ))
    record = cursor.fetchone()

  if not record:
    # No snippet was found with that name.
    logging.warning("No snippet with name = {} found!".format(name))
    print("No snippet with name = {} found.".format(name))
  else:
    print(record[0], record[1])
    logging.debug("Snippet {} retrieved successfully.".format(name))
    return record[0]
  

def edit(name):
  """Retrieve snippet text with a given name, allow user to replace it 
  with new text.
  
  If there is no such snippet, throw an error to that affect.
  
  Returns the snippet.
  """
  logging.error("FIXME: Unimplemented - edit{!r}".format(name))
  return name
  

def delete(name):
  """Delete snippet with a given name.
  
  If there is no such snippet, throw an error to that affect.
  
  Returns the deleted snippet.
  """
  
  logging.error("FIXME: Unimplemented - delete{!r}".format(name))
  
  
def rename(name):
  """Rename snippet with a given name.
  
  If there is no such snippet, throw an error to that affect.
  
  Returns the new snippet.
  """
  
  logging.error("FIXME: Unimplemented - rename{!r}".format(name))
  

def search(text):
  """Retrieve snippets that contain a piece of text.
  
  Returns a dict of keywords, snippets.
  """
  with connection, connection.cursor() as cursor:
    cursor.execute("select keyword, message from snippets where keyword like '%{}%' or message like '%{}%'".format(text, text))
    records = cursor.fetchall()
  return records
  
  
def main():
  """Main function"""
  logging.info("Constructing parser")
  parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
  
  subparsers = parser.add_subparsers(dest="command", help="Available commands")
  
  # Subparser for the put command
  logging.debug("Constructing put subparser")
  put_parser = subparsers.add_parser("put", help="Store a snippet")
  put_parser.add_argument("name", help="The name of the snippet")
  put_parser.add_argument("snippet", help="The snippet text")
  put_parser.add_argument("--hide", action="store_true", dest="hidden", help="Hide snippet")
  put_parser.add_argument("--show", "--unhide", "--no-hide", "--hide=0", action="store_false", dest="hidden", help="show snippet")

  
  # Subparser for get command
  logging.debug("Construction get subparser")
  get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
  get_parser.add_argument("name", help="The name of the snippet")

  # Subparser for catalog command
  logging.debug("Constructing catalog subparser")
  catalog_parser = subparsers.add_parser("catalog", help="Retrieve list of snippet names")
  
  # Subparser for search command
  logging.debug("Constructing search subparser")
  search_parser = subparsers.add_parser("search", help="Retrieve list of snippets matching text")
  search_parser.add_argument("text", help="The text to search for")

  
  arguments = parser.parse_args(sys.argv[1:])
  
  # Convert parsed arguments from Namespace to dictionary
  arguments = vars(arguments)
  command = arguments.pop("command")
  # TODO: alphabetize if/elif construction
  if command == "put":
    name, snippet = put(**arguments)
    print("Stored {!r} as {!r}".format(snippet, name))
  elif command == "get":
    snippet = get(**arguments)
    print("Retrieved snippet: {!r}".format(snippet))
  elif command == "catalog":
    for keyword in catalog():
      print(keyword[0])
  elif command == "search":
    records = search(**arguments)
    if records:
      for k, v in records:
        print(k, v)
    else:
      print("No matching snippets.")
      
  
if __name__ == "__main__":
  main()