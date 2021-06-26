from unittest import TestCase

from app import app 
from models import db, User 

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False 

db.drop_all()
db.create_all()

class PetViewsTestCase(TestCase):
    "Test views for Users"

    def setUp(self):
        """Add sample user"""

        User.query.delete()

        user = User(first_name = "Jamie", last_name="Foxx", img_url="https://media1.popsugar-assets.com/files/thumbor/ENkPPbStnnsZFm5O0dkX7psHb1k/199x110:2667x2578/fit-in/2048xorig/filters:format_auto-!!-:strip_icc-!!-/2020/03/03/040/n/1922398/c2cd1cf85e5eef0faee127.72402681_/i/Jamie-Foxx.jpg")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id 
        self.user = user
    
    def tearDown(self):
        db.session.rollback()
    
    def test_redirect_home(self):
        with app.test_client() as client:
            resp = client.get('/')
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/users")

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Jamie', html)
            self.assertIn('Foxx', html)


    def test_user_details(self):
        with app.test_client() as client: 
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Jamie Foxx</h1>', html)
            self.assertIn(self.user.img_url, html)
    
    def test_add_user(self):
        with app.test_client() as client:
            new_user = {'first_name':'Mike', 'last_name': 'Tyson', 'img_url': "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Mike_Tyson_2019_by_Glenn_Francis.jpg/220px-Mike_Tyson_2019_by_Glenn_Francis.jpg"}

            resp = client.post('/users/new', data = new_user, follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Mike Tyson', html)
    
    def test_delete_user(self):
        with app.test_client() as client: 
            resp = client.post(f'users/{self.user_id}/delete', follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotEqual('Jamie', html)