import SC
from P0 import compileString
from wasmtime import Store, Module, Func, Instance, FuncType, ValType

def scanString(src):
    SC.init(src); syms = [(SC.sym, SC.val)]
    while SC.sym != SC.EOF:
        SC.getSym()
        syms.append((SC.sym, SC.val))
    return syms

#### PART A
print("Part A:")
try:
    if scanString('5 ∉ {3}') == [(SC.NUMBER, 5), (SC.NOTELEMENT, 5), (SC.LBRACE, 5), (SC.NUMBER, 3), (SC.RBRACE, 3), (SC.EOF, 3)]:
        print("    Test Case 1 passed")
    else:
        print("    Test Case 1 failed")
except:
    print("    Test Case 1 failed")
try:
    if scanString('s ∖ t') == [(SC.IDENT, 's'), (SC.DIFFERENCE, 's'), (SC.IDENT, 't'), (SC.EOF, 't')]:
        print("    Test Case 2 passed")
    else:
        print("    Test Case 2 failed")
except:
    print("    Test Case 2 failed")


#### PART B
# Part B Test case 1
p0_program_B = """
program bitsets
  var a, b: set [1 .. 5]
  var c: boolean
    c := (2 ∈ a) or (2 ∉ a)
    a := ∁ a ∩ b ∖ a ∪ b
"""

accepted_output_part_b = """\
seq
  :=
    Var(name = c, lev = 1, tp = <class 'ST.Bool'>)
    or
      ∈
        Const(name = , tp = <class 'ST.Int'>, val = 2)
        Var(name = a, lev = 1, tp = Set(lower = 1, length = 5))
      ∉
        Const(name = , tp = <class 'ST.Int'>, val = 2)
        Var(name = a, lev = 1, tp = Set(lower = 1, length = 5))
  :=
    Var(name = a, lev = 1, tp = Set(lower = 1, length = 5))
    ∪
      ∖
        ∩
          ∁
            Var(name = a, lev = 1, tp = Set(lower = 1, length = 5))
          Var(name = b, lev = 1, tp = Set(lower = 1, length = 5))
        Var(name = a, lev = 1, tp = Set(lower = 1, length = 5))
      Var(name = b, lev = 1, tp = Set(lower = 1, length = 5))"""

print("Part B:")
try:
    if compileString(p0_program_B, target='ast') == accepted_output_part_b:
        print("    Test case 1 passed")
    else:
        print("    Test case 1 failed")
except:
    print("    Test case 1 failed (Fail to generate bitsets.ast)")

# Part B Test case 2
try:
    compileString("""
program bitsets
  var a, b: set [1 .. 5]
  var c: boolean
    c := a ∉ b
""", target='ast')
    print("   Test case 2 failed (no error was thrown)")
    raise
except Exception as e:
    if str(e) == "line 5 pos 14 bad type":
        print("    Test case 2 passed")
    else:
        print("    Test case 2 failed (unexpected error)")

# Part B Test case 3
try:
    compileString("""
program bitsets
  var a, b: set [1 .. 5]
  var c: boolean
    c := 2 ∉ c
""", target='ast')
    print("    Test case 3 failed (no error was thrown)")
    raise
except Exception as e:
    if str(e) == "line 5 pos 14 set expected":
        print("    Test case 3 passed")
    else:
        print("    Test case 3 failed (unexpected error)")

# Part B Test case 4
try:
    compileString("""
program bitsets
  var a, b: set [1 .. 5]
  var c: boolean
    a := c ∖ b
""", target='ast')
    print("   Test case 4 failed (no error was thrown)")
    raise
except Exception as e:
    if str(e) == "line 5 pos 14 bad type":
        print("    Test case 4 passed")
    else:
        print("    Test case 4 failed (unexpected error)")

# Part B Test case 5
try:
    compileString("""
program bitsets
  var a, b: set [1 .. 5]
    a := b ∖ 3
""", target='ast')
    print("    Test case 5 failed (no error was thrown)")
    raise
except Exception as e:
    if str(e) == "line 4 pos 14 bad type":
        print("    Test case 5 passed")
    else:
        print("    Test case 5 failed (unexpected error)")

### PART C
p0_program_C = """
program bitsets
  var a, b: set [1 .. 11]
  var i: integer
    i, a := 1, {3, 5, 7}
    if i ∉ a then a := a ∖ {7, 9}
    while i < 12 do
      if i ∈ a then write(i)
      i := i + 1
"""

accepted_output_part_c = """\
(module
(import "P0lib" "write" (func $write (param i32)))
(import "P0lib" "writeln" (func $writeln))
(import "P0lib" "read" (func $read (result i32)))
(global $_memsize (mut i32) i32.const 0)
(func $program
(local $a i32)
(local $b i32)
(local $i i32)
(local $0 i32)
i32.const 1
i32.const 3
local.set $0
i32.const 1
local.get $0
i32.shl
i32.const 5
local.set $0
i32.const 1
local.get $0
i32.shl
i32.or
i32.const 7
local.set $0
i32.const 1
local.get $0
i32.shl
i32.or
local.set $a
local.set $i
local.get $i
local.set $0
i32.const 1
local.get $0
i32.shl
local.get $a
i32.and
i32.eqz
if
i32.const 7
local.set $0
i32.const 1
local.get $0
i32.shl
i32.const 9
local.set $0
i32.const 1
local.get $0
i32.shl
i32.or
i32.const 0xffe
i32.xor
local.get $a
i32.and
local.set $a
end
loop
local.get $i
i32.const 12
i32.lt_s
if
local.get $i
local.set $0
i32.const 1
local.get $0
i32.shl
local.get $a
i32.and
if
local.get $i
call $write
end
local.get $i
i32.const 1
i32.add
local.set $i
br 1
end
end
)
(memory 1)
(start $program)
)"""

arr = []
def runwasmtime(watfile):
    def write_func(i: int):
        arr.append(i)

    def writeln_func():
        print()

    def read_func() -> int:
        return 0
    
    store = Store()
    module = Module.from_file(store.engine, watfile)

    write = Func(store, FuncType([ValType.i32()], []), write_func)
    writeln = Func(store, FuncType([], []), writeln_func)
    read = Func(store, FuncType([], [ValType.i32()]), read_func)

    Instance(store, module, [write, writeln, read])


print("Part C:")
success = False

try:
    compileString(p0_program_C, 'bitsets.wat', target = 'wat')
    success = True
except Exception as e:
    print("    Test case 1 failed (Failed to generate bitset.wat)")

if success:
    if open('bitsets.wat').read() == accepted_output_part_c:
        print("    Test case 1 passed")
    else:
        print("    Test case 1 failed")
    try:
        runwasmtime('bitsets.wat')
        if arr == [3, 5]:
            print("    Test case 2 passed")
        else:
            print("    Test case 2 failed") 
    except:
        print("    Test case 2 failed (Failed to run bitsets.wasm)")
       






