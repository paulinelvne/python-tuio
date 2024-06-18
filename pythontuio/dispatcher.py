"""
classes to handle incoming osc messages
"""
from abc import ABC # abstract base class of python
from typing import List
from pythonosc.dispatcher import Dispatcher

from .tuio_profiles import Cursor, Blob, Object
from .tuio_profiles import Cursor25D, Blob25D, Object25D
from .tuio_profiles import Cursor3D, Blob3D, Object3D
from .tuio_profiles import TUIO_BLOB, TUIO_CURSOR, TUIO_OBJECT
from .tuio_profiles import TUIO_BLOB25D, TUIO_CURSOR25D, TUIO_OBJECT25D
from .tuio_profiles import TUIO_BLOB3D, TUIO_CURSOR3D, TUIO_OBJECT3D

from .const import TUIO_END,TUIO_ALIVE,TUIO_SET, TUIO_SOURCE



# pylint: disable=unnecessary-pass
class TuioListener(ABC):
    """
    Abstract TuioListener to define callbacks für the diffrent tuio events
    """
    def add_tuio_object(self, obj):
        """Abstract function to add a behavior for tuio add object event"""
        pass
    def update_tuio_object(self, obj):
        """Abstract function to add a behavior for tuio update object event"""
        pass
    def remove_tuio_object(self, obj):
        """Abstract function to add a behavior for tuio remove object event"""
        pass

    def add_tuio_cursor(self, cur):
        """Abstract function to add a behavior for tuio add cursor event"""
        pass
    def update_tuio_cursor(self, cur):
        """Abstract function to add a behavior for tuio update cursor event"""
        pass
    def remove_tuio_cursor(self, cur):
        """Abstract function to add a behavior for tuio remove cursor event"""
        pass

    def add_tuio_blob(self, blob):
        """Abstract function to add a behavior for tuio add blob event"""
        pass
    def update_tuio_blob(self, blob):
        """Abstract function to add a behavior for tuio update blob event"""
        pass
    def remove_tuio_blob(self, blob):
        """Abstract function to add a behavior for tuio remove blob event"""
        pass
    def refresh(self, time):
        """Abstract This callback method is invoked by the TuioClient
        to mark the end of a received TUIO message bundle."""
        pass
# pylint: enable=unnecessary-pass


