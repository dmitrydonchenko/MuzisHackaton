####### Класс работы с БД пользователей и событий ########

import peewee

db = peewee.MySQLDatabase('muzis', user='vkrent', passwd='VkRentDb')


class MySQLModel(peewee.Model):
    class Meta:
        database = db


# Класс таблицы пользователей в БД
class Users(MySQLModel):
    id = peewee.CharField(primary_key=True)   # id пользователя в мессенджере
    user_name = peewee.CharField()            # имя пользователя
    login = peewee.CharField()


# Класс таблицы исполнителей
class Artists(MySQLModel):
    id = peewee.CharField(primary_key=True)


# Класс таблицы событий в БД
class Events(MySQLModel):
    id = peewee.BigIntegerField(primary_key=True)
    event_name = peewee.CharField()
    url = peewee.CharField()
    city = peewee.CharField()
    artist_id = peewee.ForeignKeyField(Artists, db_column='artist_id', to_field='id', related_name='artists_events')


# Класс таблицы исполнителей и пользователей
class UsersArtists(MySQLModel):
    id = peewee.BigIntegerField(primary_key=True)
    user_id = peewee.ForeignKeyField(Users, db_column='user_id', to_field='id', related_name='users_artists')
    artist_id = peewee.ForeignKeyField(Artists, db_column='artist_id', to_field='id', related_name='artists_users')


# Класс таблицы пользователей и событий в БД
class UsersEvents(MySQLModel):
    id = peewee.BigIntegerField(primary_key=True)
    user_id = peewee.ForeignKeyField(Users, db_column='user_id', to_field='id', related_name='users_events')
    event_id = peewee.ForeignKeyField(Events, db_column='event_id', to_field='id', related_name='events_users')

############# Методы добавления ################


# Добавляет нового пользователя в БД
def insert_user(user_id, name, m_login):
    if not is_user_exists(user_id):
        res = Users.insert(id = user_id, user_name = name, login = m_login).execute()
        return res
    return -1


# Добавляет новое событие в БД
def insert_event(name, event_url, event_city, artist_name):
    if not is_event_exists(event_url):
        res = Events.insert(event_name = name, url = event_url, city = event_city, artist_id = artist_name).execute()
        return res
    return -1


# Добавить пользователя в список участников события
def checkin_user(m_user_id, m_event_id):
    res = UsersEvents.insert(user_id = m_user_id, event_id = m_event_id).execute()
    return res


# Добавить исполнителя
def insert_artist(artist_name):
    if not is_artist_exists(artist_name):
        res = Artists.insert(id = artist_name).execute()
        return res
    return -1


# Добавить исполнителя в список любимых у пользователя
def insert_user_artist(m_user_id, m_artist_name):
    res = UsersArtists.insert(user_id = m_user_id, artist_id = m_artist_name).execute()
    return res


def get_user_events(user_id):
    res = UsersEvents.select().where(UsersEvents.user_id == user_id)
    events = []
    for r in res:
        events.append(Events.select().where(Events.id == r.event_id))
    return events

######## Методы для получения данных из БД ############


# Возвращает список событий любимых исполнителей пользователя
def get_user_possible_events(user_id):
    db.connect()
    users_favourite_artists = UsersArtists.select().where(UsersArtists.user_id == user_id)
    for artist in users_favourite_artists:
        for event in Events.select().where(Events.artist_id == artist.artist_id.id):
            yield event
    db.close()

def get_user_events(user_id):
    res = UsersEvents.select().where(UsersEvents.user_id == user_id)
    events = []
    for r in res:
        events.append(Events.select().where(Events.id == r.event_id).first())
    return events


# Возвращает список участников события
def get_users_by_event(event_id):
    db.connect()
    users = Users.select().join(UsersEvents.event_id == event_id, UsersEvents.user_id == Users.id)
    db.close()
    return users


def get_user_by_id(user_id):
    return Users.select().where(Users.id == user_id).first()

# Возвращает список людей, которые идут на те же события
def get_soulmates(user_id, event_id):
    users_events = UsersEvents.select().where(UsersEvents.event_id == event_id)
    users =  []
    for user_event in users_events:
        if not user_event.user_id.id == user_id:
            users.append(get_user_by_id(user_event.user_id.id))
    return users


#Возвращает список любимых исполнителей пользователя
def get_favourite_artists(user_id):
    db.connect()
    users_favourite_artists = UsersArtists.select().where(UsersArtists.user_id == user_id)
    db.close()
    return users_favourite_artists

########## Методы проверки ################


# Возвращает True, если исполнитель с таким именем уже существует
def is_artist_exists(artist_name):
    db.connect()
    if (Artists.select().where(Artists.id == artist_name)).count() > 0:
        db.close()
        return True
    db.close()
    return False


# Возвращает True, если событие с данным url уже есть в БД
def is_event_exists(event_url):
    db.connect()
    if (Events.select().where(Events.url == event_url)).count() > 0:
        db.close()
        return True
    db.close()
    return False


# Возвращает True, если пользователь с таким id уже существует
def is_user_exists(user_id):
    db.connect()
    if (Users.select().where(Users.id == user_id)).count() > 0:
        db.close()
        return True
    db.close()
    return False


