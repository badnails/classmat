#! start code
#! end done
#! fill B

code 1 a R one
code 0 b R zero
code c c R seek_end

one 1 1 R one
one 0 0 R one
one c c R one
one B 1 L seek_l_end

zero 1 1 R zero
zero 0 0 R zero
zero c c R zero
zero B 0 L seek_l_end

seek_l_end 0 0 L seek_l_end
seek_l_end 1 1 L seek_l_end
seek_l_end c c L seek_l_end
seek_l_end a 1 R code
seek_l_end b 0 R code

seek_end 0 0 R seek_end
seek_end 1 1 R seek_end
seek_end B B L sub

sub 1 0 N done
sub 0 1 L sub
sub c c N done
