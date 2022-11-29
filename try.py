import re
string = 'var i=\'&#109;a\'+\'i&#108;\'+\'&#116;o\';var a=\'durkovic&#46;peter&#64;gmail&#46;com\';document.write(\'<a href="\'+i+\':\'+a+\'\"  class=\"emailLink eyJqIjoiZCJ9\" onclick=\"ga_track( \"company_detail\", \"multimedia\", \"email\" ); _kt.i( 1324894, 20 );\">\'+a+\'</a>\');'
match=(re.search('&#64;', string))
index = match.start()
indexForward = index
indexBackward = index
mail = ""

while string[indexBackward] != '\'':
    mail += string[indexBackward]
    indexBackward -= 1
mail = mail[::-1]
while string[indexForward] != '\'':
    mail += string[indexForward]
    indexForward += 1
mail = mail.replace("&#46;", ".").replace("&&#64;", "@")
print(mail)
