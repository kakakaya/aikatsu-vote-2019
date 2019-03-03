import datetime
from peewee import *

DATABASE = "dev_ranking.db"

db = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        legacy_table_names = False
        database = db


class Entry(BaseModel):
    name = TextField(index=True, unique=True)


class RankingLog(BaseModel):
    created = DateTimeField(default=datetime.datetime.now)


class EntryRankingLog(BaseModel):
    entry = ForeignKeyField(Entry)
    ranking_log = ForeignKeyField(RankingLog)
    rank = IntegerField()


def save_ranking(ranking):
    ranking_log = RankingLog.create()
    for rank, name in enumerate(ranking):
        rank += 1
        try:
            entry = Entry.get(Entry.name == name)
        except Exception as e:
            entry = Entry.create(name=name)

        EntryRankingLog.create(
            entry=entry,
            rank=rank,
            ranking_log=ranking_log,
        )


def recent_rankings(hour_range=6):
    # rankings = RankingLog.select(
    #     RankingLog.created,
    #     EntryRankingLog.rank,
    # ).order_by(
    #     RankingLog.created.desc()
    # ).limit(hour_range).join(EntryRankingLog, JOIN.LEFT_OUTER).where(RankingLog.id == EntryRankingLog.ranking_log)
    Latest = RankingLog.alias()
    latest_query = Latest.select().order_by(Latest.created.desc()).limit(hour_range)
    query = RankingLog.select(
        Entry.name,
        EntryRankingLog,
        RankingLog,
    ).join(EntryRankingLog).join_from(EntryRankingLog, Entry)

    # query = EntryRankingLog.select(
    #     EntryRankingLog.rank,
    #     Entry.name,
    #     RankingLog.created,
    # ).join(Entry).join_from(Latest, JOIN.RIGHT_OUTER)

    # rankings = (
    #     RankingLog.select(RankingLog.created,
    # # EntryRankingLog.rank,
    # # Entry.name,
    #                       ).order_by(RankingLog.created.desc()).limit(hour_range)
    # )

    # rankings = rankings.join(
    #     EntryRankingLog,
    #     JOIN.LEFT_OUTER,
    # ).join(
    #     Entry,
    #     JOIN.LEFT_OUTER,
    # )
    print(query.sql())

    return query


def init_db():
    # ranking = get_ranking()
    db.connect()
    db.create_tables([Entry, RankingLog, EntryRankingLog])
