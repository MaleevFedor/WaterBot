from data.user_class import User
from data import db_session
from datetime import datetime


def count_streaks():
    cur = datetime.now()
    cur = 24 - int(cur.hour)
    print(cur)
    db_sess = db_session.create_session()
    for i in db_sess.query(User).filter(User.timezone == cur).all():
        if i.drinked < i.goal:
            db_sess.query(User).filter(User.tg_id == i.tg_id).update({'streak': 0})
        db_sess.query(User).filter(User.tg_id == i.tg_id).update({'drinked': 0})
        db_sess.commit()
    db_sess.close()
