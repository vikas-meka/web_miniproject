from django.test import TestCase, Client
from home import views
from django.urls import reverse
from .models import course, mark, student_detail, course_key, admin_key, grade, admin_detail, student_password

class CourseModelTests(TestCase):
    """ Test cases related to the course model """

    def setUp(self):
        # Setting up a course instance for testing
        self.course = course.objects.create(
            username='course_user1', password='password123', course1='CS101',
            credits=3, year='2', branch='CSE', name='Data Structures', teacher='Prof. Smith'
        )

    def test_course_creation(self):
        """ Test Case 1.1: Verify course creation """
        self.assertEqual(course.objects.count(), 1)
        self.assertEqual(self.course.course1, 'CS101')
    
    def test_course_primary_key_uniqueness(self):
        """ Test Case 1.2: Ensure unique primary key for course """
        with self.assertRaises(Exception):
            course.objects.create(course1='CS101')  # Duplicate primary key
    
    def test_course_string_representation(self):
        """ Test Case 1.3: Verify __str__ representation """
        self.assertEqual(str(self.course), 'course_user1')

    def test_course_with_null_optional_fields(self):
        """ Test Case 1.4: Create a course with null optional fields """
        course_with_nulls = course.objects.create(
            username='course_user2', course1='CS102', credits=None, year=None, branch=None
        )
        self.assertIsNone(course_with_nulls.credits)


class StudentDetailModelTests(TestCase):
    """ Test cases for student_detail model """

    def setUp(self):
        self.student = student_detail.objects.create(
            roll_no='ST001', name='John Doe', year='3', branch='ECE', password='mypassword'
        )

    def test_student_creation(self):
        """ Test Case 2.1: Verify student creation """
        self.assertEqual(student_detail.objects.count(), 1)
        self.assertEqual(self.student.roll_no, 'ST001')

    def test_duplicate_roll_no(self):
        """ Test Case 2.2: Ensure unique roll_no """
        with self.assertRaises(Exception):
            student_detail.objects.create(roll_no='ST001')  # Duplicate roll number
    
    def test_student_string_representation(self):
        """ Test Case 2.3: Verify __str__ method """
        self.assertEqual(str(self.student), 'ST001')
    


class MarkModelTests(TestCase):
    """ Test cases for mark model """

    def setUp(self):
        self.mark_entry = mark.objects.create(
            roll_no='ST001', course='CS101', ct1=20, ct2=25, end=50, internals=10, total=105, grade=4, score='A'
        )

    def test_mark_entry_creation(self):
        """ Test Case 3.1: Verify mark entry creation """
        self.assertEqual(mark.objects.count(), 1)
        self.assertEqual(self.mark_entry.course, 'CS101')
    
    def test_total_marks(self):
        """ Test Case 3.2: Verify total marks calculation """
        self.assertEqual(self.mark_entry.total, 105)
    
    def test_null_fields_in_mark_entry(self):
        """ Test Case 3.3: Allow null values for optional fields """
        mark_with_nulls = mark.objects.create(roll_no='ST002', course='CS102', total=70, grade=None)
        self.assertIsNone(mark_with_nulls.grade)

    def test_invalid_grade_type(self):
        """ Test Case 3.4: Grade must be an integer """
        with self.assertRaises(Exception):
            mark.objects.create(roll_no='ST003', course='CS103', grade='invalid')


  
class GradeModelTests(TestCase):
    """ Test cases for grade model """

    def setUp(self):
        self.grade_entry = grade.objects.create(roll_no='ST001', cgpa='8.5')

    def test_grade_entry_creation(self):
        """ Test Case 5.1: Verify grade entry creation """
        self.assertEqual(grade.objects.count(), 1)
        self.assertEqual(self.grade_entry.cgpa, '8.5')
    
    def test_grade_string_representation(self):
        """ Test Case 5.3: Verify __str__ representation """
        self.assertEqual(str(self.grade_entry), 'ST001')


class CourseKeyModelTests(TestCase):
    """ Test cases for course_key model """

    def setUp(self):
        self.course_key = course_key.objects.create(key='key1', course='CS101', name='Data Structures')

    def test_course_key_creation(self):
        """ Test Case 6.1: Verify course key creation """
        self.assertEqual(course_key.objects.count(), 1)
        self.assertEqual(self.course_key.course, 'CS101')
    

    def test_update_entered_marks(self):
        """ Test Case 6.3: Update entered_marks """
        self.course_key.entered_marks = '60'
        self.course_key.save()
        self.assertEqual(self.course_key.entered_marks, '60')


class AdminKeyModelTests(TestCase):
    """ Test cases for admin_key model """

    def setUp(self):
        self.admin_key = admin_key.objects.create(key='admin_key1', name='Admin 1')

    def test_admin_key_creation(self):
        """ Test Case 7.1: Verify admin key creation """
        self.assertEqual(admin_key.objects.count(), 1)
        self.assertEqual(self.admin_key.key, 'admin_key1')
    
    def test_admin_key_fields(self):
        """ Test Case 7.2: Check optional fields """
        self.assertIsNone(self.admin_key.entered_courses)


class StudentPasswordModelTests(TestCase):
    """ Test cases for student_password model """

    def setUp(self):
        self.student_password = student_password.objects.create(username='student1', password='pass1')

    def test_student_password_creation(self):
        """ Test Case 8.1: Verify creation of student_password entry """
        self.assertEqual(student_password.objects.count(), 1)
    
    def test_student_password_retrieval(self):
        """ Test Case 8.3: Retrieve password entry """
        entry = student_password.objects.get(username='student1')
        self.assertEqual(entry.password, 'pass1')


