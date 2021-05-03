from . import main

@main.route('/')
def index():

  '''
  View root page function that returns the index page and its data
  '''

  title = 'Chat'

  return '<h1>Hello Joy</h1>'