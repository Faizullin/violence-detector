import json
import os
import random
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files import File
from django.db.models import QuerySet

from apps.accounts.groups import AdminGroup, DeveloperGroup, StaffGroup

User = get_user_model()


def seed(use_allauth):
    # academic_config = AcademicConfig.objects.create(
    #     email_enabled=False
    # )
    if use_allauth: 
        from allauth.account.models import EmailAddress
    groupAdmin = Group.objects.create(
        name=AdminGroup.name,
        id=AdminGroup.id,
    )
    groupDeveloper = Group.objects.create(
        name=DeveloperGroup.name,
        id=DeveloperGroup.id,
    )
    groupStaff = Group.objects.create(
        name=StaffGroup.name,
        id=StaffGroup.id,
    )
    user1 = User.objects.create_user(
        username="admin",
        email="admin@example.com",
        password="admin.password@1234",
        is_staff=True,
        is_superuser=True,
    )
    if use_allauth:
        EmailAddress.objects.create(
            user=user1,
            email=user1.email,
            verified=True,
        )
    user1.groups.set([groupAdmin, groupDeveloper])
    user2 = User.objects.create_user(
        username="user1",
        email="user1@example.com",
        password="user1.password@1234",
        is_staff=True,
    )
    if use_allauth:
        EmailAddress.objects.create(
            user=user2,
            email=user2.email,
            verified=True,
        )
    user2.groups.set([groupDeveloper])
    user3 = User.objects.create_user(
        username="user3",
        email="user3@example.com",
        password="user3.password@1234",
    )
    if use_allauth:
        EmailAddress.objects.create(
            user=user3,
            email=user3.email,
            verified=True,
        )

    prefix_path = 'seeding/data'
    # with open(f'{prefix_path}/tour_periods.json', "r") as f:
    #     data_list = json.load(f)
    #     arr: list[TourPackage] = []
    #     for i in data_list:
    #         instance = TourPeriod.objects.create(
    #             **{key: value for key, value in i.items() if key != 'image'},
    #         )
    #         arr.append(instance)
    # deposit = TourPeriodPaymentDeposit.objects.create(
    #     amount=100,
    # )
    # for i in arr:
    #     i.save()
    #     i.deposits.set([deposit])

    # tour_period_list = TourPeriod.objects.all()
    # with open(f'{prefix_path}/destinations.json', "r") as f:
    #     data_list = json.load(f)
    #     arr: list[TourPeriod] = []
    #     for i in data_list:
    #         image_path = os.path.join(prefix_path, i['image'])
    #         instance = DestinationGuide(
    #             **{key: value for key, value in i.items() if key != 'image'}
    #         )
    #         with open(image_path, 'rb') as img_file:
    #             instance.image.save(os.path.basename(
    #                 image_path), File(img_file), save=False)
    #         arr.append(instance)
    # for i in arr:
    #     i.save()

    # with open(f'{prefix_path}/tours.json', "r") as f:
    #     data_list = json.load(f)
    #     arr: list[TourPackage] = []
    #     for i in data_list:
    #         image_path = os.path.join(prefix_path, i['image'])
    #         instance = TourPackage.objects.language('en').create(
    #             **{key: value for key, value in i.items() if key != 'image'}
    #         )
    #         with open(image_path, 'rb') as img_file:
    #             instance.image.save(os.path.basename(
    #                 image_path), File(img_file), save=False)
    #         arr.append(instance)
    # for i in arr:
    #     i.save()
    #     i.dates.set(tour_period_list)
    # with open(f'{prefix_path}/blogs.json', "r") as f:
    #     data_list = json.load(f)
    #     arr = []
    #     for i in data_list:
    #         image_path = os.path.join(prefix_path, i['image'])
    #         instance = BlogPost(
    #             **{key: value for key, value in i.items() if key != 'image'}
    #         )
    #         with open(image_path, 'rb') as img_file:
    #             instance.image.save(os.path.basename(
    #                 image_path), File(img_file), save=False)
    #         arr.append(instance)
    # for i in arr:
    #     i.save()
    # with open(f'{prefix_path}/reviews.json', "r") as f:
    #     data_list = json.load(f)
    #     arr = []
    #     for i in data_list:
    #         image_path = os.path.join(prefix_path, i['image'])
    #         instance = CustomerReview(
    #             **{key: value for key, value in i.items() if key != 'image'}
    #         )
    #         with open(image_path, 'rb') as img_file:
    #             instance.image.save(os.path.basename(
    #                 image_path), File(img_file), save=False)
    #         arr.append(instance)
    # for i in arr:
    #     i.save()

    # academic_config.email_enabled = True
    # academic_config.save()

    # reviews = CustomerReview.objects.order_by('-updated_at')
    # tours = TourPackage.objects.all()
    # destination_guides = DestinationGuide.objects.all()
    # blogs = BlogPost.objects.order_by('-updated_at')
    # data = {
    #     'reviews_ids': [i.id for i in reviews],
    #     'destination_guides_ids': [i.id for i in destination_guides],
    #     'tours_ids': [i.id for i in tours],
    #     'blogs_ids': [i.id for i in blogs],
    # }
    # HomePreviewModel.objects.create(data=json.dumps(data))

    print("Seed data created successfully.")


if __name__ == "__main__":
    seed()
