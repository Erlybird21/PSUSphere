from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from studentorg.models import College, Program, Student


class APITestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='api-test-user'
        )
        cls.token = Token.objects.create(user=cls.user)
        cls.college = College.objects.create(
            college_name='Test College'
        )
        cls.program = Program.objects.create(
            prog_name='Test Program',
            college=cls.college,
        )
        cls.student = Student.objects.create(
            student_id='TEST-001',
            lastname='Test',
            firstname='Student',
            middlename='',
            program=cls.program,
        )

    def setUp(self):
        self.client = APIClient()

    def authenticate(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )

    def test_unauthenticated_requests_are_rejected(self):
        for url in (
            '/api/colleges/',
            f'/api/colleges/{self.college.pk}/',
            '/api/programs/',
            f'/api/programs/{self.program.pk}/',
            '/api/students/',
            f'/api/students/{self.student.pk}/',
        ):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code,
                    status.HTTP_401_UNAUTHORIZED,
                )

    def test_invalid_token_is_rejected(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token invalid-token'
        )
        response = self.client.get('/api/colleges/')
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_college_crud(self):
        self.authenticate()

        create = self.client.post(
            '/api/colleges/',
            {'college_name': 'API College'},
            format='json',
        )
        self.assertEqual(
            create.status_code,
            status.HTTP_201_CREATED,
        )
        college_id = create.data['id']

        detail_url = f'/api/colleges/{college_id}/'

        update = self.client.put(
            detail_url,
            {'college_name': 'API College Updated'},
            format='json',
        )
        self.assertEqual(
            update.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            update.data['college_name'],
            'API College Updated',
        )

        partial = self.client.patch(
            detail_url,
            {'college_name': 'API College Patched'},
            format='json',
        )
        self.assertEqual(
            partial.status_code,
            status.HTTP_200_OK,
        )

        delete = self.client.delete(detail_url)
        self.assertEqual(
            delete.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            College.objects.filter(pk=college_id).exists()
        )

    def test_program_crud_and_nested_students(self):
        self.authenticate()

        create = self.client.post(
            '/api/programs/',
            {
                'prog_name': 'API Program',
                'college': self.college.pk,
            },
            format='json',
        )
        self.assertEqual(
            create.status_code,
            status.HTTP_201_CREATED,
        )
        program_id = create.data['id']

        detail_url = f'/api/programs/{program_id}/'

        detail = self.client.get(detail_url)
        self.assertEqual(
            detail.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(detail.data['students'], [])

        update = self.client.put(
            detail_url,
            {
                'prog_name': 'API Program Updated',
                'college': self.college.pk,
            },
            format='json',
        )
        self.assertEqual(
            update.status_code,
            status.HTTP_200_OK,
        )

        delete = self.client.delete(detail_url)
        self.assertEqual(
            delete.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Program.objects.filter(pk=program_id).exists()
        )

        nested = self.client.get(
            f'/api/programs/{self.program.pk}/'
        )
        self.assertEqual(
            nested.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(nested.data['students']), 1)
        self.assertEqual(
            nested.data['students'][0]['id'],
            self.student.pk,
        )

    def test_student_crud_and_program_name(self):
        self.authenticate()

        create = self.client.post(
            '/api/students/',
            {
                'student_id': 'TEST-002',
                'lastname': 'API',
                'firstname': 'Student',
                'middlename': '',
                'program': self.program.pk,
            },
            format='json',
        )
        self.assertEqual(
            create.status_code,
            status.HTTP_201_CREATED,
        )
        student_id = create.data['id']
        self.assertEqual(
            create.data['program_name'],
            'Test Program',
        )

        detail_url = f'/api/students/{student_id}/'

        detail = self.client.get(detail_url)
        self.assertEqual(
            detail.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            detail.data['program'],
            self.program.pk,
        )
        self.assertEqual(
            detail.data['program_name'],
            'Test Program',
        )

        update = self.client.put(
            detail_url,
            {
                'student_id': 'TEST-002',
                'lastname': 'API Updated',
                'firstname': 'Student',
                'middlename': '',
                'program': self.program.pk,
            },
            format='json',
        )
        self.assertEqual(
            update.status_code,
            status.HTTP_200_OK,
        )

        partial = self.client.patch(
            detail_url,
            {'lastname': 'API Patched'},
            format='json',
        )
        self.assertEqual(
            partial.status_code,
            status.HTTP_200_OK,
        )

        delete = self.client.delete(detail_url)
        self.assertEqual(
            delete.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Student.objects.filter(pk=student_id).exists()
        )

    def test_invalid_foreign_key_and_missing_fields_are_rejected(self):
        self.authenticate()

        invalid_fk = self.client.post(
            '/api/students/',
            {
                'student_id': 'TEST-003',
                'lastname': 'Bad',
                'firstname': 'Program',
                'program': 999999,
            },
            format='json',
        )
        self.assertEqual(
            invalid_fk.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn('program', invalid_fk.data)

        missing = self.client.post(
            '/api/students/',
            {
                'student_id': 'TEST-004',
                'firstname': 'Missing',
                'program': self.program.pk,
            },
            format='json',
        )
        self.assertEqual(
            missing.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn('lastname', missing.data)

    def test_missing_record_returns_404(self):
        self.authenticate()
        response = self.client.get('/api/colleges/999999/')
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
