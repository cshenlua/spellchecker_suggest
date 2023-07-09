# spellchecker_suggest
A simple program that reads over a document and suggests spelling changes for the document, providing recommendations using the minimum-edit-distance algorithm.

## Run 
```python3 spellchecker.py <file_name> words```

## Demo 
Below are the contents of a .txt file, you may notice that there are some obvious spelling errors : 
```
you wioll rejoice to hear that no disaster have accompany the
commencement of an enterprise which you have regard with such evil
foreboding. I arrive here yesterdy, and my first task is to assure
my dear sister of my welfure and increasing confidence in the success
of my undertaking.
```
### Output : 
```
mispelled word: wioll -- (line: 1) -- suggested words : [ill, will, swill]
mispelled word: yesterdy -- (line: 3) -- suggested words : [yester, yesterday]
mispelled word: welfure -- (line: 4) -- suggested words : [welfare]
```
