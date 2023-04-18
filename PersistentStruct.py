# automatically generated by the FlatBuffers compiler, do not modify

# namespace: 

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class PersistentStruct(object):
    __slots__ = ['_tab']

    @classmethod
    def SizeOf(cls):
        return 24

    # PersistentStruct
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # PersistentStruct
    def SumLat(self): return self._tab.Get(flatbuffers.number_types.Float64Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))
    # PersistentStruct
    def SumLon(self): return self._tab.Get(flatbuffers.number_types.Float64Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(8))
    # PersistentStruct
    def Counter(self): return self._tab.Get(flatbuffers.number_types.Int32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(16))

def CreatePersistentStruct(builder, sumLat, sumLon, counter):
    builder.Prep(8, 24)
    builder.Pad(4)
    builder.PrependInt32(counter)
    builder.PrependFloat64(sumLon)
    builder.PrependFloat64(sumLat)
    return builder.Offset()