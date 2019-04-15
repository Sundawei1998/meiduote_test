from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from alipay import AliPay
from django.conf import settings
import os

from orders.models import OrderInfo

# Create your views here.

class PaymentView(APIView):
    """生成支付链接"""

    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):

        # 获取当前的请求用户对象
        user = request.user

        # 校验订单的有效性
        try:
            order_model = OrderInfo.objects.get(order_id=order_id, user=user, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'])
        except OrderInfo.DoesNotExist:
            return Response({'message': '订单有误'}, status=status.HTTP_400_BAD_REQUEST)

        # 支付宝
        ALIPAY_APPID = '2016091900551154'
        ALIPAY_DEBUG = True
        ALIPAY_URL = 'https://openapi.alipaydev.com/gateway.do'
        # 创建alipay  SDK中提供的支付对象
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keys/app_private_key.pem'),  # 指定应用自己的私钥文件绝对路径
            alipay_public_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keys/alipay_public_key.pem'), # 指定支付宝公钥文件的绝对路径
            sign_type="RSA2",  # RSA 或者 RSA2  加密方式推荐使用RSA2
            debug = settings.ALIPAY_DEBUG  # 默认False
        )

        # 调用SDK的方法得到支付链接后面的查询参数
        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,  # 马上要支付的订单编号
            total_amount=str(order_model.total_amount),  # 支付总金额, 它不认识Decimal 所以这里一定要转换类型
            subject='美多商城%s' % order_id,  # 标题
            return_url="http://www.meiduo.site:8080/pay_success.html",  # 支付成功后的回调url
        )

        # 拼接好支付链接
        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do?order_id=xxx&xxx=abc
        # 沙箱环境支付链接 :  https://openapi.alipaydev.com/gateway.do? + order_string
        # 真实环境支付链接 :  https://openapi.alipay.com/gateway.do? + order_string
        alipay_url = settings.ALIPAY_URL + '?' + order_string


        # 响应
        return Response({'alipay_url': alipay_url})
