// automatically generated by the FlatBuffers compiler, do not modify

package NamespaceC;

import java.nio.*;
import java.lang.*;
import java.util.*;
import com.google.flatbuffers.*;

@SuppressWarnings("unused")
public final class TableInC extends Table {
  public static void ValidateVersion() { Constants.FLATBUFFERS_23_3_3(); }
  public static TableInC getRootAsTableInC(ByteBuffer _bb) { return getRootAsTableInC(_bb, new TableInC()); }
  public static TableInC getRootAsTableInC(ByteBuffer _bb, TableInC obj) { _bb.order(ByteOrder.LITTLE_ENDIAN); return (obj.__assign(_bb.getInt(_bb.position()) + _bb.position(), _bb)); }
  public void __init(int _i, ByteBuffer _bb) { __reset(_i, _bb); }
  public TableInC __assign(int _i, ByteBuffer _bb) { __init(_i, _bb); return this; }

  public NamespaceA.TableInFirstNS referToA1() { return referToA1(new NamespaceA.TableInFirstNS()); }
  public NamespaceA.TableInFirstNS referToA1(NamespaceA.TableInFirstNS obj) { int o = __offset(4); return o != 0 ? obj.__assign(__indirect(o + bb_pos), bb) : null; }
  public NamespaceA.SecondTableInA referToA2() { return referToA2(new NamespaceA.SecondTableInA()); }
  public NamespaceA.SecondTableInA referToA2(NamespaceA.SecondTableInA obj) { int o = __offset(6); return o != 0 ? obj.__assign(__indirect(o + bb_pos), bb) : null; }

  public static int createTableInC(FlatBufferBuilder builder,
      int referToA1Offset,
      int referToA2Offset) {
    builder.startTable(2);
    TableInC.addReferToA2(builder, referToA2Offset);
    TableInC.addReferToA1(builder, referToA1Offset);
    return TableInC.endTableInC(builder);
  }

  public static void startTableInC(FlatBufferBuilder builder) { builder.startTable(2); }
  public static void addReferToA1(FlatBufferBuilder builder, int referToA1Offset) { builder.addOffset(0, referToA1Offset, 0); }
  public static void addReferToA2(FlatBufferBuilder builder, int referToA2Offset) { builder.addOffset(1, referToA2Offset, 0); }
  public static int endTableInC(FlatBufferBuilder builder) {
    int o = builder.endTable();
    return o;
  }

  public static final class Vector extends BaseVector {
    public Vector __assign(int _vector, int _element_size, ByteBuffer _bb) { __reset(_vector, _element_size, _bb); return this; }

    public TableInC get(int j) { return get(new TableInC(), j); }
    public TableInC get(TableInC obj, int j) {  return obj.__assign(__indirect(__element(j), bb), bb); }
  }
  public TableInCT unpack() {
    TableInCT _o = new TableInCT();
    unpackTo(_o);
    return _o;
  }
  public void unpackTo(TableInCT _o) {
    if (referToA1() != null) _o.setReferToA1(referToA1().unpack());
    else _o.setReferToA1(null);
    if (referToA2() != null) _o.setReferToA2(referToA2().unpack());
    else _o.setReferToA2(null);
  }
  public static int pack(FlatBufferBuilder builder, TableInCT _o) {
    if (_o == null) return 0;
    int _refer_to_a1 = _o.getReferToA1() == null ? 0 : NamespaceA.TableInFirstNS.pack(builder, _o.getReferToA1());
    int _refer_to_a2 = _o.getReferToA2() == null ? 0 : NamespaceA.SecondTableInA.pack(builder, _o.getReferToA2());
    return createTableInC(
      builder,
      _refer_to_a1,
      _refer_to_a2);
  }
}

