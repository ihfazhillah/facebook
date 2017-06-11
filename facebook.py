import requests
from bs4 import BeautifulSoup
from credentials import (EMAIL, PASSWORD)
from constans import (ROOT_URL, LOGIN_FORM_SELECTOR, COMPOSER_SELECTOR)


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

    # need to skip new facebook auth system
    login_resp = sess.get(url + "/login/save-device/cancel/?ref=dbl")

    return login_resp, sess

def post_status(login_resp, session, status):
    """input
            - login_resp = response dari login (halaman home/redirect setelah login)
            - session = session yang digunakan untuk login
            - status = string, status facebook yang akan di post

        return 
            requests.Session object, response object
    """

    # get form data
    soup = BeautifulSoup(login_resp.content, 'html.parser')
    form = soup.select(COMPOSER_SELECTOR)[0]
    action_url = form['action']
    hidden_data = form.findAll("input", {"type": "hidden"})
    hidden_data.pop()
    data_dict = {x['name']: x['value'] for x in hidden_data}

    data_dict.update({'xc_message': status, 'rst_icv': '', 'view_post': 'Kirim'})

    after_post_resp = session.post(requests.compat.urljoin(ROOT_URL, action_url), data=data_dict)

    return after_post_resp, session

if __name__ == '__main__':
    resp, sess = login(ROOT_URL, (EMAIL, PASSWORD))
    assert 'Kirim' in resp.text, "Kirim not found"

    resp, sess = post_status(resp, sess, "ini saya coba dengan script requests dari \n http://docs.python-requests.org/en/master/user/quickstart/")
    assert "Anda telah memperbarui status Anda" in resp.text, "Anda telah memperbarui status Anda tidak ditemukan"
