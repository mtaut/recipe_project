from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Recipe
from .forms import RecipeSearchForm


# Create your tests here.

class RecipeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # set up recipe object for tests in the Recipe class
        cls.user = User.objects.create_user(username='user1', password='word345')
        cls.recipe = Recipe.objects.create(        
            name='Recipe One',
            ingredients='test ingredient1, test ingredient2, test ingredient3, test ingredient4',
            cooking_time=11,
            description='Recipe one test description.'
        )

    def setUp(self):
        self.client.login(username='user1', password='word345')

    def test_recipe_name(self):
        # get recipe object to test
        recipe = Recipe.objects.first()
        #get metadata for 'name' field and use it to query its data
        field_label = recipe._meta.get_field('name').verbose_name
        # compare value to the expected result
        self.assertEqual(field_label, 'name')

    def test_recipe_name_length(self):
        recipe = Recipe.objects.first()
        # get metadata for 'name' and use it to query its max_length
        max_length = recipe._meta.get_field('name').max_length
        # compare value to expected result, maximum of 120
        self.assertEqual(max_length, 120)

    def test_recipe_cooking_time_value(self):
        recipe = Recipe.objects.first()
        # test value of cooking_time
        self.assertEqual(recipe.cooking_time, 11)

    def test_recipe_description_label(self):
        recipe = Recipe.objects.first()
        # test verbose name of description field
        field_label = recipe._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_calculate_difficulty(self):
        self.assertEqual(self.recipe.calculate_difficulty(), "Hard")


class RecipeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user2', password='word123')
        cls.recipe = Recipe.objects.create(
            name="Test Recipe2",
            ingredients="test ingredient3, test ingredient4, eggs, sugar, test ingredient5",
            cooking_time=15,
            description="simple test recipe."
        )

    def setUp(self):
        self.client.login(username='user2', password='word123')

    # test list view of recipes
    def test_recipe_list_view(self):
        response = self.client.get(reverse('recipes:recipes_list'))
        
        self.assertContains(response, "Test Recipe2")
        self.assertTemplateUsed(response, 'recipes/recipes_list.html')

    # test individual recipe details
    def test_recipe_detail_view(self):
        response = self.client.get(reverse('recipes:detail', args=[self.recipe.pk]))
        
        self.assertContains(response, "Test Recipe2")
        self.assertTemplateUsed(response, 'recipes/recipes_detail.html')

class RecipeSearchFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user3', password='password11')
        cls.recipe = Recipe.objects.create(
            name='Test Recipe3',
            ingredients='test ingredient5, test ingredient6, test ingredient7, test ingredient8',
            cooking_time=7,
            description='nice recipe for a test'
        )

    def setUp(self):
        self.client.login(username='user3', password='password11')

    # test ingredient search
    def test_search_ingredient(self):
        url = reverse('recipes:recipes_list')
        response = self.client.get(url, {'ingredient': 'test ingredient5'})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('search_results', response.context)

        search_results = response.context['search_results']
        self.assertGreater(len(search_results), 0)
        self.assertIn(self.recipe, search_results)

    # test chart with ingredient
    def test_valid_form(self):
        form_data = {'ingredient': 'tomato', 'chart_type': '#1'}
        form = RecipeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    # test chart without ingredient
    def test_invalid_form_without_ingredient(self):
        form_data = {'chart_type': '#1'}
        form = RecipeSearchForm(data=form_data)
        self.assertFalse(form.is_valid())

    # test chart generation
    def test_chart_generation(self):
        url = reverse('recipes:recipes_list')

        form_data = {
            'ingredient': 'chicken',
            'chart_type': '#1',
        }
        response = self.client.get(url, form_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('chart', response.context)    

class RecipeFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user4', password='password1123')
        
    def setUp(self):
        self.client.login(username='user4', password='password1123')

    # test user-created recipe
    def test_create_recipe(self):
        url = reverse('recipes:create_recipe')

        form_data = {
            'name': 'Test Recipe3',
            'ingredients': 'test ingredient, test ingredient8',
            'cooking_time': 3,
            'description': 'recipe for a test',
            'pic': ''
        }
        response = self.client.post(url, form_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Recipe.objects.filter(name='Test Recipe3').exists())

        