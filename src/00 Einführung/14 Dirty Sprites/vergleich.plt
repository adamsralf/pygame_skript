reset
set terminal wxt
set key left
set xlabel "Iterationen"
set ylabel "Sekunden"
set format x "%g "
set terminal pdfcairo color solid

set title "Rechnervergleich ohne DirtySprite"
set output "ohne_05_100.pdf"
set xrange [0:400]
set yrange [0.0:0.04]
plot "tbs1/perf0_05_100.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "sea-green" title "TBS1",\
     "surface/perf0_05_100.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "red" title "Surface",\
     "zuhause/perf0_05_100.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "blue" title "Zuhause"

set title "Rechnervergleich mit DirtySprite"
set output "mit_05_100.pdf"
set xrange [0:400]
set yrange [0.0:0.04]
plot "tbs1/perf1_05_100.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "sea-green" title "TBS1",\
     "surface/perf1_05_100.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "red" title "Surface",\
     "zuhause/perf1_05_100.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "blue" title "Zuhause"

set title "Vergleich mit reduzierter fps"
set output "fps_05_4000.pdf"
set xrange [0:16000]
set yrange [0.0:0.06]
plot "perf0.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "sea-green" title "Sprite",\
     "perf1.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "red" title "DirtySprite"
set output
# pause mouse
