import os
import uuid
from base64 import b64encode, b64decode
import hashlib
from typing import List

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
    # middle_name: Mapped['str'] = mapped_column(nullable=True)

    __table_args__ = (
        UniqueConstraint('first_name', 'last_name'),
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
    # address: Mapped['str'] = mapped_column(VARCHAR(512))
    # contact_phone: Mapped['str'] = mapped_column(VARCHAR(11))
    # email: Mapped['str'] = mapped_column(VARCHAR(256))

    __table_args__ = (
        UniqueConstraint(
            'name',  # 'address'
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


class DealerCar(Base):
    __tablename__ = 'dealer_cars'

    dealer_id: Mapped['int'] = mapped_column(ForeignKey('dealers.id',
                                                        onupdate='CASCADE',
                                                        ondelete='CASCADE'),
                                             primary_key=True)
    car_vin: Mapped['str'] = mapped_column(ForeignKey('cars.vin',
                                                      onupdate='CASCADE',
                                                      ondelete='CASCADE'),
                                           primary_key=True)


class Car(Base):
    __tablename__ = 'cars'

    vin: Mapped['str'] = mapped_column(VARCHAR(17),
                                       primary_key=True)
    model_kit: Mapped['int'] = mapped_column(ForeignKey('model_kits.id',
                                                        onupdate='CASCADE',
                                                        ondelete='RESTRICT'))
    engine: Mapped['int'] = mapped_column(ForeignKey('engines.id',
                                                     onupdate='CASCADE',
                                                     ondelete='RESTRICT'))
    transmission: Mapped['int'] = mapped_column(ForeignKey('transmissions.id',
                                                           onupdate='CASCADE',
                                                           ondelete='RESTRICT'))
    colour: Mapped['int'] = mapped_column(ForeignKey('colours.id',
                                                     onupdate='CASCADE',
                                                     ondelete='RESTRICT'))

    model_kit_data: Mapped['ModelKit'] = relationship(passive_deletes=True)
    engine_data: Mapped['Engine'] = relationship(passive_deletes=True)
    transmission_data: Mapped['Transmission'] = relationship(passive_deletes=True)
    colour_data: Mapped['Colour'] = relationship(passive_deletes=True)


class ModelKit(Base):
    __tablename__ = 'model_kits'

    id: Mapped['int'] = mapped_column(Identity(start=1, increment=1),
                                      primary_key=True)
    model_id: Mapped['int'] = mapped_column(ForeignKey('models.id',
                                                       onupdate='CASCADE',
                                                       ondelete='CASCADE'))
    kit_id: Mapped['int'] = mapped_column(ForeignKey('kits.id',
                                                     onupdate='CASCADE',
                                                     ondelete='RESTRICT'))

    __table_args__ = (UniqueConstraint(
        'model_id', 'kit_id'
    ),)


class Model(Base):
    __tablename__ = 'models'

    id: Mapped['int'] = mapped_column(Identity(start=1, increment=1),
                                      primary_key=True)
    name: Mapped['str'] = mapped_column(VARCHAR(64), unique=True)


class Kit(Base):
    __tablename__ = 'kits'

    id: Mapped['int'] = mapped_column(Identity(start=1, increment=1),
                                      primary_key=True)
    name: Mapped['str'] = mapped_column(VARCHAR(64))


class ModelKitParameter(Base):
    __tablename__ = 'model_kit_parameters'

    model_kit_id: Mapped['int'] = mapped_column(ForeignKey('model_kits.id',
                                                           onupdate='CASCADE',
                                                           ondelete='CASCADE'),
                                                primary_key=True)
    parameter_id: Mapped['int'] = mapped_column(ForeignKey('parameters.id',
                                                           onupdate='CASCADE',
                                                           ondelete='CASCADE'),
                                                primary_key=True)

    parameter_data: Mapped[List['Parameter']] = relationship(uselist=True,
                                                             passive_deletes=True)


class Parameter(Base):
    __tablename__ = 'parameters'

    id: Mapped['int'] = mapped_column(Identity(start=1, increment=1),
                                      primary_key=True)
    name: Mapped['str'] = mapped_column(VARCHAR(64))


class Engine(Base):
    __tablename__ = 'engines'

    id: Mapped['int'] = mapped_column(Identity(start=1, increment=1),
                                      primary_key=True)
    name: Mapped['str'] = mapped_column(VARCHAR(64))


class Transmission(Base):
    __tablename__ = 'transmissions'

    id: Mapped['int'] = mapped_column(Identity(start=1, increment=1),
                                      primary_key=True)
    name: Mapped['str'] = mapped_column(VARCHAR(64))


class Colour(Base):
    __tablename__ = 'colours'

    id: Mapped['int'] = mapped_column(Identity(start=1, increment=1),
                                      primary_key=True)
    name: Mapped['str'] = mapped_column(VARCHAR(64))
