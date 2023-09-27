
import musicbrainzngs
import wikipedia

musicbrainzngs.set_useragent('djai', '0.1', 'http://example.com')

result = musicbrainzngs.search_recordings('Oblivion', artist='Grimes', limit=1)

for recording in result['recording-list']:
    print('Title:', recording['title'])
    print('Artist:', recording['artist-credit'][0]['artist']['name'])
    print('Length:', recording['length'])
    print('ID:', recording['id'])

wikipedia.set_lang('en')

page_py = wikipedia.page('Oblivion (Grimes song)')

print('Page - Summary: %s' % page_py.summary)
