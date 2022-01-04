from Query_Creator import Query_Creator

class Event:
    # initialize login session
    def __init__(self, event_id, event_name, event_type, event_time):

        # class constructor
        self._event_id = event_id
        self._event_name = event_name
        self.event_type = event_type
        self.event_time = event_time

        def event_insert(self):
            # insert an event into database
            pass

        def event_delete(self):
            # deletes an event from database
            pass

        def event_backup(self):
            # should save event also to an log file located on the server
            pass
