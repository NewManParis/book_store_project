
AVAILABLE = 1
BORROWED = 2
ARCHIVED = 3

STATUS_CHOICES = (
    (AVAILABLE, ("Available to borrow")),
    (BORROWED, ("Borrowed by someone")),
    (ARCHIVED, ("Archived - not available anymore")),
)

OTH = "OTHER"
AST = "ASTRONOMY"
BIO = "BIOLOGY"
CHEM = "CHEMISTRY"
HIS = "HISTORY"
MED = "MEDECINE"
MAT = "MATHEMATICS"
PSY = "PSYCHOLOGY"

CATEGORY_CHOICES = (
    (OTH, ("Other")),
    (AST, ("Astronomy")),
    (BIO, ("Biology")),
    (CHEM, ("Chemistry")),
    (HIS, ("History")),
    (MED, ("Medecine")),
    (MAT, ("Mathematics")),
    (PSY, ("Psychology")),
)    