from django.shortcuts import render
from rest_framework.views import APIView


# Create your views here.
class CartView(APIView):
    """购物车增删改查"""

    def perform_authentication(self, request):
        """重写此方法 直接pass 可以延后认证 延后到第一次通过 request.user 或request.auth才去做认证"""
        pass

    def post(self, request):
        """新增"""
        print('xxxx')
        pass

    def get(self, request):
        """查询"""
        pass

    def put(self, request):
        """修改"""
        pass

    def delete(self, request):
        """删除"""
        pass