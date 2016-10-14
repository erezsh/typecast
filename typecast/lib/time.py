from __future__ import absolute_import
import time

from ..typecast import typecast_decor, CastError, Typecast, autocast

class Unit(metaclass=Typecast):

    def __init__(self, value):
        setattr(self, self._attr, value)

    def __repr__(self):
        return "%s(%g)" % (self.__class__.__name__, getattr(self, self._attr))

class TimeUnit(Unit):
    def __add__(self, other):
        return Seconds((self >> Seconds).seconds + (other >> Seconds).seconds) >> type(self)

    def __sub__(self, other):
        return Seconds((self >> Seconds).seconds - (other >> Seconds).seconds) >> type(self)

    def __mul__(self, scalar):
        assert isinstance(scalar, (int, float))
        return type(self)(getattr(self, self._attr) * scalar)

    def __div__(self, scalar):
        assert isinstance(scalar, (int, float))
        return type(self)(getattr(self, self._attr) / scalar)

    def __eq__(self, other):
        other = other >> type(self)
        return getattr(self, self._attr) == getattr(other, self._attr)

    def __lt__(self, other):
        other = other >> type(self)
        return getattr(self, self._attr) < getattr(other, self._attr)

    def __ne__(self, other):
        return not (self == other)
    def __gt__(self, other):
        return other < self
    def __ge__(self, other):
        return not (self < other)
    def __le__(self, other):
        return not (other < self)

    def __hash__(self):
        return hash((self >> Seconds).seconds)


class Seconds(TimeUnit):
    _attr = 'seconds'


class Millisecs(TimeUnit):
    _attr = 'millisecs'

    def to__Seconds(self, cls):
        return cls(self.millisecs / 1000.0)

    def from__Seconds(cls, seconds):
        return cls(seconds.seconds * 1000.0)


class Minutes(TimeUnit):
    _attr = 'minutes'

    def to__Seconds(self, cls):
        return cls(self.minutes * 60.0)

    def from__Seconds(cls, seconds):
        return cls(seconds.seconds / 60.0)

class Hours(TimeUnit):
    _attr = 'hours'

    def to__Seconds(self, cls):
        return cls(self.hours * (60.0 * 60.0))

    def from__Seconds(cls, seconds):
        return cls(seconds.seconds / (60.0 * 60.0))

class Days(TimeUnit):
    _attr = 'days'

    def to__Seconds(self, cls):
        return cls(self.days * (60.0 * 24.0 * 60.0))

    def from__Seconds(cls, seconds):
        return cls(seconds.seconds / (24.0 * 60.0 * 60.0))


class Weeks(TimeUnit):
    _attr = 'weeks'

    def to__Days(self, cls):
        return cls(self.weeks * 7)

    def from__Days(cls, days):
        return cls(days.days / 7.0)


@autocast
def sleep(secs: Seconds):
    time.sleep(secs.seconds)

