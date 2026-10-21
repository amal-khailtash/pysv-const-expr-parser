


// https://github.com/MikePopoloski/slang/blob/master/tests/unittests/ast/ExpressionTests.cpp

// i + 3
// 5'b0101 + 4'b1100
// 2'b1 & (((17'b101 >> 1'b1) - 4'b1100) == 21'b1)
// 2'b1 & (((17'b101 >> 1'b1) - 2.0) == 21'b1)
// 35'd123498234978234
// 0'd234
// 16777216'd1
// 16
// 'b ??0101?1
// 999999999999
// 'b _?1
// 'b3
// 'ox789
// 'd?
// 'd  z_
// 'd x1
// 'd a
// 'h g
// 3'h f
// 'd
// 9999e99999
// 9999e-99999
// 'h4194304f
// '{42, -39}
// '{999, '{1, 0}}
// '{1, 2, 3}
// '{2 {42}}
// '{2 {2}}
// '{2 {1, 2}}
// '{3 {2}}
// '{ c:9, default:2, int:42, int:37, d:-1 }
// '{ default:0, int:1, index - 1 + 1:-42 }
// 234.0567891ns
// '{1, 2, 3}
// '{3{A3}}
// '{A3, 4, 5, 6, 7, 8, 9}
// {A3, 4, 5, A3, 6}
// '{9{1}}
// {9{32'd1}}
// {A3, {4,5,6,7,8,9} }
// {A3, '{4,5,6,7,8,9} }
// {A3, 4, AI3'{5, 6, 7}, 8, 9}
// {4, 5}
// {4, 5, R1}
// '{}
// (3:4:5)

// https://github.com/chipsalliance/sv-tests/tree/master/tests/chapter-11

// simple
    // 11.4.11--simple_cond_op-sim.sv
    // assign b = (a) ? 0 : 1;

    // 11.4.12--simple_concat_op-sim.sv
    // assign c = {a, b};

    // 11.4.13--simple_set_member-sim.sv
    // assign b = (a inside {2, 3, 4, 5});

    // 11.4.14.3--simple_unpack_stream-sim.sv
    // assign d = {<<2 {a, b, c}};

    // 11.5.1--simple_idx_neg_part_select-sim.sv
    // assign b = a[15-:4];

    // 11.5.1--simple_idx_pos_part_select-sim.sv
    // assign b = a[0+:4];

    // 11.5.1--simple_idx_select-sim.sv
    // assign b = a[2];

    // 11.5.1--simple_non_idx_part_select-sim.sv
    // assign b = a[7:6];

    // 11.5.2--simple_array_addressing-sim.sv
    // assign b = mem[a];

// 11.3.5--expr_short_circuit.sv
// function int fun(logic a);  retunr a;  endfunction
// d = a && (b || fun(c));

// 11.3.6--assign_in_exp-sim.sv
// int a;
// int b; b = (a-=1);
// int c; c = a;
// (c-1)

// 11.3.6--assign_in_exp.sv
// int a;
// int b;
// b = (a-=1);

// 11.3.6--assign_in_expr-sim.sv
// int a;
// int b;
// int c;
// a = (b = (c = 5));

// 11.3.6--assign_in_expr.sv
// int a;
// int b;
// int c;
// a = (b = (c = 5));

// 11.3.6--assign_in_expr_inv.sv
// int a;
// int b;
// int c;
// a = b = c = 5;

// 11.3.6--assign_in_expression-sim.sv
// int a;
// int b;
// int c;
// c = a;
// b = (++a);
// (c+1)

// 11.3.6--assign_in_expression.sv
// int a;
// int b;
// b = (++a);

// 11.3.6--assignment_in_expression-sim.sv
// int a;
// int b;
// b = (++a);

// 11.3.6--assignment_in_expression.sv
// int a;
// int b;
// b = (a+=1);

// 11.3.6--two_assign_in_expr-sim.sv
// int a;
// int b;
// int c;
// int d;
// int e;
// c = a;
// e = b;
// d = ((b += (a+=1) + 1));
// (e+c+2)
// (e+c+2)

// 11.3.6--two_assign_in_expr.sv
// int a;
// int b;
// int c;
// int d;
// int e;
// c = a;
// e = b;
// d = ((b += (a+=1) + 1));

// 11.4.1--assignment-sim.sv
// reg [3:0] a;
// reg [3:0] b;
// a = 4'd12;
// b = 4'd5;
// a = b;

// 11.4.10--arith-shift-assignment-signed.sv
// logic signed [7:0] a, b, c;
// a = -120; // 128 + 8
// b = a;
// c = a;
// b <<<= 3;
// c >>>= 3;

// 11.4.10--arith-shift-assignment-unsigned.sv
// logic [7:0] a, b, c;
// a = 8;
// b = a;
// c = a;
// b <<<= 3;
// c >>>= 3;

