from decimal import Decimal

import pytest
from faker import Faker

from auction.core import models
from auction.core.constants import LotStatuses
from tests import factories

pytestmark = pytest.mark.django_db


def test_user_must_have_useraccount(api_client):
    user = factories.UserFactory.create()
    api_client.force_authenticate(user=user)
    response = api_client.get('/api/pets/')
    assert response.status_code == 403


def test_users_see_only_their_pets(api_client, user_account):
    factories.PetFactory.create_batch(5, owner=user_account)
    factories.PetFactory.create_batch(5)
    api_client.force_authenticate(user=user_account.user)
    response = api_client.get('/api/pets/')
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_user_can_see_open_lots(api_client, user_account):
    factories.LotFactory.create_batch(5, status=LotStatuses.OPEN)
    factories.LotFactory.create_batch(5, status=LotStatuses.CLOSED)
    api_client.force_authenticate(user=user_account.user)
    response = api_client.get('/api/lots/')
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_user_can_close_his_lot(api_client, user_account):
    lot = factories.LotFactory.create(author=user_account, status=LotStatuses.OPEN)
    api_client.force_authenticate(user=user_account.user)
    response = api_client.post(f'/api/lots/{lot.id}/close/', {})
    assert response.status_code == 200
    lot.refresh_from_db()
    assert lot.status == LotStatuses.CLOSED


def test_user_cannot_close_others_lot(api_client, user_account):
    factories.LotFactory.create(author=user_account, status=LotStatuses.OPEN)
    random_lot = factories.LotFactory.create(status=LotStatuses.OPEN)
    api_client.force_authenticate(user=user_account.user)
    response = api_client.post(f'/api/lots/{random_lot.id}/close/', {})
    assert response.status_code == 400


def test_user_can_see_bids_for_lot(api_client, user_account):
    lot = factories.LotFactory.create(author=user_account, status=LotStatuses.OPEN)
    factories.BidFactory.create_batch(5, lot=lot)
    api_client.force_authenticate(user=user_account.user)
    response = api_client.get(f'/api/lots/{lot.id}/bids/')
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_user_can_place_bids(api_client, user_account):
    lot = factories.LotFactory.create(status=LotStatuses.OPEN)
    api_client.force_authenticate(user=user_account.user)
    bid_data = {
        'lot': lot.id,
        'price': Decimal('0.01')
    }
    bids_count = models.Bid.objects.count()
    assert bids_count == 0
    response = api_client.post(f'/api/bids/', bid_data)
    assert response.status_code == 201
    bids_count = models.Bid.objects.count()
    assert bids_count == 1


def test_user_cannot_place_bid_in_closed_lot(api_client, user_account):
    lot = factories.LotFactory.create(status=LotStatuses.CLOSED)
    api_client.force_authenticate(user=user_account.user)
    bid_data = {
        'lot': lot.id,
        'price': Decimal('0.01')
    }
    response = api_client.post(f'/api/bids/', bid_data)
    assert response.status_code == 400
    bids_count = models.Bid.objects.count()
    assert bids_count == 0


def test_user_cannot_place_bid_in_his_lot(api_client, user_account):
    lot = factories.LotFactory.create(
        status=LotStatuses.OPEN,
        author=user_account
    )
    api_client.force_authenticate(user=user_account.user)
    bid_data = {
        'lot': lot.id,
        'price': Decimal('0.01')
    }
    response = api_client.post(f'/api/bids/', bid_data)
    assert response.status_code == 400
    bids_count = models.Bid.objects.count()
    assert bids_count == 0


def test_user_can_delete_his_bids(api_client, user_account):
    lot = factories.LotFactory.create(status=LotStatuses.OPEN)
    bid = factories.BidFactory.create(
        lot=lot, price=Decimal('0.01'), author=user_account
    )
    api_client.force_authenticate(user=user_account.user)
    response = api_client.delete(f'/api/bids/{bid.id}/')
    assert response.status_code == 200
    bids_count = models.Bid.objects.count()
    assert bids_count == 0


def test_user_cannot_delete_not_his_bids(api_client, user_account):
    lot = factories.LotFactory.create(status=LotStatuses.OPEN)
    bid = factories.BidFactory.create(lot=lot)
    api_client.force_authenticate(user=user_account.user)
    response = api_client.delete(f'/api/bids/{bid.id}/')
    assert response.status_code == 400
    bids_count = models.Bid.objects.count()
    assert bids_count == 1


def test_user_cannot_delete_bid_for_closed_lot(api_client, user_account):
    lot = factories.LotFactory.create(status=LotStatuses.CLOSED)
    bid = factories.BidFactory.create(
        lot=lot, price=Decimal('0.01'), author=user_account
    )
    api_client.force_authenticate(user=user_account.user)
    response = api_client.delete(f'/api/bids/{bid.id}/')
    assert response.status_code == 400
    bids_count = models.Bid.objects.count()
    assert bids_count == 1


def test_insufficient_balance(api_client):
    user_account = factories.UserAccountFactory.create(balance=Decimal('100.00'))
    lot_1 = factories.LotFactory.create(status=LotStatuses.OPEN)
    lot_2 = factories.LotFactory.create(status=LotStatuses.OPEN)
    lot_3 = factories.LotFactory.create(status=LotStatuses.OPEN)
    factories.BidFactory.create(lot=lot_1, author=user_account, price=Decimal('50.00'))
    factories.BidFactory.create(lot=lot_2, author=user_account, price=Decimal('30.00'))
    api_client.force_authenticate(user=user_account.user)
    request_data = {
        'lot': lot_3.id,
        'price': '30.00'
    }
    response = api_client.post('/api/bids/', request_data)
    assert response.status_code == 400


def test_user_can_accept_bid(faker, api_client, user_account):
    pet = factories.PetFactory(
        owner=user_account
    )
    test_bid_price = faker.pydecimal(
        left_digits=2, right_digits=2, positive=True
    )
    test_bid_user_balance = faker.pydecimal(
        left_digits=2, right_digits=2, positive=True, min_value=test_bid_price
    )
    bid_user_account = factories.UserAccountFactory(
        balance=test_bid_user_balance
    )
    lot = factories.LotFactory.create(
        status=LotStatuses.OPEN,
        author=user_account,
        pet=pet
    )
    bid = factories.BidFactory.create(
        lot=lot,
        price=test_bid_price,
        author=bid_user_account
    )
    prev_lot_user_balance = user_account.balance

    api_client.force_authenticate(user=user_account.user)
    response = api_client.post(f'/api/bids/{bid.id}/accept/')
    assert response.status_code == 200
    user_account.refresh_from_db()
    assert user_account.balance == prev_lot_user_balance + test_bid_price
    bid_user_account.refresh_from_db()
    assert bid_user_account.balance == test_bid_user_balance - test_bid_price
    lot.refresh_from_db()
    assert lot.status == LotStatuses.CLOSED
    pet.refresh_from_db()
    assert pet.owner == bid_user_account
