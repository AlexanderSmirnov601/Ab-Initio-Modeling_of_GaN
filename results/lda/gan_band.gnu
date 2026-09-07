reset session
set style data lines
set nokey
set xrange [0: 3.08885]
set yrange [  2.44039 : 25.90440]
set ylabel "Energy, eV"
set arrow 1 from  1.14996,   2.44039 to  1.14996,  25.90440 nohead
set arrow 2 from  2.47783,   2.44039 to  2.47783,  25.90440 nohead
set xtics ("G"  0.00000,"M|G"  1.14996,"K|G"  2.47783,"A"  3.08885)
set arrow 3 from 0, 10.77 to 3.08885, 10.77 nohead
set arrow 3 dt 2 lw 1.5 lc rgb "red"
set label "Fermi energy" at 0.5, 11.3 right offset -1, 0
plot "gan_band.dat" with lines lc rgb "black"
