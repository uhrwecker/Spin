"""Abstract base class for any velocity to come, also sets the API straight"""


class VelocityABC:
    """Abstract base class for any velocity yet to come. Any velocity has to have these entry points."""
    def __init__(self, s, position):
        self.s = s
        self.position = position #might be any position (orbit distance, rel distance etc)

        self.vel = self._calculate_velocity()

    def _calculate_velocity(self):
        """This method is used to calculate the specific velocities
        and should ALWAYS ONLY use the class variables.
        Return:
            (Velocity, ..) AND Gamma = 1 / 1 - sqrt(all_v**2) """

        raise NotImplementedError('You have to build your velocity class correctly bro.')

    def get_velocity(self):
        return self.vel

    def change_position(self, position, recalc=True):
        self.position = position

        if recalc:
            self.vel = self._calculate_velocity()