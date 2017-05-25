RC_plots = veroC.png VeroR.png Hist.R.png Hist_C.png best_fit.png
Resultado_hw5.pdf : $(RC_plots)
	pdflatex Resultados_hw5.tex

$(RC_plots) : CircuitoRC.txt
	python circuitoRC.py

