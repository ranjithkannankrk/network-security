(herald "Mutual Authentication"
  (comment "Project 3 - Protocol 2"))

(defprotocol ns basic
  (defrole init
    (vars (a b name) (r2 r1 data))
    (trace
	 (send (cat a r2))
	 (recv (cat (enc r2 (ltk a b)) r1))
	 (send (enc r1 (ltk a b)))))
  (defrole resp
    (vars (a b name) (r1 r2 data))
    (trace
	 (recv (cat a r2))
	 (send (cat (enc r2 (ltk a b)) r1))
     (recv (enc r1 (ltk a b)))))
  (comment "Mutual Authentication"))
  
;;; The initiator point-of-view
(defskeleton ns
  (vars (a b name) (r2 data))
  (defstrand init 3 (a a) (b b) (r2 r2))
  (non-orig (ltk a b))
  (uniq-orig r2)
  (comment "initator point-of-view"))

;;; The Responder point-of-view
(defskeleton ns
  (vars (a b name) (r1 data))
  (defstrand resp 3 (a a) (b b) (r1 r1))
  (non-orig (ltk a b))
  (uniq-orig r1)
  (comment "reponder point-of-view"))
  
  
