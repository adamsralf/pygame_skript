reset
set terminal wxt
set key left
set xlabel "Frames per second"
set ylabel "Abweichung von Höhe 315"
#set format x "%g "
set terminal pdfcairo color solid

set title "Vergleich des Positionsfehlers (Median)"
set output "fehler_invers.pdf"
set xrange [10:600]
#set yrange [0.0:0.04]
plot "result_05f.txt" using 1:(315 - $13) with lines ls 1 lw 2 linecolor "sea-green" title "deltatime = 1/fps",\
     "result_05g.txt" using 1:(315 - $13) with lines ls 1 lw 2 linecolor "red" title "deltatime = clock.tick()"

pause mouse

set output "fehler_float.pdf"
set title "Vergleich des Positionsfehlers (Median) ohne und mit float"
plot "result_05g.txt" using 1:(315 - $13) with lines ls 1 lw 2 linecolor "sea-green" title "Version 1: rect.top",\
     "result_05h.txt" using 1:(315 - $13) with lines ls 1 lw 2 linecolor "red" title "Version 2: Vector2"

pause mouse

set output "fehler_funktion.pdf"
set xrange [10:600]
set title "Vergleich des Positionsfehlers (Median) mit unterschiedlicher Zeitmessung"
plot "result_05h.txt" using 1:(315 - $13) with lines ls 1 lw 2 linecolor "sea-green" title "clock.tick()",\
     "result_05i.txt" using 1:(315 - $13) with lines ls 1 lw 2 linecolor "red" title "time.time()"


set output

pause mouse
