#coding=utf8

import csv

def geld(x):
  return '{:20,.2f}'.format(float(x)/100).replace(".",",") + " \euro{}"

with open('kategorien.csv', 'rb') as csvfile:
   reader = csv.reader(csvfile, delimiter=';', quotechar='"')
   kategorien = list(reader)

with open('bauteile.csv', 'rb') as csvfile:
   reader = csv.reader(csvfile, delimiter=';', quotechar='"')
   bauteile = list(reader)

with open('kaesten.csv', 'rb') as csvfile:
   reader = csv.reader(csvfile, delimiter=';', quotechar='"')
   kaesten = list(reader)
   
with open('output.tex', 'w') as texfile:
  texfile.write("\documentclass[a4paper,12pt,landscape]{report} "
                "\usepackage[official]{eurosym} "
                "\usepackage[utf8]{inputenc} \usepackage{ngerman} "
                "\usepackage[top=2cm, bottom=2cm, left=2cm, "
                "right=2cm,landscape]{geometry} \pagestyle{empty} "
                "\\begin{document}")
  for kasten in kaesten:
    texfile.write("\\begin{center} ")
    texfile.write("\huge \\textbf{Elektroniksortiment - Kasten %s} " % kasten[0])
    if kasten[1] == "1":
      texfile.write("\n\n\Large \\textbf{Preise sind verbindlich}")
    texfile.write("\end{center} \large")
    if kasten[2] == "1":
      texfile.write("\\begin{tabular}{|p{2.7cm}|p{2.7cm}|p{2.7cm}|"
                    "p{2.7cm}|p{2.7cm}|p{2.7cm}|p{2.7cm}|p{2.7cm}|}")
      bt = [bauteil for bauteil in bauteile if bauteil[0][0] == kasten[0]]
      for row in range(1,4):
        texfile.write(" \hline ")
        col = 1
        while col <= 8:
          if col != 1:
            texfile.write(" & ")
          bauteil = None
          for b in bt:
            if b[0] == kasten[0] + str(row) + str(col):
              bauteil = b
          if bauteil is not None:
            laenge = int(bauteil[1])
            if laenge == 1:
              texfile.write("\\textbf{%s} \\newline %s \\newline \\textbf{%s}" % (bauteil[0],bauteil[3],geld(bauteil[4])))
            else:
              texfile.write("\multicolumn{%s}{|p{%scm}|}{\\textbf{%s} \\newline %s \\newline \\textbf{%s}}" % (bauteil[1],str(laenge*3),bauteil[0],bauteil[3],geld(bauteil[4])))
            col = col + laenge
          else:
            texfile.write("\\textbf{%s} \\newline leer" % (kasten[0] + str(row) + str(col)))
            col = col + 1 
        texfile.write (" \\\\ ")
          
      texfile.write(" \hline ")
      bauteil = None
      for b in bt:
        if b[0] == kasten[0] + "41":
          bauteil = b
      if bauteil is not None:
        texfile.write("\multicolumn{3}{|p{8.1cm}|}{\\textbf{%s} \\newline %s \\newline \\textbf{%s}} &" % (bauteil[0],bauteil[3],geld(bauteil[4])))
      else:
        texfile.write("\multicolumn{3}{|p{8.1cm}|}{\\textbf{%s} \\newline leer} &" % (kasten[0] + "41"))
      texfile.write("\multicolumn{2}{|p{5.4cm}|}{} &")
      bauteil = None
      for b in bt:
        if b[0] == kasten[0] + "46":
          bauteil = b
      if bauteil is not None:
        texfile.write("\multicolumn{3}{|p{8.1cm}|}{\\textbf{%s} \\newline %s \\newline \\textbf{%s}} \\\\" % (bauteil[0],bauteil[3],geld(bauteil[4])))
      else:
        texfile.write("\multicolumn{3}{|p{8.1cm}|}{\\textbf{%s} \\newline leer} \\\\" % (kasten[0] + "46"))
      texfile.write(" \hline \end{tabular} ")
    else:
      texfile.write(" \\begin{tabular}{|p{8cm}|p{8cm}|p{8cm}|}")
      bt = [bauteil for bauteil in bauteile if bauteil[0][0] == kasten[0]]
      for i, bauteil in enumerate(bt):
        if i % 3 == 0:
          texfile.write(" \hline ")
        texfile.write("%s \\newline \\textbf{%s}" % (bauteil[3], geld(bauteil[4])))
        if i % 3 == 2:
          texfile.write(" \\\\ ")
        else:
          texfile.write(" & ")
      if len(bt) % 3 == 1:
        texfile.write (" & \\\\ ")
      elif len(bt) % 3 == 2:
        texfile.write (" \\\\ ")
      texfile.write(" \hline \end{tabular} ")
    texfile.write(" \\newpage ")
    
  for kategorie in kategorien:
    texfile.write("\\begin{center} ")
    texfile.write("\huge \\textbf{Elektroniksortiment} \n\n \\textbf{Kategorie %s}" % kategorie[1])
    texfile.write("\n\n\Large \\textbf{Mit * markierte Preise sind verbindlich}")
    texfile.write("\end{center} \large")
    texfile.write("\\begin{tabular}{|p{17cm}|p{3.5cm}|p{3.5cm}|} ")
    texfile.write("\hline \\textbf{Bezeichnung} & \\textbf{Ort} & \\textbf{Preis} \\\\")
    bt = [bauteil for bauteil in bauteile if bauteil[2] == kategorie[0]]
    for i,b in enumerate(bt):
      if i % 20 == 0 and i != 0:
        texfile.write(" \hline \end{tabular} \\newpage \\begin{tabular}{|p{17cm}|p{3.5cm}|p{3.5cm}|} ")
      texfile.write(" \hline ")
      k = [kasten for kasten in kaesten if b[0][0] == kasten[0]]
      if k[0][1] == "1":
        verbindlich = "*"
      else:
        verbindlich = ""
      texfile.write("%s & %s & %s \\\\ " % (b[3],b[0],geld(b[4])+verbindlich))
    texfile.write("\hline \end{tabular} \\newpage ")

  texfile.write("\end{document}")
