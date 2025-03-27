from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import datetime, timedelta
from .models import Todo, Tag

class TagTests(APITestCase):
    def setUp(self):
        # 創建測試用的標籤
        self.tag1 = Tag.objects.create(name="工作", color="#FF0000")
        self.tag2 = Tag.objects.create(name="個人", color="#00FF00")

    def test_create_tag(self):
        """測試創建標籤"""
        url = '/api/todos/tags/'
        data = {'name': '學習', 'color': '#0000FF'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 3)
        self.assertEqual(Tag.objects.get(name='學習').color, '#0000FF')

    def test_list_tags(self):
        """測試獲取標籤列表"""
        url = '/api/todos/tags/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class TodoTests(APITestCase):
    def setUp(self):
        # 創建測試用的標籤
        self.tag1 = Tag.objects.create(name="工作", color="#FF0000")
        self.tag2 = Tag.objects.create(name="個人", color="#00FF00")
        
        # 創建測試用的待辦事項
        self.todo1 = Todo.objects.create(
            title="測試任務1",
            description="這是第一個測試任務",
            priority=2,
            status='pending',
            due_date=timezone.now() + timedelta(days=1)
        )
        self.todo1.tags.add(self.tag1)

    def test_create_todo(self):
        """測試創建待辦事項"""
        url = '/api/todos/'
        data = {
            'title': '新測試任務',
            'description': '這是一個新的測試任務',
            'priority': 3,
            'status': 'pending',
            'due_date': (timezone.now() + timedelta(days=2)).isoformat(),
            'tag_ids': [self.tag1.id, self.tag2.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 2)
        self.assertEqual(response.data['title'], '新測試任務')
        self.assertEqual(len(response.data['tags']), 2)

    def test_list_todos(self):
        """測試獲取待辦事項列表"""
        url = '/api/todos/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_todos(self):
        """測試過濾待辦事項"""
        # 創建另一個待辦事項用於測試
        Todo.objects.create(
            title="高優先級任務",
            priority=4,
            status='pending'
        )

        # 測試優先級過濾
        response = self.client.get('/api/todos/', {'priority': 4})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '高優先級任務')

        # 測試狀態過濾
        response = self.client.get('/api/todos/', {'status': 'pending'})
        self.assertEqual(len(response.data), 2)

        # 測試標籤過濾
        response = self.client.get('/api/todos/', {'tag': '工作'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '測試任務1')

    def test_search_todos(self):
        """測試搜索待辦事項"""
        response = self.client.get('/api/todos/', {'search': '測試任務'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '測試任務1')

    def test_toggle_status(self):
        """測試切換待辦事項狀態"""
        url = f'/api/todos/{self.todo1.id}/toggle_status/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')

        # 再次切換回pending
        response = self.client.post(url)
        self.assertEqual(response.data['status'], 'pending')

    def test_overdue_todos(self):
        """測試過期待辦事項"""
        # 創建一個過期的待辦事項
        Todo.objects.create(
            title="過期任務",
            due_date=timezone.now() - timedelta(days=1),
            status='pending'
        )

        response = self.client.get('/api/todos/overdue/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '過期任務')

    def test_today_todos(self):
        """測試今日待辦事項"""
        # 創建一個今天到期的待辦事項
        Todo.objects.create(
            title="今日任務",
            due_date=timezone.now(),
            status='pending'
        )

        response = self.client.get('/api/todos/today/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_update_todo(self):
        """測試更新待辦事項"""
        url = f'/api/todos/{self.todo1.id}/'
        data = {
            'title': '更新的標題',
            'description': '更新的描述',
            'priority': 3,
            'tag_ids': [self.tag2.id]
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], '更新的標題')
        self.assertEqual(response.data['priority'], 3)
        self.assertEqual(len(response.data['tags']), 1)

    def test_delete_todo(self):
        """測試刪除待辦事項"""
        url = f'/api/todos/{self.todo1.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0) 