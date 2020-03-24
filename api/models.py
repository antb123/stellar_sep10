from flask_sqlalchemy import Model
from api import db, TimeStampedModel
import uuid
import decimal
import enum


class TimeStampedModel(Model):
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)


class Asset(TimeStampedModel, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text, default="USD", nullable=False)
    issuer = db.Column(db.Text, nullable=False)
    significant_decimals = db.Column(db.Integer, default=2, nullable=False)
    transactions = db.relationship("Transaction", backref='asset', cascade="all, delete", lazy='dynamic')
    deposit_enabled = db.Column(db.Boolean, default=True, nullable=False)
    deposit_fee_fixed = db.Column(db.Decimal, default=0, nullable=False, precision=30, scale=7)
    deposit_fee_percent = db.Column(db.Decimal,
        default=0,
        nullable=False,
        precision=30,
        scale=7,
    )
    deposit_min_amount = db.Column(db.Decimal, default=0, nullable=False, precision=30, scale=7)
    deposit_max_amount = db.Column(db.Decimal, default=decimal.MAX_EMAX, nullable=False, precision=30, scale=7)
    withdrawal_enabled = db.Column(db.Boolean, default=True, nullable=False)
    """``True`` if SEP-6 withdrawal for this asset is supported."""
    withdrawal_fee_fixed = db.Column(db.Decimal, default=0, nullable=False, precision=30, scale=7)
    withdrawal_fee_percent = db.Column(db.Decimal,
        default=0,
        nullable=False,
        precision=30,
        scale=7,
    )
    withdrawal_min_amount = db.Column(db.Decimal, default=0, nullable=False, precision=30, scale=7)
    withdrawal_max_amount = db.Column(db.Decimal, default=decimal.MAX_EMAX, nullable=False, precision=30, scale=7)

    def __str__(self):
        return f"{self.code} - issuer({self.issuer})"


class KindEnum(enum.Enum):
    deposit = 'deposit'
    withdrawal = 'withdrawal'


# interalization
class StatusEnum(enum.Enum):
    completed = 'completed'
    pending_external = 'waiting on an external entity'
    pending_anchor = 'Processing'
    pending_stellar = 'stellar is executing the transaction'
    pending_trust = 'waiting for a trustline to be established'
    pending_user = 'waiting on user action'
    pending_user_transfer_start = 'waiting on the user to transfer funds'
    incomplete = 'incomplete'
    no_market = 'no market for the asset'
    too_small = 'the transaction amount is too small'
    too_large = 'the transaction amount is too big'
    error = 'error'


class MemoTypesEnum(enum.Enum):
    text = 'text'
    id = 'id'
    hash = 'hash'


class Transaction(TimeStampedModel, db.Model):
    id = db.Column(db.String(40), primary_key=True, default=str(uuid.uuid4()))
    # Stellar account to watch, and asset that is being transactioned
    # NOTE: these fields should not be publicly exposed
    stellar_account = db.Column(db.Text, nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
    These fields can be shown through an API:
    kind = db.Column(db.Enum(KindEnum), default=KindEnum.deposit, nullable=False)
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.pending_external, nullable=False)
    status_eta = db.Column(db.Integer, default=3600)
    status_message = db.Column(db.Text)
    stellar_transaction_id = db.Column(db.Text)
    external_transaction_id = db.Column(db.Text)
    amount_in = db.Column(db.Decimal, precision=30, scale=7)
    amount_out = db.Column(db.Decimal,precision=30, scale=7)
    amount_fee = db.Column(db.Decimal, precision=30, scale=7)
    started_at = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    completed_at = db.Column(db.DateTime)
    from_address = db.Column(db.Text)
    to_address = db.Column(db.Text)
    external_extra = db.Column(db.Text)
    external_extra_text = db.Column(db.Text)
    deposit_memo = db.Column(db.Text)
    deposit_memo_type = db.Column(db.Enum(MemoTypesEnum), default=MemoTypesEnum.text, nullable=False)
    withdraw_anchor_account = db.Column(db.Text)
    withdraw_memo = db.Column(db.Text)
    withdraw_memo_type = db.Column(db.Enum(MemoTypesEnum), default=MemoTypesEnum.text, nullable=False)
    refunded = db.Column(db.Boolean, default=False, nullable=False)

    def asset_name(self):
        return self.asset.code + ':' + self.asset.issuer

