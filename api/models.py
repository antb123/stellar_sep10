from api import db
import uuid
import decimal
import enum
import datetime


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # code = db.Column(db.Text, default="USD", nullable=False)
    # issuer = db.Column(db.Text, nullable=False)
    # significant_decimals = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Text, unique=True,  nullable=False)
    deposit_enabled = db.Column(db.Boolean, default=True)
    deposit_fee_fixed = db.Column(db.Decimal, default=0, blank=True, precision=30, scale=7)
    deposit_fee_percent = db.Column(db.Decimal,
        default=0,
        blank=True,
        precision=30,
        scale=7,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    deposit_min_amount = db.Column(db.Decimal, default=0, blank=True, precision=30, scale=7)
    deposit_max_amount = db.Column(db.Decimal, default=decimal.MAX_EMAX, blank=True, precision=30, scale=7)
    withdrawal_enabled = db.Column(db.Boolean, default=True)
    """``True`` if SEP-6 withdrawal for this asset is supported."""
    withdrawal_fee_fixed = db.Column(db.Decimal, default=0, blank=True, precision=30, scale=7)
    withdrawal_fee_percent = db.Column(db.Decimal,
        default=0,
        blank=True,
        precision=30,
        scale=7,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    withdrawal_min_amount = db.Column(db.Decimal, default=0, blank=True, precision=30, scale=7)
    withdrawal_max_amount = db.Column(db.Decimal, default=decimal.MAX_EMAX, blank=True, precision=30, scale=7)


class KindEnum(enum.Enum):
    deposit = 'deposit'
    withdrawal = 'withdrawal'


class StatusEnum(enum.Enum):
    completed = 'completed'
    pending_external = 'pending_external'
    pending_anchor = 'pending_anchor'
    pending_stellar = 'pending_stellar'
    pending_trust = 'pending_trust'
    pending_user = 'pending_user'
    pending_user_transfer_start = 'pending_user_transfer_start'
    incomplete = 'incomplete'
    no_market = 'no_market'
    too_small = 'too_small'
    too_large = 'too_large'
    error = 'error'


class MemoTypesEnum(enum.Enum):
    text = 'text'
    id = 'id'
    hash = 'hash'


class Transaction(db.Model):

    id = db.Column(db.Integer, primary_key=True, default=uuid.uuid4)
    # Stellar account to watch, and asset that is being transactioned
    # NOTE: these fields should not be publicly exposed
    stellar_account = db.Column(db.Text, validators=[MinLengthValidator(1)])
    asset = db.relationship("Asset", backref='transaction', ondelete="CASCADE")
    kind = db.Column(db.Enum(KindEnum), default=KindEnum.deposit)
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.pending_external)
    status_eta = db.Column(db.Integer, blank=True, default=3600)
    # status_message = db.Column(db.Text, blank=True)
    stellar_transaction_id = db.Column(db.Text, blank=True)
    external_transaction_id = db.Column(db.Text, blank=True)
    amount_in = db.Column(db.Decimal, blank=True, precision=30, scale=7)
    amount_out = db.Column(db.Decimal, blank=True, precision=30, scale=7)
    amount_fee = db.Column(db.Decimal, blank=True, precision=30, scale=7)
    started_at = db.Column(db.DateTime, default=datetime.datetime.now)
    completed_at = db.Column(db.DateTime, )
    from_address = db.Column(db.Text, blank=True)
    to_address = db.Column(db.Text, blank=True)
    external_extra = db.Column(db.Text, blank=True)
    external_extra_text = db.Column(db.Text, blank=True)
    deposit_memo = db.Column(db.Text, blank=True)
    deposit_memo_type = db.Column(db.Enum(MemoTypesEnum), default=MemoTypesEnum.text)
    withdraw_anchor_account = db.Column(db.Text, blank=True)
    withdraw_memo = db.Column(db.Text, blank=True)
    withdraw_memo_type = db.Column(db.Enum(MemoTypesEnum), default=MemoTypesEnum.text)
    # refunded = db.Column(db.Boolean, default=False)
