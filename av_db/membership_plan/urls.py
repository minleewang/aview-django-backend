from django.urls import path, include
from rest_framework.routers import DefaultRouter

from membership_plan.controller.membership_controller import MembershipController

router = DefaultRouter()
router.register(r'memberships', MembershipController, basename='memberships')

urlpatterns = [
    path('', include(router.urls)),

    # 구독 생성
    path('create',
         MembershipController.as_view({'post': 'create_membership'}),
         name='구독 생성'),

    # 구독 조회
    path('status',
         MembershipController.as_view({'get': 'get_membership'}),
         name='구독 상태 조회'),

    # 구독 연장
    path('extend',
         MembershipController.as_view({'post': 'extend_membership'}),
         name='구독 연장'),

    # 만료 예정자 조회
    path('expiring',
         MembershipController.as_view({'get': 'get_expiring_memberships'}),
         name='만료 예정자'),

    # 자동 갱신 실행
    path('auto-renew',
         MembershipController.as_view({'post': 'auto_renew_memberships'}),
         name='자동 갱신 실행'),

    # 만료 구독 비활성화
    path('deactivate',
         MembershipController.as_view({'post': 'deactivate_expired_memberships'}),
         name='만료 비활성화'),
]