import os, urllib.parse
os.chdir(r'D:\AiWordSpace')
path = '/Java%E9%9D%A2%E8%AF%95%E5%AE%9D%E5%85%B8_%E6%80%BB%E7%9B%AE%E5%BD%95.html'
path = urllib.parse.unquote(path, errors='surrogatepass')
print('decoded:', repr(path))
words = [w for w in path.split('/') if w]
print('words:', words)
full = os.getcwd()
for w in words:
    full = os.path.join(full, w)
print('full:', repr(full))
print('exists:', os.path.exists(full))