reset
set terminal wxt
set key left
set title "Vergleich Sprite vs. Dirty Sprite"
set xlabel "Iterationen"
set ylabel "Sekunden"
set format x "%g "
set terminal pdfcairo color solid
set output "tbs1_05_100.pdf"
plot "perf0_05_100.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "sea-green" title "Sprite",\
     "perf1_05_100.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "red" title "DirtSprite"

set output "tbs1_05_4000.pdf"
plot "perf0_05_4000.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "sea-green" title "Sprite",\
     "perf1_05_4000.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "red" title "DirtSprite"

set output "tbs1_30_100.pdf"
plot "perf0_30_100.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "sea-green" title "Sprite",\
     "perf1_30_100.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "red" title "DirtSprite"

set output "tbs1_50_100.pdf"
plot "perf0_50_100.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "sea-green" title "Sprite",\
     "perf1_50_100.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "red" title "DirtSprite"

set output "tbs1_100_40.pdf"
plot "perf0_100_40.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "sea-green" title "Sprite",\
     "perf1_100_40.txt" using 1 "%lf" with lines smooth sbezier ls 1 lw 2 linecolor "red" title "DirtSprite"

set terminal wxt

# pause mouse
