from filter import LogFilter

# include = ['aa','dog']
# exclude = ['cc']
a = LogFilter("aa,dog", "cc")
assert a.filter("dogaa") == True
assert a.filter("dogaacc") == False
assert a.filter("dogcc") == False
assert a.filter("dogca") == True
