import os
import uuid
from base64 import b64encode, b64decode
import hashlib

from sqlalchemy import MetaData, UniqueConstraint, Identity, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.dialects.postgresql import VARCHAR, TEXT, INTEGER, UUID, REAL


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "pk": "pk_%(table_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "ix": "ix_%(table_name)s_%(column_0_name)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
        }
    )
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped['uuid.UUID'] = mapped_column(primary_key=True)
    username: Mapped['str'] = mapped_column(unique=True)
    password: Mapped['str'] = mapped_column(VARCHAR(256))
    first_name: Mapped['str'] = mapped_column()
    last_name: Mapped['str'] = mapped_column()
    middle_name: Mapped['str'] = mapped_column(nullable=True)

    __table_args__ = (
        UniqueConstraint('first_name', 'last_name', 'middle_name'),
    )

    def generate_salted_hash(self):
        salt = os.urandom(16)
        hashed = b64encode(hashlib.scrypt(bytes(self.password, encoding='utf-8'), n=8192, r=16, p=1, salt=salt)).\
            decode('utf-8')
        self.password = f"{b64encode(salt).decode('utf-8')}|{hashed}"
        return self.password

    def compare_hash(self, password):
        salt, hashed = self.password.split('|')
        salt = b64decode(salt)
        if not (b64encode(hashlib.scrypt(bytes(password, encoding='utf-8'), n=8192, r=16, p=1, salt=salt)).
                decode('utf-8') == hashed):
            return False
        return True


class Dealer(Base):
    __tablename__ = 'dealers'

    id: Mapped['int'] = mapped_column(Identity(start=1, increment=1),
                                      primary_key=True)
    name: Mapped['str'] = mapped_column(VARCHAR(512))
    address: Mapped['str'] = mapped_column(VARCHAR(512))
    contact_phone: Mapped['str'] = mapped_column(VARCHAR(11))
    email: Mapped['str'] = mapped_column(VARCHAR(256))

    __table_args__ = (
        UniqueConstraint(
            'name', 'address'
        ),
    )


class DealerUser(Base):
    __tablename__ = 'dealer_users'

    user_id: Mapped['uuid.UUID'] = mapped_column(ForeignKey('users.id',
                                                            onupdate='CASCADE',
                                                            ondelete='CASCADE'),
                                                 primary_key=True)
    dealer_id: Mapped['int'] = mapped_column(ForeignKey('dealers.id',
                                                        onupdate='CASCADE',
                                                        ondelete='CASCADE'),
                                             primary_key=True)


class Car(Base):
    __tablename__ = 'cars'

    vin: Mapped['str'] = mapped_column(VARCHAR(17),
                                       primary_key=True)
    dealer_id: Mapped['int'] = mapped_column(ForeignKey('dealers.id',
                                                        onupdate='CASCADE',
                                                        ondelete='RESTRICT'))
    equipment: Mapped['int'] = mapped_column(ForeignKey('equipments.id',
                                                        onupdate='CASCADE',
                                                        ondelete='RESTRICT'))
    model_color: Mapped['int'] = mapped_column(ForeignKey('model_colors.id',
                                                          onupdate='CASCADE',
                                                          ondelete='RESTRICT'))
    extra_equipment: Mapped['str'] = mapped_column(TEXT,
                                                   nullable=True)
    gifts: Mapped['str'] = mapped_column(TEXT,
                                         nullable=True)

    model_color_img: Mapped['ModelColor'] = relationship()
    equipments: Mapped['Equipment'] = relationship()
    dealer: Mapped['Dealer'] = relationship(back_populates='cars')


class ModelColor(Base):
    __tablename__ = 'model_colors'

    id: Mapped['int'] = mapped_column(Identity(start=1, increment=1, cache=10),
                                      primary_key=True)
    model_id: Mapped['int'] = mapped_column(ForeignKey('models.id',
                                                       onupdate='CASCADE',
                                                       ondelete='RESTRICT'))
    color_id: Mapped['int'] = mapped_column(ForeignKey('colors.id',
                                                       onupdate='CASCADE',
                                                       ondelete='RESTRICT'))
    filename: Mapped['str'] = mapped_column(VARCHAR(64),
                                            nullable=True)


class Model(Base):
    __tablename__ = 'models'

    id: Mapped['int'] = mapped_column(Identity(start=1, increment=1, cache=10),
                                      primary_key=True)
    name: Mapped['str'] = mapped_column(VARCHAR(64))


class Equipment(Base):
    __tablename__ = 'equipments'

    id: Mapped['int'] = mapped_column(Identity(start=1, increment=1, cache=10),
                                      primary_key=True)
    model: Mapped['int'] = mapped_column(ForeignKey('models.id',
                                                    onupdate='CASCADE',
                                                    ondelete='RESTRICT'))
    engine: Mapped['int'] = mapped_column(ForeignKey('engines.id',
                                                     onupdate='CASCADE',
                                                     ondelete='RESTRICT'))
    transmission: Mapped['int'] = mapped_column(ForeignKey('transmissions.id',
                                                           onupdate='CASCADE',
                                                           ondelete='RESTRICT'))


class Engine(Base):
    __tablename__ = 'engines'

    id: Mapped['int'] = mapped_column(Identity(start=1, increment=1, cache=10),
                                      primary_key=True)
    name: Mapped['str'] = mapped_column(VARCHAR(128))
    # manufacturer: Mapped['int'] = mapped_column()  ? ACTECO only
    volume: Mapped['float'] = mapped_column(REAL)
    hps: Mapped['int'] = mapped_column(INTEGER)
    consumption: Mapped['float'] = mapped_column(REAL)
    acceleration: Mapped['float'] = mapped_column(REAL)


class Transmission(Base):
    __tablename__ = 'transmissions'

    id: Mapped['int'] = mapped_column(Identity(start=1, increment=1, cache=10),
                                      primary_key=True)
    type: Mapped['int'] = mapped_column(ForeignKey('transmission_types.id',
                                                   onupdate='CASCADE',
                                                   ondelete='CASCADE'))
    speed: Mapped['int'] = mapped_column(INTEGER)


class TransmissionType(Base):
    __tablename__ = 'transmission_types'

    id: Mapped['int'] = mapped_column(Identity(start=1, increment=1, cache=10),
                                      primary_key=True)
    name: Mapped['str'] = mapped_column(VARCHAR(64))
    description: Mapped['str'] = mapped_column(TEXT)


class Color(Base):
    __tablename__ = 'colors'

    id: Mapped['int'] = mapped_column(Identity(start=1, increment=1, cache=10),
                                      primary_key=True)
    name: Mapped['str'] = mapped_column(VARCHAR(64))
