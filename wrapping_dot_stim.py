import numpy
from numpy import *
from psychopy import visual


class WrappingDotStim(visual.DotStim):
    circle_squared_field_size: object
    density: object
    _dotsXYBackUp: object
    circlesNDots: object
    _dotsXYBackUp: numpy.array
    rate_circle_to_square = 1

    def __init__(self,
                 win,
                 units='',
                 density=1,
                 coherence=0.5,
                 fieldPos=(0.0, 0.0),
                 fieldSize=(1.0, 1.0),
                 fieldShape='sqr',
                 dotSize=2.0,
                 dotLife=3,
                 dir=0.0,
                 speed=0.5,
                 rgb=None,
                 color=(1.0, 1.0, 1.0),
                 colorSpace='rgb',
                 opacity=1.0,
                 contrast=1.0,
                 depth=0,
                 element=None,
                 signalDots='same',
                 noiseDots='direction',
                 name=None,
                 autoLog=None):
        self.density = density
        self.circlesNDots = int(self.density_to_number_of_dots(density, fieldSize))
        self.circle_squared_field_size = fieldSize

        if fieldShape == 'circle':  # make more dots than we need and only use those that are within circle
            # the size if fake for the calculation of updatesXY.
            fieldSize *= 2
            # the rate should be greater in order to catch the needed point in the circle
            self.rate_circle_to_square = 16

        visual.DotStim.__init__(self,
                                win=win,
                                units=units,
                                nDots=int(self.rate_circle_to_square * self.density_to_number_of_dots(density,
                                                                                                      self.circle_squared_field_size)),
                                coherence=coherence,
                                fieldPos=fieldPos,
                                fieldSize=fieldSize,
                                fieldShape=fieldShape,
                                dotSize=dotSize,
                                dotLife=dotLife,
                                dir=dir,
                                speed=speed,
                                rgb=rgb,
                                color=color,
                                colorSpace=colorSpace,
                                opacity=opacity,
                                contrast=contrast,
                                depth=depth,
                                element=element,
                                signalDots=signalDots,
                                noiseDots=noiseDots,
                                name=name,
                                autoLog=autoLog)

    def _newDotsXY(self, nDots):
        """Returns a uniform spread of dots, according to the
            fieldShape and fieldSize
            usage::
            dots = self._newDots(nDots) """
        if self.fieldShape == 'circle':  # make more dots than we need and only use those that are within circle

            dots_in_circle = 0

            while dots_in_circle < int(nDots / self.rate_circle_to_square):
                self._newDots = numpy.array(numpy.random.uniform(-self.fieldSize[0] / 2.0,
                                                                 self.fieldSize[0] / 2.0,
                                                                 [nDots, 2]))
                self._dotsXYBackUp = numpy.copy(self._newDots)

                filtered_dots = self._newDots[
                    numpy.hypot(self._newDots[:, 0], self._newDots[:, 1]) < self.circle_squared_field_size / 2]
                dots_in_circle = len(filtered_dots)

            return filtered_dots[0:self.density_to_number_of_dots(self.density, self.circle_squared_field_size) + 1:1]

        else:
            return numpy.array(numpy.random.uniform(-self.fieldSize[0] / 2.0, self.fieldSize[0] / 2.0, [nDots, 2]))

    def newDotsXYCircle(self, nDots):
        dots_in_circle = 0
        while dots_in_circle * 15 < nDots:
            self._newDots = numpy.array(numpy.random.uniform(-self.fieldSize[0] / 2.0,
                                                             self.fieldSize[0] / 2.0,
                                                             [nDots * self.rate_circle_to_square, 2]))

            filtered_dots = self._newDots[
                numpy.hypot(self._newDots[:, 0], self._newDots[:, 1]) < self.circle_squared_field_size / 2]
            dots_in_circle = len(filtered_dots)

        return self._newDots[0:nDots:1]

    def _update_dotsXY(self):
        """
        The user shouldn't call this - its gets done within draw()
        """
        """Find dead dots, update positions, get new positions for dead and out-of-bounds 
        """

        if self.fieldShape == 'circle':
            self.nDots = self.circlesNDots * self.rate_circle_to_square
        else:
            self._dotsXYBackUp = self._dotsXY

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
            self._dotsXYBackUp[:, 0] += self.speed * numpy.reshape(numpy.cos(self._dotsDir), (self.nDots,))
            self._dotsXYBackUp[:, 1] += self.speed * numpy.reshape(numpy.sin(self._dotsDir),
                                                                   (self.nDots,))  # 0 radians=East!
        elif self.noiseDots == 'direction':
            # simply use the stored directions to update position
            self._dotsXYBackUp[:, 0] += self.speed * numpy.reshape(numpy.cos(self._dotsDir), (self.nDots,))
            self._dotsXYBackUp[:, 1] += self.speed * numpy.reshape(numpy.sin(self._dotsDir),
                                                                   (self.nDots,))  # 0 radians=East!
        elif self.noiseDots == 'position':
            # update signal dots
            self._dotsXYBackUp[self._signalDots, 0] += self.speed * numpy.reshape(
                numpy.cos(self._dotsDir[self._signalDots]),
                (self._signalDots.sum(),))
            self._dotsXYBackUp[self._signalDots, 1] += self.speed * numpy.reshape(
                numpy.sin(self._dotsDir[self._signalDots]),
                (
                    self._signalDots.sum(),))  # 0 radians=East!
            # update noise dots
            dead = dead + (~self._signalDots)  # just create new ones
        # handle boundaries of the field
        if self.fieldShape in [None, 'square', 'sqr', 'circle']:
            self._dotsXYBackUp[(self._dotsXYBackUp[:, 0] > (self.fieldSize[0] / 2.0)),
                               0] = numpy.subtract(numpy.mod((self._dotsXYBackUp[(self._dotsXYBackUp[:,
                                                                                  0] > (self.fieldSize[0] / 2.0)), 0]),
                                                             (self.fieldSize[0] / 2.0)),
                                                   (self.fieldSize[0] / 2.0))
            self._dotsXYBackUp[(self._dotsXYBackUp[:, 1] > (self.fieldSize[1] / 2.0)),
                               1] = numpy.subtract(numpy.mod((self._dotsXYBackUp[(self._dotsXYBackUp[:,
                                                                                  1] > (self.fieldSize[1] / 2.0)), 1]),
                                                             (self.fieldSize[1] / 2.0)),
                                                   (self.fieldSize[1] / 2.0))
            self._dotsXYBackUp[(self._dotsXYBackUp[:, 0] < -(self.fieldSize[0] / 2.0)),
                               0] = numpy.mod(self._dotsXYBackUp[(self._dotsXYBackUp[:, 0] < -(self.fieldSize[0] /
                                                                                               2.0)), 0],
                                              (self.fieldSize[0] / 2.0))
            self._dotsXYBackUp[(self._dotsXYBackUp[:, 1] < -(self.fieldSize[1] / 2.0)),
                               1] = numpy.mod(self._dotsXYBackUp[(self._dotsXYBackUp[:, 1] < -(self.fieldSize[1] /
                                                                                               2.0)), 1],
                                              (self.fieldSize[1] / 2.0))

        if self.fieldShape == 'circle':
            # add out-of-bounds to those that need replacing
            # update any dead dots
            if sum(dead):
                self._dotsXYBackUp[dead, :] = self.newDotsXYCircle(sum(dead))

            # transform to a normalised circle (radius = 1 all around) then to polar coords to check
            filterd_dots_in_circle = self._dotsXYBackUp[numpy.hypot \
                                         (self._dotsXYBackUp[:, 0],
                                          self._dotsXYBackUp[:, 1]) < self.circle_squared_field_size / 2]

            filterd_dots_in_circle = filterd_dots_in_circle[
                  0:self.density_to_number_of_dots(self.density, self.circle_squared_field_size) + 1:1]

            self._dotsXY[:] = filterd_dots_in_circle[:]

        else:
            # add out-of-bounds to those that need replacing
            # update any dead dots
            if sum(dead):
                self._dotsXYBackUp[dead, :] = self._newDotsXY(sum(dead))
                self._dotsXY[:] = self._dotsXYBackUp[:]

        if self.fieldShape == 'circle':
            self.nDots = self.circlesNDots

        print('a')

        # update the pixel XY coordinates
        self._updateVertices()

    def density_to_number_of_dots(self, dots_density, field_size):
        # todo: check here if a caculation of the field size is also correct for the degree dimension.
        # todo: check here if the numer of dots should be different for type of 'circle'.
        return int(dots_density * field_size ** 2 / 2)
        pass
