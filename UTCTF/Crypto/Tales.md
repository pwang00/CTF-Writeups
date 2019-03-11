#Tale of Two Cities - 800

## Problem description

Looks like this book got a little messed up... there are some weird characters in there.  

Hint: hOpEfully thIS hint will help you!  A000788

## Solution

In the problem description, we were given a text file copy of "A Tale of Two Cities" by Charles Dickens.  Immediately after opening the file, we notice that some characters are not ASCII.  This powerfully suggests that the file was tampered with in multiple areas, and that we should figure out where exactly the author made those changes.  

Thankfully, the copy that the challenge writer used for "A Tale of Two Cities" was the Project Gutenberg version that could easily be found online.  We thus proceed to download the original "A Tale of Two Cities" text file, and compare the modified and original copies of the book.

```diff cities1.txt tale-of-two-cities.txt```



 
