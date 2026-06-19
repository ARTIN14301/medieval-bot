from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///medieval_bot.db')

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, unique=True)
    level = Column(Integer, default=1)
    experience = Column(Float, default=0)
    gold = Column(Float, default=100)
    health = Column(Integer, default=100)
    max_health = Column(Integer, default=100)
    attack = Column(Integer, default=10)
    defense = Column(Integer, default=5)
    territory = Column(Integer, default=0)
    territory_gold = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_daily_quest = Column(DateTime, nullable=True)
    is_banned = Column(Boolean, default=False)

    # Relationships
    inventory = relationship("Inventory", back_populates="owner")
    army = relationship("Army", back_populates="owner")
    battles = relationship("Battle", foreign_keys="Battle.player1_id")
    quests = relationship("Quest", back_populates="owner")


class Inventory(Base):
    __tablename__ = "inventory"

    item_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    item_name = Column(String)
    quantity = Column(Integer, default=1)
    item_type = Column(String)  # weapon, armor, potion
    
    owner = relationship("User", back_populates="inventory")


class Army(Base):
    __tablename__ = "army"

    army_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    unit_name = Column(String)
    unit_type = Column(String)  # Knight, Archer, Mage, etc
    quantity = Column(Integer, default=1)
    attack = Column(Integer)
    defense = Column(Integer)
    health = Column(Integer)
    cost = Column(Float)

    owner = relationship("User", back_populates="army")


class Battle(Base):
    __tablename__ = "battles"

    battle_id = Column(Integer, primary_key=True, index=True)
    player1_id = Column(Integer, ForeignKey("users.user_id"))
    player2_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    winner_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    gold_reward = Column(Float, default=0)
    experience_reward = Column(Float, default=0)
    battle_type = Column(String)  # pvp, solo, boss
    created_at = Column(DateTime, default=datetime.utcnow)


class Quest(Base):
    __tablename__ = "quests"

    quest_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    quest_name = Column(String)
    quest_type = Column(String)  # daily, dungeon
    gold_reward = Column(Float)
    experience_reward = Column(Float)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="quests")


class Dungeon(Base):
    __tablename__ = "dungeons"

    dungeon_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    difficulty = Column(Integer)  # 1-5
    required_level = Column(Integer)
    gold_reward = Column(Float)
    experience_reward = Column(Float)
    boss_health = Column(Integer)
    boss_attack = Column(Integer)


class Ranking(Base):
    __tablename__ = "rankings"

    rank_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    rank_type = Column(String)  # wealth, power, level, territory
    rank_position = Column(Integer)
    score = Column(Float)
    updated_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
