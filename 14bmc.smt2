(set-logic QF_BV)

(declare-fun x () (_ BitVec 14))
(declare-fun y () (_ BitVec 14))
(assert (distinct (bvmul x y) (bvmul y x)))

(check-sat)
(exit)
