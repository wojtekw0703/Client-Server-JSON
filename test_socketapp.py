import unittest
from unittest.mock import patch
from server import message_user,User, table_user


def user_dashboard(login):
    if message_user.count(User.login == login) > 5:
        print(f"{login} - inbox overflow \n")

                
class TestServer(unittest.TestCase):
    def test_message_database(self):
        message = message_user.search(User.login=='aneta')
        self.assertEqual(message,[{'login': 'aneta', 'message': 'I am newbie'}]) 
    
    @patch('builtins.print')
    def test_inbox_overflow(self, mock_print):
        user_dashboard('wojtek')
        mock_print.assert_called_with('wojtek - inbox overflow \n')

    def test_insert(self):
        table_user.insert({'login': 'test', 'password': 'test'})
        account = table_user.search(User.login=='test')
        self.assertEqual(account,[{'login': 'test', 'password': 'test'}]) 
    



if __name__ == "__main__":
    unittest.main() 