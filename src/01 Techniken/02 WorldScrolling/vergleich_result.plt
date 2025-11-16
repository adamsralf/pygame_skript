reset
set terminal wxt
set key left
set xlabel "Frames per second"
set ylabel "Tick (Bezier geglättet)"
#set format x "%g "
set terminal pdfcairo color solid

#set title "Performance mit und ohne Sichtbarkeitsprüfung"
set output "PerformaceMitOhnePrüfung.pdf"
set xrange [1:4000]
#set yrange [0.0:0.04]
plot "result.txt" using 1:2 with lines ls 1 lw 2 linecolor "sea-green" smooth bezier  title "ohne Sichtbarkeitsprüfung",\
     "result.txt" using 1:3 with lines ls 1 lw 2 linecolor "red" smooth bezier  title "mit Sichtbarkeitsprüfung"

pause mouse

set output


