from django.test import TestCase

# Create your tests here.
from Todo.models import TodoDB
from django.utils import timezone
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse


def setup():
    '''Creating a test user'''
    user = User.objects.create_user(username='test', email='test@test.com')
    user.set_password('12345')
    #Tip: f you set the password through the argument, it will be saved as hash of 12345, so this is the right way
    user.save()
    return user

class Models_test(TestCase):
    '''Class to check functioning of models'''

    def test_1_add_object_as_owner(self):
        '''Checking if the test user can add object'''

        dummy = TodoDB.objects.create(item_text="Testing",date_added=timezone.now(), owner=setup())
        self.assertEqual(TodoDB.objects.get(id=dummy.id).item_text, "Testing")


    def test_2_del_object_as_owner(self):
        '''Checking if the test user can delete object'''

        dummy = TodoDB.objects.create(item_text="Testing", date_added=timezone.now(), owner=setup())
        TodoDB.objects.get(id=dummy.id).delete()
        #Tip: This delete issues object deletion in the db but python instance (dummy) remains alive. So, query needs to b
        #Tip:  fetched again as previous query is still stored in python variable dummy. >> https://docs.djangoproject.com/en/2.1/ref/models/instances/#django.db.models.Model.delete

        self.assertQuerysetEqual(TodoDB.objects.all(), [])
        self.assertRaises(TodoDB.DoesNotExist, TodoDB.objects.get, id=dummy.id)
        #Tip: Here TodoDB.DoesNotExist is the exception, TodoDB.objects.get is the callable, and id=dummy.id is the argument.

    def test_3_add_object_as_Anonymous_user(self):
        '''Checking if the Anonymous user can add object'''

        self.assertRaises(ValueError, TodoDB.objects.create, item_text='Testing', date_added=timezone.now(), owner=AnonymousUser())
        #Tip: If you're expecting Thing(name='1234') to raise an exception, then it should be written like this: self.assertRaises(FooException, Thing, name='1234');
        #Tip: Unittest's assertRaises takes a callable [i.e the function] and arguments [function's arguments]
        #Tip: Creating an object with Anonymous user (which is not allowed in our model) before assertRaise will itself raise issue before it goes to assert.




def create_object():
    '''This function creates an entry with owner/user- test'''
    dummy = TodoDB.objects.create(item_text="Testing", date_added=timezone.now(), owner=setup())
    return dummy

class Views_test(TestCase):
    '''This class contains all the view functions tests for this app'''

    def test_4_add_and_view_object_as_owner(self):
        '''create user, login and view entry'''
        # Create user
        setup()

        # login as user
        login = self.client.login(username='test', password='12345')
        self.assertTrue(login)
        # add entry as owner
        self.client.post(reverse('todo:add'), {'item': 'Hello'})
        # item is the form_name that we are passing through POST method

        # Going to home page and checking if the query has Hello.

        response = self.client.get(reverse('todo:list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['context'], ['<TodoDB: Hello>'])
        self.assertContains(response, "Hello")

    def test_5_delete_object_as_owner(self):
        ''' create user, login and delete entry'''

        a = create_object()
        #Tip: TestCase comes with its own client, so no need to use Client()
        login = self.client.login(username='test', password='12345')
        self.assertTrue(login)
        response1=self.client.get(reverse('todo:del', args=[a.id])) #or args(a.id,)

        #checking the redirection after deleting the entry
        self.assertRedirects(response1, expected_url='/list/', target_status_code=200)

        #Verify the entry is not present after deleting
        response=self.client.get(reverse('todo:list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context_data['context'], [])
        #Tip: 'context' is the name of context_object_name from views
        #Tip:  context_data the from generic.ListView's context
        self.assertNotContains(response,"Testing")

    def test_6_view_data_when_not_loggedin(self):
        ''' Creating element using test user and try to view as anonymous user.'''
        create_object()
        #User tries to visit index  page ie / which asks user to login
        response= self.client.get(reverse('todo:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry! You must login to view your items.")
        #User tries to visit home page ie /index/ which contains details of object
        response = self.client.get(reverse('todo:list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/accounts/login/?next=/list/', target_status_code=404)


    def test_7_add_object_when_not_loggedin(self):
        '''User logs in, adds entry and views entry'''

        #add entry when not loggedin
        response =self.client.post(reverse('todo:add'), {'item':'Hello'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response ,expected_url="/accounts/login/?next=/add_item/",target_status_code=404)
        # The above line checks if the redirect is being done to the expected url with target_Status_code=404

    def test_8_delete_object_when_not_loggedin(self):
        '''Creating data with test user'''
        a = create_object()

        # Trying to delete via url pattern as Anonymous user
        self.client.get(reverse('todo:del', args=[a.id]))

        #Check with test user if data still present
        self.client.login(username='test', password='12345')
        response = self.client.get(reverse('todo:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Testing")

        #Trying to check directly via models
        self.assertEqual(TodoDB.objects.get(id=a.id).item_text,"Testing")

    def test_9_add_object_as_non_owner(selfself):
        '''Test to see if non_owner can delete data'''

        pass

    def test_10_delete_object_as_non_owner(self):
        '''Test to see if non_owner can delete data'''
        pass


    def test_11_view_object_as_non_owner(self):
        '''Checking if user1 can view data of user2'''

        # Creating element as test user
        create_object()

        #Loging in as random user
        random_user= User.objects.create_user(username='gary')
        random_user.set_password('12345')
        random_user.save()
        self.client.login(username='gary', password='12345')
        response = self.client.get(reverse('todo:list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context_data['context'], [])

