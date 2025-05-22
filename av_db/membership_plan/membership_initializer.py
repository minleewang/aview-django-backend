from membership_plan.entity.membership import Membership

def create_default_memberships(sender, **kwargs):
    """
    post_migrate 시 호출되어 Membership 기본 요금제를 자동 등록합니다.
    이미 데이터가 존재하면 아무 작업도 하지 않습니다.
    """
    if Membership.objects.exists():
        print("ℹ️ Membership 기본 데이터가 이미 존재합니다. 초기화 건너뜀.")
        return

    Membership.objects.create(
        id=1,
        name='하루 요금제',
        price=4000,
        duration_days=1,
        plan_type="DAY"
    )

    Membership.objects.create(
        id=2,
        name='일주일 요금제',
        price=20000,
        duration_days=7,
        plan_type="WEEK"
    )

    Membership.objects.create(
        id=3,
        name='한달 요금제',
        price=60000,
        duration_days=30,
        plan_type="MONTH"
    )

    print("✅ 기본 Membership 요금제 3종 등록 완료.")
