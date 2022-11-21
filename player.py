class player:    
    def __init__(self, state, position, def_range, att_range, block_time, point = 0):
        print("player created")
        self.state = state
        self.position = position
        self.point = point
        self.def_range = def_range
        self.att_range = att_range
        self.block_time = block_time

    @property
    def _state(self):
        return self.state
    @_state.setter
    def _state(self, new_state):
        self.state = new_state

    @property
    def _position(self):
        return self.position

    @_position.setter
    def _position(self, new_position):
        self.position = new_position

    @property
    def _point(self):
        return self.point
    
    @_point.setter
    def _point(self, new_point):
        self.point = new_point

    @property
    def _def_range(self):
        return self.def_range
    
    @_def_range.setter
    def _def_range(self, new_def_range):
        self.def_range = new_def_range

    @property
    def _att_range(self):
        return self.att_range
    
    @_att_range.setter
    def _att_range(self, new_att_range):
        self.att_range = new_att_range

    @property
    def _block_time(self):
        return self.block_time
    
    @_block_time.setter
    def _block_time(self, new_block_time):
        self.block_time = new_block_time
    