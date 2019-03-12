# Tale of Two Cities - 800

## Problem description

Looks like this book got a little messed up... there are some weird characters in there.  

Hint: hOpEfully thIS hint will help you!  A000788

## Solution

In the problem description, we were given a UTF-8 encoded text file copy of "A Tale of Two Cities" by Charles Dickens.  Immediately after opening the file, we notice a multitude of non-ASCII characters.  This powerfully suggests that the file was tampered with in multiple areas, and that we should figure out where exactly the author made those changes.  

Thankfully, the copy that the challenge writer used for "A Tale of Two Cities" was the Project Gutenberg version that could easily be found online.  We thus proceed to download the original "A Tale of Two Cities" text file, and compare the modified and original copies of the book.

```$ diff cities1.txt tale-of-two-cities.txt```

```
197c197
< up long rows of miscellaneous criminals; now, hanging a housebreaker on
---
> up long rows of miscellaneous criminals; n㐾 hanging a housebreaker on
311c311
< “I say a horse at a canter coming up, Joe.”
---
...
(Omitted)
...
< myself--timorous of highwaymen, and the prisoner has not a timorous
---
> myself--timorous of highwaymen,㑎d the prisoner has not a timorous
2979c2974
< “Have you no remembrance of the occasion?”
---
> “Have you no remem㑟Offset: 0x3400asion?”
```

A few things stand out here.  As aforementioned, we find many non-ASCII Chinese characters.  However, towards the end of the diff output, we see the following text: ```Offset: 0x3400```  Given the structure of the challenge, we then deduce that the non-ASCII characters could be in the 0x3400 ordinal range, so when subtracted from the given offset, would yield differences between 0 and 255 (i.e. in the ASCII character range).  We then proceed to collect all the non-ASCII Chinese characters from the diff output in the order they appear, and end up with ```㐾㐻㐌㐟㐀㐏㑖㐄㐓㐀㐴㐀㐄㐻㐉㐴㐷㐻㐾㐇㑎㑟```.  Subtracting 0x3400 from the ordinal values of the characters in the following manner, we end up with an list of differences:

```
chars = ["㐾", "㐻", "㐌", "㐟", "㐀", "㐏", "㑖", "㐄", "㐓", "㐀", "㐴", "㐀", "㐄", "㐻", "㐉", "㐴", "㐻", "㐾", "㐇", "㑎", "㑟"]
differences = [ord(i) - 0x3400 for i in chars]
print(differences)

//[62, 59, 12, 31, 0, 15, 86, 4, 19, 0, 52, 0, 4, 59, 9, 52, 55, 59, 62, 7, 78, 95]
```

Unfortunately, the list does not yield a readable flag when its entries are converted to ASCII, which means it is encoded using some other means.

This is where the hint comes in handy.  A quick Google search of "A000788" yields a result from the Online Encyclopedia of Integer Sequences (OEIS), which coincidentally happens to be the exact characters that are capitalized in the hint.  We learn that A000788 is the sequence representing the total number of 1's in binary expansions of 0, ..., n, so we write a function to calculate the nth value of said sequence.

```a000788 = lambda x: sum((bin(i+1).count("1") for i in range(x)))```

Since the hint involves sequences, which involve indexing, we then infer that the flag characters are indexed in some manner, most likely alphabetical order: (a = 0, b = 1, c = 2, ..., z = 25).  Additionally, we already know that the flag format is fixed as "utflag", which translates to ```[20, 19, 5, 11, 0, 6, 26]``` alphabetically indexed.  So in essence we can construct a known-plaintext attack between the 