import uuid
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy
from food_app.models import Food, Category

# add_food関数用のテストクラス
class TestAddFood(TestCase):
    
    # 食材の追加が成功することを検証する
    def test_add_food_success(self):

        category = Category.objects.get(category="調味料")
        print(category)

        # Postパラメータ
        params = {
            "name": "テスト用",
            "category": category,
            "expiry_date": "2022-11-13",
            "expiration_date": "",
            "memo": "テスト用メモです",
        }

        # 食材追加処理(Post)を実行
        response = self.client.post(reverse_lazy('food_app:add_food'), params)

        # 食材追加後にホームへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy("food_app:index"))

        # 食材がデータベースに登録されたか検証
        self.assertExqual(Food.objects.filter(name="テスト用").count(), 1)

    # 食材の追加が失敗すること検証する
    def test_add_food_failure(self):

        # 食材追加処理(Post)を実効
        response = self.client.post(reverse_lazy("food_app:add_food"))

        # 必須フォームフィールが未入力によるエラーになることを検証
        self.assertFormError(response, "form", "name", "このフィールドは必須です。")

# update_food関数用のテストクラス
class TestUpdateFood(TestCase):

    # 食材更新処理が成功することを検証する
    def test_update_food_success(self):

        # テスト用食材データの作成
        food = Food.objects.create(name="更新テスト用編集前", category=Category.objects.get(category="調味料"))

        # Postパラメータ
        params = {"title": "更新テスト用編集後"}

        # 食材更新処理(Post)を実行
        response = self.client.post(reverse_lazy("food_app:update_food", kwargs={"uuid": food.uuid}), params)

        # 食材詳細ページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy("food_app:food_detail", kwargs={"uuid": food.uuid}))

        # 食材データが編集されたかを検証
        self.assertEqual(Diary.objects.get(uuid=food.uuid).name, "更新テスト用編集後")

    # 食材更新処理が失敗することを検証する
    def test_update_food_failure(self):

        # 食材更新処理(Post)を実行
        response = self.client.post(reverse_lazy("food_app:update_food"), kwargs={"uuid": 999})

        # 存在しない食材データを編集しようとしてエラーになることを検証
        self.assertEqual(response.status_code, 404)

# delete_food関数用のテストクラス
class TestDeleteFood(TestCase):

    # 食材データ削除処理が成功することを検証する
    def test_delete_food_success(self):

        # テスト用食材データの作成
        food = Food.objects.create(name="削除テスト用", category=Category.objects.get(category="調味料"),)

        # 食材データ削除処理(Post)を実行
        response = self.client.post(reverse_lazy("food_app:delete_food", kwargs={"uuid": food.uuid}))

        # ホームページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy("food_app:index"))

        # 食材データが削除されたかを検証
        self.assertEqual(Diary.objects.filter(uuid=food.uuid).count(), 0)

    # 食材データ削除処理が失敗することを検証する
    def test_delete_food_failure(self):
        
        # 食材データ削除処理(Post)を実行
        response = self.client.post(reverse_lazy('food_app:delete_food', kwargs={"uuid": uuid.uuid4}))

        # 存在しない食材データを削除しようとしてえらいになることを検証
        self.assertEqual(response.status_code, 404)









