
"""
this python file is written orientated by the TUIO spezification
https://www.tuio.org/?specification
It supports only 2D Object|Blob|Cursor

            Profile
                |
    ---------------------
    |           |       |
  Object     Cursor    Blob


"""

from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.osc_message import OscMessage

from .const import TUIO_BLOB, TUIO_CURSOR, TUIO_OBJECT
from .const import TUIO_BLOB25D, TUIO_CURSOR25D, TUIO_OBJECT25D
from .const import TUIO_BLOB3D, TUIO_CURSOR3D, TUIO_OBJECT3D

class Profile:
    """
    custom class of all subjects passing the TUIO connection.
    See more at https://www.tuio.org/?specification

    """

    def __init__(self, session_id):
        self.session_id = session_id

class Object(Profile):
    """
    TUIO Object 2D Interactive Surface
    """
    def __init__(self, session_id):
        super().__init__(session_id)
        self.class_id               = -1            # i
        self.position               = (0, 0)   # x,y
        self.angle                  = 0             # a
        self.velocity               = (0, 0)   # X,Y
        self.velocity_rotation      = 0             # A
        self.motion_acceleration    = 0             # m
        self.rotation_acceleration  = 0             # r

    def get_message(self) -> OscMessage:
        """
        returns the OSC message of the Object with the TUIO spezification
        """
        x, y = self.position
        X, Y = self.velocity
        builder = OscMessageBuilder(address=TUIO_OBJECT)
        for val in [
                "set",
                int(self.session_id),
                int(self.class_id),
                float(x),
                float(y),
                float(self.angle),
                float(X),
                float(Y),
                float(self.velocity_rotation),
                float(self.motion_acceleration),
                float(self.rotation_acceleration)
        ]:
            builder.add_arg(val)
        return builder.build()

class Cursor(Profile):
    """
    TUIO Cursor 2D Interactive Surface
    """
    def __init__(self, session_id):
        super().__init__(session_id)
        self.position               = (0, 0)   # x,y
        self.velocity               = (0, 0)   # X,Y
        self.motion_acceleration    = 0        # m

    def get_message(self)-> OscMessage:
        """
        returns the OSC message of the Cursor with the TUIO spezification
        """
        x, y = self.position
        X, Y = self.velocity
        builder = OscMessageBuilder(address=TUIO_CURSOR)
        for val in [
                "set",
                self.session_id,
                float(x),
                float(y),
                float(X),
                float(Y),
                float(self.motion_acceleration)
        ]:
            builder.add_arg(val)
        return builder.build()

class Blob(Profile):
    # pylint: disable=too-many-instance-attributes
    """
    TUIO Blob 2D Interactive Surface
    """
    def __init__(self, session_id):
        super().__init__(session_id)
        self.position               = (0, 0)        # x,y
        self.angle                  =  5            # a
        self.dimension              = (.1, .1)      # w, h
        self.area                   = 0.1           # f
        self.velocity               = (0.1, 0.1)    # X,Y
        self.velocity_rotation      = 0.1           # A
        self.motion_acceleration    = 0.1           # m
        self.rotation_acceleration  = 0.1           # r

    def get_message(self)-> OscMessage:
        """
        returns the OSC message of the Blob with the TUIO spezification
        """
        x, y = self.position
        X, Y = self.velocity
        w, h = self.dimension
        builder = OscMessageBuilder(address=TUIO_BLOB)
        for val in [
                "set",
                self.session_id,
                float(x),
                float(y),
                float(self.angle),
                float(w),
                float(h),
                float(self.area),
                float(X),
                float(Y),
                float(self.velocity_rotation),
                float(self.motion_acceleration),
                float(self.rotation_acceleration)
        ]:
            builder.add_arg(val)
        return builder.build()


class Object25D(Profile):
    """
    TUIO Object 2.5D Interactive Surface
    """
    def __init__(self, session_id):
        super().__init__(session_id)
        self.class_id               = -1            # i
        self.position               = (0, 0, 0)     # x,y,z
        self.angle                  = 0             # a
        self.velocity               = (0, 0, 0)     # X,Y,Z
        self.velocity_rotation      = 0             # A
        self.motion_acceleration    = 0             # m
        self.rotation_acceleration  = 0             # r

    def get_message(self) -> OscMessage:
        """
        returns the OSC message of the Object with the TUIO spezification
        """
        x, y, z = self.position
        X, Y, Z = self.velocity
        builder = OscMessageBuilder(address=TUIO_OBJECT25D)
        for val in [
                "set",
                int(self.session_id),
                int(self.class_id),
                float(x),
                float(y),
                float(z),
                float(self.angle),
                float(X),
                float(Y),
                float(Z),
                float(self.velocity_rotation),
                float(self.motion_acceleration),
                float(self.rotation_acceleration)
        ]:
            builder.add_arg(val)
        return builder.build()

class Cursor25D(Profile):
    """
    TUIO Cursor 2.5D Interactive Surface
    """
    def __init__(self, session_id):
        super().__init__(session_id)
        self.position               = (0, 0, 0)     # x,y,z
        self.velocity               = (0, 0, 0)     # X,Y,Z
        self.motion_acceleration    = 0             # m

    def get_message(self)-> OscMessage:
        """
        returns the OSC message of the Cursor with the TUIO spezification
        """
        x, y, z = self.position
        X, Y, Z = self.velocity
        builder = OscMessageBuilder(address=TUIO_CURSOR25D)
        for val in [
                "set",
                self.session_id,
                float(x),
                float(y),
                float(z),
                float(X),
                float(Y),
                float(Z),
                float(self.motion_acceleration)
        ]:
            builder.add_arg(val)
        return builder.build()

