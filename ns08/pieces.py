"""NS08 Ember the Baby Dragon — round tables transcribed from the pattern."""
HEAD = [(1,"6 sc in MR",6),(2,"inc in each st around",12),(3,"[sc, inc] x6",18),
 (4,"[2 sc, inc] x6",24),(5,"[3 sc, inc] x6",30),(6,"[4 sc, inc] x6",36),
 (7,"sc in each st around",36),(8,"sc in each st around",36),(9,"[4 sc, dec] x6",30),
 (10,"[3 sc, dec] x6",24),(11,"[2 sc, dec] x6",18),(12,"[sc, dec] x6",12),(13,"dec x6",6)]
SNOUT = [(1,"6 sc in MR",6),(2,"[sc, inc] x3",9),(3,"[2 sc, inc] x3",12),
 (4,"sc in each st around",12),(5,"sc in each st around",12)]
BODY = [(1,"6 sc in MR",6),(2,"inc in each st around",12),(3,"[sc, inc] x6",18),
 (4,"[2 sc, inc] x6",24),(5,"[3 sc, inc] x6",30),(6,"sc in each st around",30),
 (7,"sc in each st around",30),(8,"sc in each st around",30),(9,"sc in each st around",30),
 (10,"[3 sc, dec] x6",24),(11,"sc in each st around",24),(12,"[2 sc, dec] x6",18),
 (13,"sc in each st around",18)]
LEG = [(1,"6 sc in MR",6),(2,"[sc, inc] x3",9)] + [(i,"sc in each st around",9) for i in range(3,9)]
TAIL = [(1,"4 sc in MR",4),(2,"sc in each st around",4),(3,"[sc, inc] x2",6),
 (4,"sc in each st around",6),(5,"sc in each st around",6),(6,"[2 sc, inc] x2",8),
 (7,"sc in each st around",8),(8,"sc in each st around",8),(9,"[3 sc, inc] x2",10),
 (10,"sc in each st around",10),(11,"sc in each st around",10),(12,"sc in each st around",10)]
HORN = [(1,"4 sc in MR",4),(2,"sc in each st around",4),(3,"[sc, inc] x2",6),
 (4,"sc in each st around",6),(5,"sc in each st around",6)]
ALL = {"Head":HEAD,"Snout":SNOUT,"Body":BODY,"Leg (x4)":LEG,"Tail":TAIL,"Horn (x2)":HORN}