class AuthenticationTests(TestCase):
    """ Test cases for admin and student authentication views """

    def setUp(self):
        self.admin = admin_detail.objects.create(username='vikas', password='vikas_meka')
        self.student_password = student_password.objects.create(username='211199', password='211199')
        self.student_detail = student_detail.objects.create(
            roll_no='211199', name='Test User', year='3', branch='CSE', password='211199')

    def test_admin_login(self):
        """ Test Case 4.1: Admin login with correct credentials """
        response = self.client.post(reverse('admin_login'), {'username': 'vikas', 'password': 'vikas_meka'})
        self.assertEqual(response.status_code, 200)
    
    def test_student_login(self):
        """ Test Case 4.2: Student login with correct credentials """
        response = self.client.post(reverse('student'), {'username': '211140', 'password': '211140'})
        self.assertEqual(response.status_code, 302)
    
    def test_invalid_login(self):
        """ Test Case 4.3: Invalid login credentials """
        response = self.client.post(('loginUser'), {'username': 'invalid', 'password': 'pass'})
        self.assertEqual(response.status_code, 404)
    
    def test_logout(self):
        """ Test Case 4.4: Ensure logout functionality """
        self.client.login(username='vikas', password='vikas_meka')
        response = self.client.get(reverse('admin_logout'))
        self.assertEqual(response.status_code, 302)

    def test_login_view_post_invalid(self):
        """Test login functionality with invalid credentials."""        
        response = self.client.post(reverse('admin_login'), {'username': 'vikas', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin_login'))
        follow_response = self.client.get(reverse('admin_login'))
        messages_list = list(follow_response.context['messages'])
        self.assertTrue(any("Incorrect credentials" in str(msg) for msg in messages_list))


# # Scenario 1: Authentication-related Views
# class AuthenticationViewsTestCase(TestCase):
#     def setUp(self):
#         """Set up client and necessary data for authentication views."""
#         self.client = Client()
#         self.sample_admin = admin_detail.objects.create(
#             username="admin",
#             password="adminpass",
#             name="Admin User"
#         )

#     def test_login_view_get(self):
#         """Test that the login page loads successfully with GET request."""
#         response = self.client.get(reverse('login'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'login.html')

    # def test_login_view_post_valid(self):
    #     """Test login functionality with valid credentials."""
    #     response = self.client.post(reverse('login'), {'username': 'admin', 'password': 'adminpass'})
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse('dashboard'))  # Assuming successful login redirects to dashboard

    # def test_login_view_post_invalid(self):
    #     """Test login functionality with invalid credentials."""
    #     response = self.client.post(reverse('login'), {'username': 'admin', 'password': 'wrongpass'})
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTemplateUsed(response, 'login.html')
    #     self.assertContains(response, "Invalid credentials")

#     def test_logout_view(self):
#         """Test that logout redirects to the index page."""
#         response = self.client.get(reverse('logout'))
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse('index'))

#     def test_admin_login(self):
#         """Test admin-specific login functionality."""
#         response = self.client.post(reverse('admin_login'), {'username': 'admin', 'password': 'adminpass'})
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse('admin_dashboard'))


# # Scenario 2: Dashboard-related Views
# class DashboardViewsTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()

#     def test_faculty_dashboard_view(self):
#         """Test faculty dashboard page loads successfully."""
#         response = self.client.get(reverse('faculty_dashboard'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'faculty_dashboard.html')

#     def test_admin_dashboard_view(self):
#         """Test admin dashboard page loads successfully."""
#         response = self.client.get(reverse('admin_dashboard'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'admin_dashboard.html')


# Scenario 3: Student-related Views
class StudentViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.sample_student = student_detail.objects.create(
            roll_no="R123",
            name="Alice",
            year="2",
            branch="CS",
            password="pass123"
        )

    def test_delete_student_view(self):
        """Test deleting a student successfully."""
        response = self.client.post(reverse('delete_student'), {'roll_no': 'R123'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('add_delete_student'))

    def test_add_delete_student_view(self):
        """Test add/delete student page loads successfully."""
        response = self.client.get(reverse('add_delete_student'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adddel_stu.html')


# Scenario 4: Course Management Views
class CourseViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.sample_course = course.objects.create(
            username="teacher1",
            password="password123",
            course1="CS101",
            credits=3,
            year="1",
            branch="CS",
            name="Computer Science",
            teacher="Dr. Smith"
        )

    def test_add_delete_course_view(self):
        """Test add/delete course page loads successfully."""
        response = self.client.get(reverse('add_delete_course'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adddel_cou.html')
    
    def test_delete_course_view(self):
        """Test deleting a course."""
        response = self.client.post(reverse('delete_course'), {'course1': 'CS101'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('add_delete_course'))

    


# # Scenario 5: Miscellaneous Views
# class MiscellaneousViewsTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()

#     def test_index_view(self):
#         """Test that the index page loads successfully."""
#         response = self.client.get(reverse('index'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'index.html')

#     def test_random_function_view(self):
#         """Test that the random function view loads successfully."""
#         response = self.client.get(reverse('random'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'random.html')

#     def test_clear_view(self):
#         """Test the clear view redirects as expected."""
#         response = self.client.get(reverse('clear'))
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse('index'))

#     def test_change_password_view(self):
#         """Test change password page loads."""
#         response = self.client.get(reverse('change_pwd'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'change_pwd.html')

#     def test_mark_list_view(self):
#         """Test mark list page loads successfully."""
#         response = self.client.get(reverse('mark_list'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'mark_list.html')

