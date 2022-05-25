from google.cloud import datastore


class DataAccess(object):

    _db = datastore.Client()

    def __init__(self, kind=None, namespace=None, eid=None):
        self.kind = kind
        self.namespace = namespace
        self.cur_key = self._get_key(eid)
        self.entity = datastore.Entity(key=self.cur_key)

    def _get_key(self, eid):
        """ creates the key instance """
        # key instance with id
        if eid:
            key = self._db.key(self.kind, int(eid), namespace=self.namespace)
        # key instance without id
        else:
            key = self._db.key(self.kind, namespace=self.namespace)
        return key

    def get_db_instance(self):
        return self._db

    def add_entity(self, dict_ob=None):
        """ add an entity to db """
        if dict_ob:
            self.entity.update(dict_ob)
        self._db.put(self.entity)

    def delete_entity(self, get=True):
        """ gets entity if get and deletes it"""
        if get:
            self.get_single_entity()
        self._db.delete(self.cur_key)

    def get_single_entity(self):
        """ gets entity and raises Value error if entity does not exist """
        self.entity = self._db.get(self.cur_key)
        if self.entity is None:
            raise ValueError

    def update_only_single(self, data=None):
        """ updates entity instance and sets in db """
        if data:
            self.entity.update(data)
        self._db.put(self.entity)

    def get_all(self):
        query = self._db.query(kind=self.kind, namespace=self.namespace)
        return list(query.fetch())

    def get_all_filtered(self, filter:tuple=None):
        """ retrieves all entities with the given kind in namespace"""
        query = self._db.query(kind=self.kind, namespace=self.namespace)
        if filter:
            query.add_filter(filter[0], filter[1], filter[2])
        return query.fetch()

    def get_all_paginated(self, limit=5, start_cursor=None):
        """ retrieves entities based on limit and cursor """
        query = self._db.query(kind=self.kind, namespace=self.namespace)
        if start_cursor:
            return query.fetch(start_cursor=start_cursor, limit=limit)
        else:
            return query.fetch(limit=limit)
