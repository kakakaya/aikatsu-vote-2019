import datetime
from peewee import SqliteDatabase, Model, TextField, DateTimeField, ForeignKeyField, IntegerField, JOIN

DATABASE = "/host/ranking.db"

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


def rankings():
    query = RankingLog.select(
        Entry.name,
        EntryRankingLog,
        RankingLog,
    ).join(EntryRankingLog).join_from(EntryRankingLog, Entry)
    return query


def recent_rankings(hour_range=6):
    recent_logs = RankingLog.select(RankingLog.id).order_by(RankingLog.created.desc()).limit(hour_range)

    query = (
        EntryRankingLog.select(Entry, RankingLog, EntryRankingLog).join_from(
            EntryRankingLog,
            Entry,
        ).join_from(
            EntryRankingLog,
            RankingLog,
        ).where(EntryRankingLog.ranking_log.in_(recent_logs))
    )

    return query


def recent_rankings_for_entry(entry_name, desc=True, hour_range=24):
    """Returns ranking for entry.
    """
    if desc:
        ranking_order = RankingLog.created.desc()
    else:
        ranking_order = RankingLog.created.asc()
    recent_logs = RankingLog.select(RankingLog.id).order_by(ranking_order).limit(hour_range)

    query = (
        EntryRankingLog.select(Entry, RankingLog, EntryRankingLog).join_from(
            EntryRankingLog,
            Entry,
        ).join_from(
            EntryRankingLog,
            RankingLog,
        ).where(EntryRankingLog.ranking_log.in_(recent_logs) & Entry.name % "*{}*".format(entry_name))
    )

    return query


def recent():
    query = Entry.select(
        Entry.name,
        EntryRankingLog.rank,
        RankingLog.created,
    ).join(EntryRankingLog).join(RankingLog)

    print(query.sql())
    return query


def init_db():
    db.connect()
    db.create_tables([Entry, RankingLog, EntryRankingLog])
