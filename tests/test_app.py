import unittest
from app import app, db
from models import User

class UserTestCase(unittest.TestCase):

    def setUp(self):
        app.config.from_object('config.TestingConfig')
        self.app = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_create_user(self):
        response = self.app.post('/users', json={
            'username': 'testuser',
            'role': 'films'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created successfully', response.get_data(as_text=True))

    def test_get_all_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_specific_user(self):
        user = User(username='testuser', role='films')
        db.session.add(user)
        db.session.commit()
        response = self.app.get(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['username'], 'testuser')

    def test_update_user(self):
        user = User(username='testuser', role='films')
        db.session.add(user)
        db.session.commit()
        response = self.app.put(f'/users/{user.id}', json={
            'username': 'updateduser',
            'role': 'people'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('User updated successfully', response.get_data(as_text=True))
        updated_user = db.session.get(User, user.id)  # Updated
        self.assertEqual(updated_user.username, 'updateduser')
        self.assertEqual(updated_user.role, 'people')

    def test_delete_user(self):
        user = User(username='testuser', role='films')
        db.session.add(user)
        db.session.commit()
        response = self.app.delete(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('User deleted successfully', response.get_data(as_text=True))
        deleted_user = db.session.get(User, user.id)  # Updated
        self.assertIsNone(deleted_user)

    def test_get_ghibli_data(self):
        user = User(username='testuser', role='films')
        db.session.add(user)
        db.session.commit()
        response = self.app.get(f'/users/{user.id}/ghibli')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

if __name__ == '__main__':
    unittest.main()
