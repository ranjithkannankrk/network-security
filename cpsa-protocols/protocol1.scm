;;; Used to generate output for inclusion in the primer.
;;; Use margin = 60 (-m 60) to generate the output.

(herald "Mutual Authentication"
  (comment "Project 1 - Protocol 1"))

(defprotocol ns basic
  (defrole init
    (vars (a b name) (r2 r1 data))
    (trace
	 (send a)
	 (recv r1)
     (send (enc r1 (ltk a b)))
	 (send r2)
	 (recv (enc r2 (ltk a b)))))
  (defrole resp
    (vars (a b name) (r1 r2 data))
    (trace
	 (recv a)
	 (send r1)
     (recv (enc r1 (ltk a b)))
	 (recv r2)
	 (send (enc r2 (ltk a b)))))
  (comment "Mutual Authentication"))
  

;;; The initiator point-of-view
(defskeleton ns
  (vars (a b name) (r2 data))
  (defstrand init 5 (a a) (b b) (r2 r2))
  (non-orig (ltk a b))
  (uniq-orig r2)
  (comment "Initiator point-of-view"))

;;; The Responder point-of-view
(defskeleton ns
  (vars (a b name) (r1 data))
  (defstrand resp 5 (a a) (b b) (r1 r1))
  (non-orig (ltk a b))
  (uniq-orig r1)
  (comment "Responder point-of-view"))
