reset
set terminal wxt
set key left
set title "Vergleich Sprite vs. Dirty Sprite"
set xlabel "Iterartionen"
set ylabel "Sekunden"
set format x "%g "
set terminal pdfcairo color solid
set output "surface_05_100.pdf"
set xrange [0:400]
set yrange [0.03:0.065]
plot "perf0_05_100.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "sea-green" title "Sprite",\
     "perf1_05_100.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "red" title "DirtSprite"

set output "surface_05_4000.pdf"
set xrange [0:16000]
set yrange [0.03:0.065]
plot "perf0_05_4000.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "sea-green" title "Sprite",\
     "perf1_05_4000.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "red" title "DirtSprite"

set output "surface_30_100.pdf"
set xrange [0:400]
set yrange [0.03:0.065]
plot "perf0_30_100.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "sea-green" title "Sprite",\
     "perf1_30_100.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "red" title "DirtSprite"

set output "surface_50_100.pdf"
set xrange [0:400]
set yrange [0.03:0.065]
plot "perf0_50_100.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "sea-green" title "Sprite",\
     "perf1_50_100.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "red" title "DirtSprite"

set output "surface_100_40.pdf"
set xrange [0:160]
set yrange [0.03:0.065]
plot "perf0_100_40.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "sea-green" title "Sprite",\
     "perf1_100_40.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "red" title "DirtSprite"

set terminal wxt
set output

# pause mouse