// 11.4.10--arith-shift-signed.sv
// logic signed [7:0] a, b, c;
// a = -120; // 128 + 8
// b = (a <<< 3);
// c = (a >>> 3);

// 11.4.10--arith-shift-unsigned.sv
// logic [7:0] a, b, c;
// a = 8;
// b = (a <<< 3);
// c = (a >>> 3);

// 11.4.11--cond_op-sim.sv
// int a = 12;
// int b = 5;
// int c;
// c = (a > b) ? 11 : 13;

// 11.4.11--cond_op.sv
// int a = 12;
// int b = 5;
// int c;
// c = (a > b) ? 11 : 13;

// 11.4.12--concat_op-bit_select.sv
// bit [3:0] a;
// bit [7:0] b = 8'b10101100;
// bit [7:0] c = 8'b01010011;
// a = {b, c}[9:6];

// 11.4.12--concat_op-sim.sv
// bit [15:0] a;
// bit [7:0] b = 8'h89;
// bit [7:0] c = 8'h12;
// a = {b, c};

// 11.4.12--concat_op.sv
// bit [15:0] a;
// bit [7:0] b = 8'b10101100;
// bit [7:0] c = 8'b01010011;
// a = {b, c};

// 11.4.12.1--nested_repl_op-sim.sv
//

// 11.4.12.1--nested_repl_op.sv
//

// 11.4.12.1--repl_op-sim.sv
//

// 11.4.12.1--repl_op.sv
//

// 11.4.12.2--string_concat_op.sv
//

// 11.4.12.2--string_repl_op.sv
//

// 11.4.13--set_member-sim.sv
//

// 11.4.13--set_member.sv
//

// 11.4.14.1--stream_concat-sim.sv
//

// 11.4.14.1--stream_concat.sv
//

// 11.4.14.2--reorder_stream-sim.sv
//

// 11.4.14.2--reorder_stream.sv
//

// 11.4.14.2--reorder_stream_byte-sim.sv
//

// 11.4.14.2--reorder_stream_byte.sv
//

// 11.4.14.3--unpack_stream-sim.sv
//

// 11.4.14.3--unpack_stream.sv
//

// 11.4.14.3--unpack_stream_inv.sv
//

// 11.4.14.3--unpack_stream_pad-sim.sv
//

// 11.4.14.3--unpack_stream_pad.sv
//

// 11.4.14.4--dynamic_array_stream-sim.sv
//

// 11.4.14.4--dynamic_array_stream.sv
//

// 11.4.14.4--dynamic_array_stream_with.sv
//

// 11.4.2--unary_op_dec-sim.sv
//

// 11.4.2--unary_op_dec.sv
//

// 11.4.2--unary_op_inc-sim.sv
//

// 11.4.2--unary_op_inc.sv
//

// 11.4.5--equality-op.sv
//

// 11.5.1--idx_neg_part_select-sim.sv
//

// 11.5.1--idx_neg_part_select.sv
//

// 11.5.1--idx_pos_part_select-sim.sv
//

// 11.5.1--idx_pos_part_select.sv
//

// 11.5.1--idx_select-sim.sv
//

// 11.5.1--idx_select.sv
//

// 11.5.1--non_idx_part_select-sim.sv
//

// 11.5.1--non_idx_part_select.sv
//

// 11.5.2--array_addressing-sim.sv
//

// 11.5.2--array_addressing.sv
//

// 11.5.2--multi_dim_array_addressing-sim.sv
//

// 11.5.2--multi_dim_array_addressing.sv
//

// 11.7--signed_func-sim.sv
//

// 11.7--signed_func.sv
//

// 11.7--unsigned_func-sim.sv
//

// 11.7--unsigned_func.sv
//

// 11.9--tagged_union.sv
//

// 11.9--tagged_union_member_access-sim.sv
//

// 11.9--tagged_union_member_access.sv
//

// 11.9--tagged_union_member_access_inv.sv
//

// 11.10--string_bit_array-sim.sv
// bit [8*14:1] a;  a = "Test";

// 11.10--string_bit_array.sv
// bit [8*14:1] a;  a = "Test";

// 11.10.1--string_compare.sv
// bit [8*14:1] a;  a = "Test";
// bit [8*14:1] b;  b = "Test";

// 11.10.1--string_concat.sv
// bit [8*14:1] a;  a = "Test";
// bit [8*14:1] b;  b = "TEST";
// {a, b}

// 11.10.1--string_copy.sv
// bit [8*14:1] a;
// bit [8*14:1] b;
// a = "Test";  b = a;

// 11.10.3--empty_string-sim.sv
// bit [8*14:1] a;  a = "";

// 11.10.3--empty_string.sv
// bit [8*14:1] a;  a = "";

// 11.11--min_max_avg_delay.sv
// #(100:200:300)

// 11.12--let_construct.sv
// logic [3:0] a = 12;
// logic [3:0] b = 15;
// logic [3:0] c = 7;
// logic d;
// let op(x, y, z) = |((x | y) & z);
