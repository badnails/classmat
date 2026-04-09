
#!start find_a_r
#!end accept
#!fill B

#found 'a', next find 'b'
find_a_r a d R find_b_r

#looking for 'a'
find_a_r b b R find_a_r
find_a_r c c R find_a_r
find_a_r d d R find_a_r

#no 'a' to the right of call point, look left
find_a_r B B L find_a_l




#found 'b', now look for 'c'
find_b_r b d R find_c_r

#looking for 'b'
find_b_r a a R find_b_r
find_b_r c c R find_b_r
find_b_r d d R find_b_r

#no 'b' to the right of call point, look left
find_b_r B B L find_b_l


#found 'c', look for new 'a'
find_c_r c d R find_a_r

#looking for 'c'
find_c_r a a R find_c_r
find_c_r b b R find_c_r
find_c_r d d R find_c_r

#no 'c' to the right of call point, look left
find_c_r B B L find_c_l


#no 'a' remaining. final check: if any other char left, we reject
find_a_l B B R exhausted_a

#business as usual
find_a_l a d R find_b_r

find_a_l b b L find_a_l
find_a_l c c L find_a_l
find_a_l d d L find_a_l


#no 'b' remaining. cannot match 'a'. reject
find_b_l B B N reject

#bau
find_b_l b d R find_c_r

find_b_l a a L find_b_l
find_b_l c c L find_b_l
find_b_l d d L find_b_l


#no 'c' remaining. reject
find_c_l B B N reject

find_c_l c d R find_a_r

find_c_l a a L find_c_l
find_c_l b b L find_c_l
find_c_l d d L find_c_l


#no 'a's left. reject if any other char found
exhausted_a b b N reject
exhausted_a c c N reject

#moving
exhausted_a d d R exhausted_a

#no 'a', 'b' or 'c' found. accept
exhausted_a B B N accept

