class TuioDispatcher(Dispatcher):
    """
    class to hold Eventlistener and the TuioCursors, TuioBlobs, and TuioObjects
    """
    def __init__(self):
        super().__init__()
        self.cursors : List(Cursor) = []
        self.objects : List(Object) = []
        self.blobs   : List(Blob) = []
        self.cursors25D : List(Cursor25D) = []
        self.objects25D : List(Object25D) = []
        self.blobs25D   : List(Blob25D) = []
        self.cursors3D : List(Cursor3D) = []
        self.objects3D : List(Object3D) = []
        self.blobs3D   : List(Blob3D) = []
        self._listener : list = []
        self.map(f"{TUIO_CURSOR}*", self._cursor_handler)
        self.map(f"{TUIO_CURSOR25D}*", self._cursor_handler)
        self.map(f"{TUIO_CURSOR3D}*", self._cursor_handler)
        self.map(f"{TUIO_OBJECT}*", self._object_handler)
        self.map(f"{TUIO_OBJECT25D}*", self._object_handler)
        self.map(f"{TUIO_OBJECT3D}*", self._object_handler)
        self.map(f"{TUIO_BLOB}*", self._blob_handler)
        self.map(f"{TUIO_BLOB25D}*", self._blob_handler)
        self.map(f"{TUIO_BLOB3D}*", self._blob_handler)
        self.set_default_handler(self._default_handler)

        self._to_delete = []
        self._to_add    = []
        self._to_update = []

    def _cursor_handler(self, address, *args):
        """
        callback to convert OSC message into TUIO Cursor
        """
        if len(args) == 0 :
            raise Exception("TUIO message is Broken. No TUIO type specified")
        ttype = args[0]
        args = list(args[1:])
        if ttype == TUIO_SOURCE:
            pass
            #print(f"Message by {args} reveiced")
        elif ttype == TUIO_ALIVE :
            if(address == TUIO_CURSOR):
                cursors = self.cursors.copy()
                self.cursors = self._sort_matchs(cursors, args, Cursor)

            elif(address == TUIO_CURSOR25D):
                cursors25D = self.cursors25D.copy()
                self.cursors25D = self._sort_matchs(cursors25D, args, Cursor25D)

            elif(address == TUIO_CURSOR3D):
                cursors3D = self.cursors3D.copy()
                self.cursors3D = self._sort_matchs(cursors3D, args, Cursor3D)

        elif ttype == TUIO_SET:
            if(address == TUIO_CURSOR):
                print("Put value for Cursor")
                for cursor in self.cursors:
                    if cursor.session_id != args[0]:
                        continue
                    cursor.position = (args[1], args[2])
                    cursor.velocity = (args[3], args[4])
                    cursor.motion_acceleration = args[5]

            elif(address == TUIO_CURSOR25D):
                for cursor in self.cursors25D:
                    if cursor.session_id != args[0]:
                        continue
                    cursor.position = (args[1], args[2], args[3])
                    cursor.velocity = (args[4], args[5], args[6])
                    cursor.motion_acceleration = args[7]

            elif(address == TUIO_CURSOR3D):
                for cursor in self.cursors3D:
                    if cursor.session_id != args[0]:
                        continue
                    cursor.position = (args[1], args[2], args[3])
                    cursor.velocity = (args[4], args[5], args[6])
                    cursor.motion_acceleration = args[7]


        elif ttype == TUIO_END:
            self._call_listener()
            print(f"Bundle recived with {address}:{ttype} {args}")


        else:
            raise Exception("Broken TUIO Package")


    def _object_handler(self, address, *args):
        """
        callback to convert OSC message into TUIO Object
        """
        if len(args) == 0 :
            raise Exception("TUIO message is Broken. No TUIO type specified")
        ttype = args[0]
        args = list(args[1:])
        if ttype == TUIO_SOURCE:
            #print(f"Message by {args} reveiced")
            pass
        elif ttype == TUIO_ALIVE :
            if(address == TUIO_OBJECT):
                objects = self.objects.copy()
                self.objects = self._sort_matchs(objects, args, Object)
            
            elif(address == TUIO_OBJECT25D):
                objects25D = self.objects25D.copy()
                self.objects25D = self._sort_matchs(objects25D, args, Object25D)

            elif(address == TUIO_OBJECT3D):
                objects3D = self.objects3D.copy()
                self.objects3D = self._sort_matchs(objects3D, args, Object3D)

        elif ttype == TUIO_SET:
            if(address == TUIO_OBJECT) :
                for obj in self.objects:
                    if obj.session_id != args[0]:
                        continue
                    obj.class_id               = args[1]                # i
                    obj.position               = (args[2], args[3])     # x,y
                    obj.angle                  = args[4]                # a
                    obj.velocity               = (args[5], args[6])     # X,Y
                    obj.velocity_rotation      = args[7]                # A
                    obj.motion_acceleration    = args[8]                # m
                    obj.rotation_acceleration  = args[9]                # r

            elif(address == TUIO_OBJECT25D) :
                for obj in self.objects25D:
                    if obj.session_id != args[0]:
                        continue
                    obj.class_id               = args[1]                        # i
                    obj.position               = (args[2], args[3], args[4])    # x,y,z
                    obj.angle                  = args[5]                        # a
                    obj.velocity               = (args[6], args[7], args[8])    # X,Y,Z
                    obj.velocity_rotation      = args[9]                        # A
                    obj.motion_acceleration    = args[10]                       # m
                    obj.rotation_acceleration  = args[11]                       # r

            elif(address == TUIO_OBJECT3D) :
                for obj in self.objects3D:
                    if obj.session_id != args[0]:
                        continue
                    obj.class_id               = args[1]                        # i
                    obj.position               = (args[2], args[3], args[4])    # x,y,z
                    obj.angle                  = (args[5], args[6], args[7])    # a,b,c
                    obj.velocity               = (args[8], args[9], args[10])   # X,Y,Z
                    obj.velocity_rotation      = (args[11], args[12], args[13]) # A,B,C
                    obj.motion_acceleration    = args[14]                       # m
                    obj.rotation_acceleration  = args[15]                       # r


        elif ttype == TUIO_END:
            self._call_listener()
            print(f"Bundle recived with {address}:{ttype} {args}")
        else:
            raise Exception("Broken TUIO Package")

    def _blob_handler(self, address, *args):
        """
        callback to convert OSC message into TUIO Blob
         """

        if len(args) == 0 :
            raise Exception("TUIO message is Broken. No TUIO type specified")
        ttype = args[0]
        args = list(args[1:])
        if ttype == TUIO_SOURCE:
            pass
        elif ttype == TUIO_ALIVE :
            if(address == TUIO_BLOB):
                blobs = self.blobs.copy()
                self.blobs = self._sort_matchs(blobs, args, Blob)

            elif(address == TUIO_BLOB25D):
                blobs25D = self.blobs25D.copy()
                self.blobs25D = self._sort_matchs(blobs25D, args, Blob25D)

            elif(address == TUIO_BLOB3D):
                blobs3D = self.blobs3D.copy()
                self.blobs3D = self._sort_matchs(blobs3D, args, Blob3D)

        elif ttype == TUIO_SET:
            if(address == TUIO_BLOB):
                for blob in self.blobs:
                    if blob.session_id != args[0]:
                        continue
                    blob.position               = (args[1], args[2])     # x,y
                    blob.angle                  = args[3]                # a
                    blob.dimension              = (args[4], args[5])     # w, h
                    blob.area                   = args[6]                # f
                    blob.velocity               = (args[7], args[8])     # X,Y
                    blob.velocity_rotation      = args[9]                # A
                    blob.motion_acceleration    = args[10]               # m
                    blob.rotation_acceleration  = args[11]               # r

            elif(address == TUIO_BLOB25D):
                for blob in self.blobs25D:
                    if blob.session_id != args[0]:
                        continue
                    blob.position               = (args[1], args[2], args[3])       # x,y,z
                    blob.angle                  = args[4]                           # a
                    blob.dimension              = (args[5], args[6])                # w, h
                    blob.area                   = args[7]                           # f
                    blob.velocity               = (args[8], args[9], args[10])      # X,Y,Z
                    blob.velocity_rotation      = args[11]                          # A
                    blob.motion_acceleration    = args[12]                          # m
                    blob.rotation_acceleration  = args[13]                          # r

            elif(address == TUIO_BLOB3D):
                for blob in self.blobs3D:
                    if blob.session_id != args[0]:
                        continue
                    blob.position               = (args[1], args[2], args[3])       # x,y,z
                    blob.angle                  = (args[4], args[5], args[6])       # a,b,c
                    blob.dimension              = (args[7], args[8], args[9])       # w, h, d
                    blob.volume                 = args[10]                          # v
                    blob.velocity               = (args[11], args[12], args[13])    # X,Y,Z
                    blob.velocity_rotation      = (args[14], args[15], args[16])    # A,B,C
                    blob.motion_acceleration    = args[17]                          # m
                    blob.rotation_acceleration  = args[18]                          # r



        elif ttype == TUIO_END:
            self._call_listener()
            print(f"Bundle recived with {address}:{ttype} {args}")
        else:
            raise Exception("Broken TUIO Package")

    def _call_listener(self):    # pylint: disable=R0912 
        for listner in self._listener:
            for profile in self._to_add:
                if  isinstance(profile, Cursor) or  isinstance(profile, Cursor25D) or isinstance(profile, Cursor3D) :
                    listner.add_tuio_cursor(profile)
                elif isinstance(profile, Object) or isinstance(profile, Object25D) or isinstance(profile, Object3D) :
                    listner.add_tuio_object(profile)
                elif isinstance(profile, Blob) or isinstance(profile, Blob25D) or isinstance(profile, Blob3D) :
                    listner.add_tuio_blob(profile)

            for profile in self._to_update:
                if  isinstance(profile, Cursor) or  isinstance(profile, Cursor25D) or isinstance(profile, Cursor3D) :
                    listner.update_tuio_cursor(profile)
                elif isinstance(profile, Object) or isinstance(profile, Object25D) or isinstance(profile, Object3D) :
                    listner.update_tuio_object(profile)
                elif isinstance(profile, Blob) or isinstance(profile, Blob25D) or isinstance(profile, Blob3D) :
                    listner.update_tuio_blob(profile)


            for profile in self._to_delete:
                if  isinstance(profile, Cursor) or  isinstance(profile, Cursor25D) or isinstance(profile, Cursor3D) :
                    listner.remove_tuio_cursor(profile)
                elif isinstance(profile, Object) or isinstance(profile, Object25D) or isinstance(profile, Object3D) :
                    listner.remove_tuio_object(profile)
                elif isinstance(profile, Blob) or isinstance(profile, Blob25D) or isinstance(profile, Blob3D) :
                    listner.remove_tuio_blob(profile)

            listner.refresh(0) # TODO implement time conzept pylint
            self._to_add    = []
            self._to_update = []
            self._to_delete = []


    def add_listener(self, listener :TuioListener):
        """
        Adds the provided TuioListener to the list of registered TUIO event listeners
        """
        self._listener.append(listener)

    def remove_listener(self, listener :TuioListener):
        """
        Removes the provided TuioListener from the list of registered TUIO event listeners
        """
        self._listener.remove(listener)

    def remove_all_listeners(self):
        """
        Removes all provided TuioListeners from the list of registered TUIO event listeners
        """
        self._listener.clear()

    def _sort_matchs(self, profile_list, session_ids, Profile_type):
        """
        sort incoming session_ids into the lists and fill the listner stacks
        """
        new_profiles = []
        rest_profiles = profile_list.copy()
        rest_sessions = session_ids.copy()

        for session_id in session_ids:
            # search for profile
            for profile in profile_list:

                if profile.session_id == session_id:
                    new_profiles.append(profile)
                    self._to_update.append(profile)# add into event list update
                    rest_profiles.remove(profile)
                    rest_sessions.remove(session_id)

        for profile in rest_profiles:
            self._to_delete.append(profile)# add into event list delete

        for session_id in rest_sessions:
            profile = Profile_type(session_id)
            new_profiles.append(profile)
            self._to_add.append(profile)# add into event list add

        return new_profiles
