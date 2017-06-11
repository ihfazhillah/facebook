# Facebook

a simple script to upload facebook status using your account. not from a graph
API.

## How to use

1. install `requests` and `bs4` package from `pypi`
2. open the shell and type:

```python
from facebook import Facebook

fb = Facebook(("youremail", "yourpassword"))
fb.update_status("your status here")
```

**Note** you need to pass a tuple in `Facebook` initialization.

or you can use the old way

```python
from facebook import login, update_status

resp, sess = login("http://m.facebook.com", ("youremail", "yourpassword"))
resp, sess = update_status(resp, sess, "your status")
```

Thats, Easy enough... !!
