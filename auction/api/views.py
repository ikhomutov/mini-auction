from django.db.transaction import atomic
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from auction.core import models
from auction.core.constants import LotStatuses
from . import serializers, exceptions


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserCreateSerializer


class PetViewSet(GenericViewSet):
    queryset = models.Pet.objects.all()
    serializer_class = serializers.PetSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(
            owner=request.user.useraccount
        )
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user.useraccount)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LotViewSet(GenericViewSet):
    queryset = models.Lot.objects.all()

    def list(self, request):
        queryset = self.get_queryset().select_related('pet').filter(status=LotStatuses.OPEN)
        serializer = serializers.LotDisplaySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = serializers.LotCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pet = serializer.validated_data['pet']

        # check that user owns pet
        if not pet.owner == request.user.useraccount:
            raise exceptions.UserNotOwnPet()

        # check that there is no existed lot for this pet
        lot_exists = models.Lot.objects.filter(
            author=request.user.useraccount,
            pet=pet,
            status=LotStatuses.OPEN,
        ).exists()
        if lot_exists:
            raise exceptions.LotExists()

        lot = serializer.save(
            author=self.request.user.useraccount,
            status=LotStatuses.OPEN
        )
        return Response(
            serializers.LotDisplaySerializer(lot).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['get'])
    def bids(self, request, pk=None):
        lot = self.get_object()
        bids = lot.bids.filter(lot__status=LotStatuses.OPEN)
        return Response(serializers.BidShortDisplaySerializer(bids, many=True).data)

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        lot = self.get_object()
        if not lot.author == request.user.useraccount:
            raise exceptions.UserIsNotAuthorForLot()

        if lot.is_closed:
            raise exceptions.LotAlreadyClosed()

        lot.close()
        return Response()


class BidViewSet(GenericViewSet):
    queryset = models.Bid.objects.select_related('lot__pet')

    def list(self, request):
        queryset = self.get_queryset().filter(
            lot__status=LotStatuses.OPEN
        )
        serializer = serializers.BidLongDisplaySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = serializers.BidCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lot = serializer.validated_data['lot']

        if lot.is_closed:
            raise exceptions.LotAlreadyClosed()

        if lot.author == request.user.useraccount:
            raise exceptions.CannotBidInOwnLot()

        user_already_has_bid = lot.bids.filter(
            author=request.user.useraccount
        ).exists()
        if user_already_has_bid:
            raise exceptions.OnlyOneBidAllowed()

        if serializer.validated_data['price'] > request.user.useraccount.available_balance:
            raise exceptions.InsufficientBalance()

        bid = serializer.save(
            author=self.request.user.useraccount,
        )
        return Response(
            serializers.BidLongDisplaySerializer(bid).data,
            status=status.HTTP_201_CREATED
        )

    def destroy(self, request, *args, **kwargs):
        bid = self.get_object()

        if bid.author != request.user.useraccount:
            raise exceptions.UserIsNotAuthorForBid()

        if bid.lot.is_closed:
            raise exceptions.LotAlreadyClosed()

        bid.delete()
        return Response()

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        bid = self.get_object()
        if bid.lot.author != request.user.useraccount:
            raise exceptions.CanOnlyAcceptBidForOwnLot()

        if bid.lot.is_closed:
            raise exceptions.LotAlreadyClosed()

        with atomic():
            bid.lot.pet.set_owner(bid.author)
            bid.lot.author.increase_balance(bid.price)
            bid.author.decrease_balance(bid.price)
            bid.lot.close()
        return Response()