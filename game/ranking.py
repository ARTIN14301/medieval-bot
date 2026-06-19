from models.database import SessionLocal, User, Ranking
from sqlalchemy import desc


class RankingSystem:
    """سیستم رنکینگ"""

    def __init__(self):
        self.db = SessionLocal()

    def update_rankings(self):
        """به‌روزرسانی رنکینگ‌ها"""
        users = self.db.query(User).all()

        # رنکینگ ثروت
        wealth_ranking = sorted(users, key=lambda u: u.gold, reverse=True)
        for i, user in enumerate(wealth_ranking, 1):
            ranking = self.db.query(Ranking).filter(
                Ranking.user_id == user.user_id,
                Ranking.rank_type == 'wealth'
            ).first()
            if ranking:
                ranking.rank_position = i
                ranking.score = user.gold
            else:
                ranking = Ranking(
                    user_id=user.user_id,
                    rank_type='wealth',
                    rank_position=i,
                    score=user.gold
                )
                self.db.add(ranking)

        # رنکینگ قدرت
        power_ranking = sorted(users, key=lambda u: u.attack + u.defense, reverse=True)
        for i, user in enumerate(power_ranking, 1):
            ranking = self.db.query(Ranking).filter(
                Ranking.user_id == user.user_id,
                Ranking.rank_type == 'power'
            ).first()
            if ranking:
                ranking.rank_position = i
                ranking.score = user.attack + user.defense
            else:
                ranking = Ranking(
                    user_id=user.user_id,
                    rank_type='power',
                    rank_position=i,
                    score=user.attack + user.defense
                )
                self.db.add(ranking)

        # رنکینگ سطح
        level_ranking = sorted(users, key=lambda u: (u.level, u.experience), reverse=True)
        for i, user in enumerate(level_ranking, 1):
            ranking = self.db.query(Ranking).filter(
                Ranking.user_id == user.user_id,
                Ranking.rank_type == 'level'
            ).first()
            if ranking:
                ranking.rank_position = i
                ranking.score = user.level
            else:
                ranking = Ranking(
                    user_id=user.user_id,
                    rank_type='level',
                    rank_position=i,
                    score=user.level
                )
                self.db.add(ranking)

        # رنکینگ قلمرو
        territory_ranking = sorted(users, key=lambda u: u.territory, reverse=True)
        for i, user in enumerate(territory_ranking, 1):
            ranking = self.db.query(Ranking).filter(
                Ranking.user_id == user.user_id,
                Ranking.rank_type == 'territory'
            ).first()
            if ranking:
                ranking.rank_position = i
                ranking.score = user.territory
            else:
                ranking = Ranking(
                    user_id=user.user_id,
                    rank_type='territory',
                    rank_position=i,
                    score=user.territory
                )
                self.db.add(ranking)

        self.db.commit()

    def get_top_ranking(self, rank_type, limit=10):
        """دریافت بهترین رنکینگ‌ها"""
        rankings = self.db.query(Ranking).filter(
            Ranking.rank_type == rank_type
        ).order_by(Ranking.rank_position).limit(limit).all()

        result = []
        for rank in rankings:
            user = self.db.query(User).filter(User.user_id == rank.user_id).first()
            if user:
                result.append({
                    'position': rank.rank_position,
                    'username': user.username,
                    'score': rank.score,
                    'level': user.level
                })
        return result

    def get_user_ranking(self, user_id):
        """دریافت رنکینگ کاربر"""
        result = {}
        for rank_type in ['wealth', 'power', 'level', 'territory']:
            ranking = self.db.query(Ranking).filter(
                Ranking.user_id == user_id,
                Ranking.rank_type == rank_type
            ).first()
            if ranking:
                result[rank_type] = ranking.rank_position
        return result

    def close(self):
        self.db.close()
