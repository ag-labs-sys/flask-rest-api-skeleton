class Database:

    def __init__(self):
        self.tasks = {}

    def add(self, task):
        self.tasks[str(task.id)] = task
        return len(self.tasks)


    def delete_task(self, uuid):

        try:
            del (self.tasks[str(uuid)])
            return True
        except KeyError:
            return False

    def get_task(self, uuid):

        try:
            task = self.tasks[str(uuid)]
            return task

        except KeyError:
            return None

    def update_task(self, id, data):

        task = self.tasks[id]
        task.text = data['text']
        task.timestamp = data['timestamp']

        self.tasks[id] = task

    def get_all_tasks(self):
        return self.tasks.values()

    def clear(self):

        "clear the tasks"
        self.tasks = {}


# Database session provider
class DBSessionProvider:

    __instance = None

    @staticmethod
    def get_db_session():
        """
        Static access method
        :return:
        """
        if DBSessionProvider.__instance is None:
            DBSessionProvider.__instance = DBSessionProvider._create_database_session()

        return DBSessionProvider.__instance

    @staticmethod
    def _create_database_session():
        """
        Create and return a DB session
        :param self:
        :return:
        """
        return Database()


db_session = DBSessionProvider.get_db_session()
