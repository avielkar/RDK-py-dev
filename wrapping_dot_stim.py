import numpy
from numpy import *
from psychopy import visual


class WrappingDotStim(visual.DotStim):
    def _newDotsXY(self, nDots):
        """Returns a uniform spread of dots, according to the
            fieldShape and fieldSize
            usage::
            dots = self._newDots(nDots) """
        if self.fieldShape == 'circle':  # make more dots than we need and only use those that are within circle
            while True:  # repeat until we have enough
                new = numpy.random.uniform(-1, 1, [nDots * 2, 2])  # fetch twice as many as needed
                inCircle = (numpy.hypot(new[:, 0], new[:, 1]) < 1)
                if sum(inCircle) >= nDots:
                    return numpy.array(new[inCircle, :][:nDots, :] * self.fieldSize / 2.0)
        else:
            return numpy.array(numpy.random.uniform(-self.fieldSize / 2.0, self.fieldSize / 2.0, [nDots, 2]))

    def _update_dotsXY(self):
        """
        The user shouldn't call this - its gets done within draw()
        """
        """Find dead dots, update positions, get new positions for dead and out-of-bounds 
        """
        # renew dead dots
        if self.dotLife > 0:  # if less than zero ignore it
            self._dotsLife -= 1  # decrement. Then dots to be reborn will be negative
            dead = (self._dotsLife <= 0.0)
            self._dotsLife[dead] = self.dotLife
        else:
            dead = numpy.zeros(self.nDots, dtype=bool)
        ##update XY based on speed and dir
        # NB self._dotsDir is in radians, but self.dir is in degs
        # update which are the noise/signal dots
        if self.signalDots == 'different':
            #  **up to version 1.70.00 this was the other way around, not in keeping with Scase et al**
            # noise and signal dots change identity constantly
            numpy.random.shuffle(self._dotsDir)
            self._signalDots = (self._dotsDir == (self.dir * pi / 180))  # and then update _signalDots from that
        # update the locations of signal and noise
        if self.noiseDots == 'walk':
            # noise dots are ~self._signalDots
            self._dotsDir[~self._signalDots] = numpy.random.rand((~self._signalDots).sum()) * pi * 2
            # then update all positions from dir*speed
            self._dotsXY[:, 0] += self.speed * numpy.reshape(numpy.cos(self._dotsDir), (self.nDots,))
            self._dotsXY[:, 1] += self.speed * numpy.reshape(numpy.sin(self._dotsDir), (self.nDots,))  # 0 radians=East!
        elif self.noiseDots == 'direction':
            # simply use the stored directions to update position
            self._dotsXY[:, 0] += self.speed * numpy.reshape(numpy.cos(self._dotsDir), (self.nDots,))
            self._dotsXY[:, 1] += self.speed * numpy.reshape(numpy.sin(self._dotsDir), (self.nDots,))  # 0 radians=East!
        elif self.noiseDots == 'position':
            # update signal dots
            self._dotsXY[self._signalDots, 0] += self.speed * numpy.reshape(numpy.cos(self._dotsDir[self._signalDots]),
                                                                            (self._signalDots.sum(),))
            self._dotsXY[self._signalDots, 1] += self.speed * numpy.reshape(numpy.sin(self._dotsDir[self._signalDots]),
                                                                            (
                                                                            self._signalDots.sum(),))  # 0 radians=East!
            # update noise dots
            dead = dead + (~self._signalDots)  # just create new ones
        # handle boundaries of the field
        if self.fieldShape in [None, 'square', 'sqr']:
            self._dotsXY[(self._dotsXY[:, 0] > (self.fieldSize / 2.0)), 0] = numpy.subtract(
                numpy.mod((self._dotsXY[(self._dotsXY[:, 0] > (self.fieldSize / 2.0)), 0]), (self.fieldSize / 2.0)),
                (self.fieldSize / 2.0))
            self._dotsXY[(self._dotsXY[:, 1] > (self.fieldSize / 2.0)), 1] = numpy.subtract(
                numpy.mod((self._dotsXY[(self._dotsXY[:, 1] > (self.fieldSize / 2.0)), 1]), (self.fieldSize / 2.0)),
                (self.fieldSize / 2))
            self._dotsXY[(self._dotsXY[:, 0] < -(self.fieldSize / 2.0)), 0] = numpy.mod(
                self._dotsXY[(self._dotsXY[:, 0] < -(self.fieldSize / 2.0)), 0], (self.fieldSize / 2.0))
            self._dotsXY[(self._dotsXY[:, 1] < -(self.fieldSize / 2.0)), 1] = numpy.mod(
                self._dotsXY[(self._dotsXY[:, 1] < -(self.fieldSize / 2.0)), 1], (self.fieldSize / 2.0))

        elif self.fieldShape == 'circle':
            # transform to a normalised circle (radius = 1 all around) then to polar coords to check
            normXY = self._dotsXY / (self.fieldSize / 2.0)  # the normalised XY position (where radius should be <1)
            dead = dead + (numpy.hypot(normXY[:, 0], normXY[:, 1]) > 1)
        # add out-of-bounds to those that need replacing
        # update any dead dots
        if sum(dead):
            self._dotsXY[dead, :] = self._newDotsXY(sum(dead))
        # update the pixel XY coordinates
        self._calcDotsXYRendered()
