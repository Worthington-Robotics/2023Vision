from SocketTables.python.socketTableClient import SocketTableClient
from constants import Constants


class Connection:
    def __init__(self):
        # Start the SocketTableClient
        self.client = SocketTableClient(Constants.HOST, Constants.PORT)


    def dispatch_tag_pose(self, tag_pose):
        key = 'Tag_Pose'
        value = "" + tag_pose
        self.client.update(key, value)

    def dispatch_robot_pose(self, tx, ty, tz):
        key = 'Robot_Pose'
        value = f"tx{tx}ty{ty}tz{tz}"
        self.client.update(key, value)