class Blob25D(Profile):
    # pylint: disable=too-many-instance-attributes
    """
    TUIO Blob 2.5D Interactive Surface
    """
    def __init__(self, session_id):
        super().__init__(session_id)
        self.position               = (0, 0, 0)         # x,y,z
        self.angle                  =  5                # a
        self.dimension              = (.1, .1)          # w, h
        self.area                   = 0.1               # f
        self.velocity               = (0.1, 0.1, 0.1)   # X,Y,Z
        self.velocity_rotation      = 0.1               # A
        self.motion_acceleration    = 0.1               # m
        self.rotation_acceleration  = 0.1               # r

    def get_message(self)-> OscMessage:
        """
        returns the OSC message of the Blob with the TUIO spezification
        """
        x, y, z = self.position
        X, Y, Z = self.velocity
        w, h = self.dimension
        builder = OscMessageBuilder(address=TUIO_BLOB25D)
        for val in [
                "set",
                self.session_id,
                float(x),
                float(y),
                float(z),
                float(self.angle),
                float(w),
                float(h),
                float(self.area),
                float(X),
                float(Y),
                float(Z),
                float(self.velocity_rotation),
                float(self.motion_acceleration),
                float(self.rotation_acceleration)
        ]:
            builder.add_arg(val)
        return builder.build()


class Object3D(Profile):
    """
    TUIO Object 3D Interactive Surface
    """
    def __init__(self, session_id):
        super().__init__(session_id)
        self.class_id               = -1            # i
        self.position               = (0, 0, 0)     # x,y,z
        self.angle                  = (0, 0, 0)     # a,b,c
        self.velocity               = (0, 0, 0)     # X,Y,Z
        self.velocity_rotation      = (0, 0, 0)     # A,B,C
        self.motion_acceleration    = 0             # m
        self.rotation_acceleration  = 0             # r

    def get_message(self) -> OscMessage:
        """
        returns the OSC message of the Object with the TUIO spezification
        """
        x, y, z = self.position
        X, Y, Z = self.velocity
        a, b, c = self.angle
        A, B, C = self.velocity_rotation
        builder = OscMessageBuilder(address=TUIO_OBJECT3D)
        for val in [
                "set",
                int(self.session_id),
                int(self.class_id),
                float(x),
                float(y),
                float(z),
                float(a),
                float(b),
                float(c),
                float(X),
                float(Y),
                float(Z),
                float(A),
                float(B),
                float(C),
                float(self.motion_acceleration),
                float(self.rotation_acceleration)
        ]:
            builder.add_arg(val)
        return builder.build()

class Cursor3D(Profile):
    """
    TUIO Cursor 3D Interactive Surface
    """
    def __init__(self, session_id):
        super().__init__(session_id)
        self.position               = (0, 0, 0)     # x,y,z
        self.velocity               = (0, 0, 0)     # X,Y,Z
        self.motion_acceleration    = 0             # m

    def get_message(self)-> OscMessage:
        """
        returns the OSC message of the Cursor with the TUIO spezification
        """
        x, y, z = self.position
        X, Y, Z = self.velocity
        builder = OscMessageBuilder(address=TUIO_CURSOR3D)
        for val in [
                "set",
                self.session_id,
                float(x),
                float(y),
                float(z),
                float(X),
                float(Y),
                float(Z),
                float(self.motion_acceleration)
        ]:
            builder.add_arg(val)
        return builder.build()

class Blob3D(Profile):
    # pylint: disable=too-many-instance-attributes
    """
    TUIO Blob 3D Interactive Surface
    """
    def __init__(self, session_id):
        super().__init__(session_id)
        self.position               = (0, 0, 0)         # x,y,z
        self.angle                  = (5, 5, 5)         # a,b,c
        self.dimension              = (.1, .1, .1)      # w,h,d
        self.volume                 = 0.1               # v
        self.velocity               = (0.1, 0.1, 0.1)   # X,Y,Z
        self.velocity_rotation      = (0.1, 0.1, 0.1)   # A,B,C
        self.motion_acceleration    = 0.1               # m
        self.rotation_acceleration  = 0.1               # r

    def get_message(self)-> OscMessage:
        """
        returns the OSC message of the Blob with the TUIO spezification
        """
        x, y, z = self.position
        a, b, c = self.angle
        X, Y, Z = self.velocity
        w, h, d = self.dimension
        A, B, C = self.velocity_rotation
        builder = OscMessageBuilder(address=TUIO_BLOB3D)
        for val in [
                "set",
                self.session_id,
                float(x),
                float(y),
                float(z),
                float(a),
                float(b),
                float(c),
                float(w),
                float(h),
                float(d),
                float(self.volume),
                float(X),
                float(Y),
                float(Z),
                float(A),
                float(B),
                float(C),
                float(self.motion_acceleration),
                float(self.rotation_acceleration)
        ]:
            builder.add_arg(val)
        return builder.build()