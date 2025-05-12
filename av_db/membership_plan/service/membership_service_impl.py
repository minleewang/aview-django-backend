from abc import ABC, abstractmethod
from datetime import timedelta, datetime
from django.utils import timezone

from membership_plan.entity.user_membership import UserMembership
from membership_plan.repository.user_membership_repository_impl import UserMembershipRepositoryImpl
from membership_plan.repository.membership_repository_impl import MembershipRepositoryImpl
from account.repository.account_repository_impl import AccountRepositoryImpl

# 구독 관련 비즈니스 로직 구현체
class MembershipServiceImpl:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__userMembershipRepository = UserMembershipRepositoryImpl.getInstance()
            cls.__instance.__membershipRepository = MembershipRepositoryImpl.getInstance()
            cls.__instance.__accountRepository = AccountRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createMembership(self, userId, membershipId):
        # 유저와 멤버십 정보 가져오기
        user = self.__accountRepository.findById(userId)
        membership = self.__membershipRepository.findById(membershipId)

        if not user:
            raise Exception(f"Account id {userId} 존재하지 않음.")
        if not membership:
            raise Exception(f"Membership id {membershipId} 존재하지 않음.")

        start_date = timezone.now()
        end_date = start_date + timedelta(days=membership.duration_days)

        userMembership = UserMembership(
            user=user,
            plan=membership,
            start_date=start_date,
            end_date=end_date,
            is_active=True,
            is_renew_scheduled=False
        )

        return self.__userMembershipRepository.save(userMembership)

    def getUserMembership(self, userId):
        return self.__userMembershipRepository.findByUserId(userId)

    def extendMembership(self, userId, days):
        userMembership = self.__userMembershipRepository.findByUserId(userId)
        if not userMembership:
            raise Exception(f"UserMembership not found for user {userId}")

        userMembership.end_date += timedelta(days=days)
        return self.__userMembershipRepository.save(userMembership)

    def getExpiringMemberships(self, withinDays):
        return self.__userMembershipRepository.findExpiringWithinDays(withinDays)

    # 자동 갱신 대상인 유저의 구독을 현재 시점 기준으로 새 기간으로 연장
    def renewScheduledMemberships(self):
        now = timezone.now()
        memberships = self.__userMembershipRepository.findExpiringWithinDays(0)

        renewed_count = 0
        for m in memberships:
            if m.is_active and m.is_renew_scheduled:
                duration = m.plan.duration_days
                m.start_date = now
                m.end_date = now + timedelta(days=duration)
                self.__userMembershipRepository.save(m)
                renewed_count += 1

        return renewed_count

    # 이미 만료된 구독을 찾아 is_active=False로 비활성화
    def deactivateExpiredMemberships(self):
        now = timezone.now()
        memberships = self.__userMembershipRepository.findExpiringWithinDays(-1)

        deactivated_count = 0
        for m in memberships:
            if m.is_active and m.end_date < now:
                m.is_active = False
                self.__userMembershipRepository.save(m)
                deactivated_count += 1

        return deactivated_count