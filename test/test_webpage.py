from bs4 import BeautifulSoup
import pytest
import pickle
import requests

def cmp(a, b):
    return (a > b) - (a < b)

class TestWebpage:
    @pytest.fixture(autouse=True)
    def get_soup(self):
        
        index_page = requests.get("http://localhost:8000/index.html")
        soup_index = BeautifulSoup(index_page.content, 'html.parser')
        self._index = soup_index

        login_page = requests.get("http://localhost:8000/login.html")
        soup_login = BeautifulSoup(login_page.content, 'html.parser')
        self._login = soup_login

        spa_page = requests.get("http://localhost:8000/spa.html")
        soup_spa = BeautifulSoup(spa_page.content, 'html.parser')
        self._spa = soup_spa

        appliance_page = requests.get("http://localhost:8000/appliance.html")
        soup_appliance= BeautifulSoup(appliance_page.content, 'html.parser')
        self._appliance = soup_appliance

    def testHomePage(self):
        soup = self._index.find('header')
        site = soup.find('nav')
        site_li = site.find_all('li')
        assert len(site_li) == 5
        count = 0   
        for li in site_li:
            if li.a.string =='Home':
                assert li.a['href'] == 'index.html'
            if li.a.string == 'Login':
                assert li.a['href'] == 'login.html'
            if li.a['href'] == '#':
                if li.a.string == 'News':
                    count = count + 1
                if li.a.string == 'Contact':
                    count = count + 1
                if li.a.string == 'About':
                    count = count + 1
                
        assert count == 3

        soup = self._index.find('section',{'class':'banner'})
        site_form = soup.find('form')
        site_select = site_form.find('select')
        count = 0
        for a in site_select.find_all('option'):
            if a.string == 'Hyderabad':
                count = count + 1    
            if a.string == 'Chennai':
                count = count + 1    
            if a.string == 'Banglore':
                count = count + 1    
            if a.string == 'Kolkata':
                count = count + 1    

        assert count == 4

        site_search = soup.find('input')
        assert site_search['type'] =='text' and site_search['placeholder'] == 'Search for a service'
        
        site_button = soup.find('button')
        assert site_button.string == 'Search'

        soup = self._index.find('section',{'class':'main-content'})
        soup_rowdiv = soup.find('div',{'class':'row'})
        soup_col = soup_rowdiv.find_all('div',{'class':'col'})
        
        assert soup_col[0].a['href'] == 'appliance.html' and soup_col[0].p.string == 'Air Conditioners' and soup_col[0].img['src']=='/media/ac.png'
        assert soup_col[1].a['href'] == 'appliance.html' and soup_col[1].p.string == 'Washing Machines' and soup_col[1].img['src']=='/media/wash.png'
        assert soup_col[2].a['href'] == 'appliance.html' and soup_col[2].p.string == 'Computers' and soup_col[2].img['src']=='/media/comp.png'
        assert soup_col[3].a['href'] == 'appliance.html' and soup_col[3].p.string == 'Refrigerators' and soup_col[3].img['src']=='/media/fridge.png'
        assert soup_col[4].a['href'] == 'spa.html' and soup_col[4].p.string == 'Spa at home' and soup_col[4].img['src']=='/media/spa.png'

        soup = self._index.find('footer')
        assert soup.h5.string is not " "

    def testLoginPage(self):
        soup = self._login.find('footer')
        assert soup.h5.string is not " "

        soup = self._login.find('header')
        site = soup.find('nav')
        site_li = site.find_all('li')
        assert len(site_li) == 5
        count = 0   
        for li in site_li:
            if li.a.string =='Home':
                assert li.a['href'] == 'index.html'
            if li.a.string == 'Login':
                assert li.a['href'] == 'login.html'
            if li.a['href'] == '#':
                if li.a.string == 'News':
                    count = count + 1
                if li.a.string == 'Contact':
                    count = count + 1
                if li.a.string == 'About':
                    count = count + 1
                
        assert count == 3

        soup = self._login.find('section',{'class':'banner'})
        assert soup is not ""

        soup = self._login.find('section',{'class':'main-content'})
        site_form = soup.find('form')
        site_input = site_form.find_all('input')

        count = 0
        for a in site_input:
            if a['type'] == 'text' and a['placeholder'] == 'Enter Username':
                count =  count + 1
            if a['type'] == 'password' and a['placeholder'] == 'Enter Password':
                count =  count + 1
             
        assert count == 2
        assert len(site_form.find_all('label')) == 2
        button =  site_form.find_all('button')
        assert button[0].string == 'Login'
        assert button[1].string == 'Cancel'

    def testAppliancePage(self):
        soup = self._appliance.find('header')
        site = soup.find('nav')
        site_li = site.find_all('li')
        assert len(site_li) == 5
        count = 0   
        for li in site_li:
            if li.a.string =='Home':
                assert li.a['href'] == 'index.html'
            if li.a.string == 'Login':
                assert li.a['href'] == 'login.html'
            if li.a['href'] == '#':
                if li.a.string == 'News':
                    count = count + 1
                if li.a.string == 'Contact':
                    count = count + 1
                if li.a.string == 'About':
                    count = count + 1
                
        assert count == 3

        soup = self._appliance.find('section',{'class':'banner'})
        site_form = soup.find('form')
        site_select = site_form.find('select')
        count = 0
        for a in site_select.find_all('option'):
            if a.string == 'Hyderabad':
                count = count + 1    
            if a.string == 'Chennai':
                count = count + 1    
            if a.string == 'Banglore':
                count = count + 1    
            if a.string == 'Kolkata':
                count = count + 1    

        assert count == 4

        soup = self._appliance.find('footer')
        assert soup.h5.string is not " "

        soup = self._appliance.find('section',{'class':'main-content'})
        assert len(soup.find_all('label'))==3
        assert len(soup.find_all('select'))==3

        label = soup.find_all('label')
        assert label[0].string == 'Select the device'
        assert label[1].string == 'Select the issue'
        assert label[2].string == 'Select the time slot'
        

        site_select = soup.find_all('select')
        option = site_select[0].find_all('option')
        assert option[0].string == 'AirConditioner'
        assert option[1].string == 'Refrigerator'
        assert option[2].string == 'Computer'
        assert option[3].string == 'Washing Machine'
        
        soption = site_select[1].find_all('option')
        assert soption[0].string == 'Not switching on'
        assert soption[1].string == 'General Service'
        assert soption[2].string == 'Missing/Faulty Parts'
        assert soption[3].string == 'External Damage'
        
        toption = site_select[2].find_all('option')
        assert toption[0].string == '9AM - 12AM'
        assert toption[1].string == '12PM - 3PM'
        assert toption[2].string == '3PM - 6PM'
        assert toption[3].string == '6PM - 9PM'

        site_button = soup.find_all('button')
        assert site_button[0].string == 'Submit Request'
        assert site_button[1].string == 'Cancel'


    def testSpaPage(self):
        soup = self._spa.find('header')
        site = soup.find('nav')
        site_li = site.find_all('li')
        assert len(site_li) == 5
        count = 0   
        for li in site_li:
            if li.a.string =='Home':
                assert li.a['href'] == 'index.html'
            if li.a.string == 'Login':
                assert li.a['href'] == 'login.html'
            if li.a['href'] == '#':
                if li.a.string == 'News':
                    count = count + 1
                if li.a.string == 'Contact':
                    count = count + 1
                if li.a.string == 'About':
                    count = count + 1
                
        assert count == 3

        soup = self._spa.find('section',{'class':'banner'})
        site_form = soup.find('form')
        site_select = site_form.find('select')
        count = 0
        for a in site_select.find_all('option'):
            if a.string == 'Hyderabad':
                count = count + 1    
            if a.string == 'Chennai':
                count = count + 1    
            if a.string == 'Banglore':
                count = count + 1    
            if a.string == 'Kolkata':
                count = count + 1    

        assert count == 4

        soup = self._spa.find('footer')
        assert soup.h5.string is not " "

        soup = self._spa.find('section',{'class':'main-content'})
        assert len(soup.find_all('label'))==2
        assert len(soup.find_all('select'))==2
        site_select = soup.find_all('select')
        ooption = site_select[0].find_all('option')
        assert ooption[0].string == 'Hair Styling'
        assert ooption[1].string == 'Nail Spa'
        assert ooption[2].string == 'Massage'
        assert ooption[3].string == 'Makeup'

        toption = site_select[1].find_all('option')
        assert toption[0].string == '9AM - 12AM'
        assert toption[1].string == '12PM - 3PM'
        assert toption[2].string == '3PM - 6PM'
        assert toption[3].string == '6PM - 9PM'

        site_button = soup.find_all('button')
        assert site_button[0].string == 'Submit Request'
        assert site_button[1].string == 'Cancel'