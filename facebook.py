import requests
from bs4 import BeautifulSoup
from credentials import (EMAIL, PASSWORD)
from constans import (ROOT_URL, LOGIN_FORM_SELECTOR)


def login(url, credentials):
    """ input 
            - url = m.facebook.com url 
            - credentials = tuple of email, facebook

        return 
            requests.Session object
    """
    headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
    sess = requests.Session()

    resp = sess.get(url, headers=headers)

    # get form data
    soup = BeautifulSoup(resp.content, 'html.parser')
    form = soup.select(LOGIN_FORM_SELECTOR)[0]
    action_url = form['action']
    hidden_data = form.findAll("input", {'type': 'hidden'})
    data_dict = {x['name']: x['value'] for x in hidden_data} 
    data_dict.update({'email': credentials[0], 'pass': credentials[1], 'login': 'Masuk'})

    login_resp = sess.post(action_url, data=data_dict, headers=headers)
    return login_resp, sess



if __name__ == '__main__':
    resp, sess = login(ROOT_URL, (EMAIL, PASSWORD))
    print(resp.text)
    assert 'Kirim' in resp.text, "Kirim not found"
