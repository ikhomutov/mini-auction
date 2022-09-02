from rest_framework.exceptions import APIException


class LotExists(APIException):
    status_code = 400
    default_detail = 'Lot for pet already exists.'
    default_code = 'lot_exists'


class UserNotOwnPet(APIException):
    status_code = 400
    default_detail = 'User is not owner of the pet'
    default_code = 'user_not_own_pet'


class UserIsNotAuthorForLot(APIException):
    status_code = 400
    default_detail = 'User is not author for the lot'
    default_code = 'user_is_not_author_for_lot'


class LotAlreadyClosed(APIException):
    status_code = 400
    default_detail = 'Lot is already closed'
    default_code = 'lot_already_closed'


class CannotBidInOwnLot(APIException):
    status_code = 400
    default_detail = 'User cannot place bid in his lot'
    default_code = 'cannot_bid_in_own_lot'


class OnlyOneBidAllowed(APIException):
    status_code = 400
    default_detail = 'User can place only one bid in a lot'
    default_code = 'only_one_bid_allowed'


class UserIsNotAuthorForBid(APIException):
    status_code = 400
    default_detail = 'User is not an author for bid'
    default_code = 'user_is_not_author_for_bid'


class CanOnlyAcceptBidForOwnLot(APIException):
    status_code = 400
    default_detail = 'User can only accept bid for his lot'
    default_code = 'can_only_accept_bid_for_own_lot'


class InsufficientBalance(APIException):
    status_code = 400
    default_detail = 'Not enough money to place bid'
    default_code = 'insufficient_balance'
