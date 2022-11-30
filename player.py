class player:    
    def __init__(self, position, def_range, att_range, block_time, mvt_speed, att_speed, point = 0, state = "REST"):
        self.state = state
        self.position = position
        self.point = point
        self.def_range = def_range
        self.att_range = att_range
        self.block_time = block_time
        self.mvt_speed = mvt_speed
        self.att_speed = att_speed
        self.moving = False
        self.attacking = False
        self.jumping = False

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

    @property
    def _mvt_speed(self):
        return self.mvt_speed
    
    @_mvt_speed.setter
    def _mvt_speed(self, new_mvt_speed):
        self.mvt_speed = new_mvt_speed

    @property
    def _att_speed(self):
        return self.att_speed
    
    @_att_speed.setter
    def _att_speed(self, new_att_speed):
        self.att_speed = new_att_speed
    
    @property
    def _moving(self):
        return self.moving
    
    @_moving.setter
    def _moving(self, new_moving):
        self.moving = new_moving

    @property
    def _attacking(self):
        return self.attacking
    
    @_attacking.setter
    def _attacking(self, new_attacking):
        self.attacking = new_attacking

    @property
    def _jumping(self):
        return self.jumping
    
    @_jumping.setter
    def _jumping(self, new_jumping):
        self.jumping = new_jumping    