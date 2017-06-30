(TeX-add-style-hook
 "defense"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "11pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("fontenc" "T1") ("ucs" "mathletters") ("inputenc" "utf8x") ("enumitem" "inline") ("ulem" "normalem")))
   (add-to-list 'LaTeX-verbatim-environments-local "VerbatimOut")
   (add-to-list 'LaTeX-verbatim-environments-local "SaveVerbatim")
   (add-to-list 'LaTeX-verbatim-environments-local "LVerbatim*")
   (add-to-list 'LaTeX-verbatim-environments-local "LVerbatim")
   (add-to-list 'LaTeX-verbatim-environments-local "BVerbatim*")
   (add-to-list 'LaTeX-verbatim-environments-local "BVerbatim")
   (add-to-list 'LaTeX-verbatim-environments-local "Verbatim*")
   (add-to-list 'LaTeX-verbatim-environments-local "Verbatim")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "Verb")
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art11"
    "fontenc"
    "mathpazo"
    "graphicx"
    "caption"
    "adjustbox"
    "xcolor"
    "enumerate"
    "geometry"
    "amsmath"
    "amssymb"
    "textcomp"
    "upquote"
    "eurosym"
    "ucs"
    "inputenc"
    "fancyvrb"
    "grffile"
    "hyperref"
    "longtable"
    "booktabs"
    "enumitem"
    "ulem")
   (TeX-add-symbols
    '("WarningTok" 1)
    '("InformationTok" 1)
    '("AttributeTok" 1)
    '("PreprocessorTok" 1)
    '("ExtensionTok" 1)
    '("BuiltInTok" 1)
    '("OperatorTok" 1)
    '("ControlFlowTok" 1)
    '("VariableTok" 1)
    '("CommentVarTok" 1)
    '("AnnotationTok" 1)
    '("DocumentationTok" 1)
    '("ImportTok" 1)
    '("SpecialStringTok" 1)
    '("VerbatimStringTok" 1)
    '("SpecialCharTok" 1)
    '("ConstantTok" 1)
    '("NormalTok" 1)
    '("ErrorTok" 1)
    '("RegionMarkerTok" 1)
    '("FunctionTok" 1)
    '("AlertTok" 1)
    '("OtherTok" 1)
    '("CommentTok" 1)
    '("StringTok" 1)
    '("CharTok" 1)
    '("FloatTok" 1)
    '("BaseNTok" 1)
    '("DecValTok" 1)
    '("DataTypeTok" 1)
    '("KeywordTok" 1)
    "tightlist"
    "maxwidth"
    "Oldincludegraphics"
    "br"
    "gt"
    "lt"
    "PY"
    "PYZbs"
    "PYZus"
    "PYZob"
    "PYZcb"
    "PYZca"
    "PYZam"
    "PYZlt"
    "PYZgt"
    "PYZsh"
    "PYZpc"
    "PYZdl"
    "PYZhy"
    "PYZsq"
    "PYZdq"
    "PYZti"
    "PYZat"
    "PYZlb"
    "PYZrb")
   (LaTeX-add-labels
    "kids-have-skills"
    "is-that-really-a-thing"
    "history"
    "math"
    "in-the-space-of-the-big-five-survey")
   (LaTeX-add-environments
    "Shaded")
   (LaTeX-add-fancyvrb-environments
    '("Highlighting" "Verbatim"))
   (LaTeX-add-caption-DeclareCaptions
    '("\\DeclareCaptionLabelFormat{nolabel}" "LabelFormat" "nolabel"))
   (LaTeX-add-xcolor-definecolors
    "urlcolor"
    "linkcolor"
    "citecolor"
    "ansi-black"
    "ansi-black-intense"
    "ansi-red"
    "ansi-red-intense"
    "ansi-green"
    "ansi-green-intense"
    "ansi-yellow"
    "ansi-yellow-intense"
    "ansi-blue"
    "ansi-blue-intense"
    "ansi-magenta"
    "ansi-magenta-intense"
    "ansi-cyan"
    "ansi-cyan-intense"
    "ansi-white"
    "ansi-white-intense"
    "incolor"
    "outcolor"))
 :latex)

