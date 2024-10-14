---
title: Untitled

---

## For Image Password:
1. Since this was a lost progress of an image, that would mean we need to search for an image editor process to get the image data. We can use **volatility** to do that. 
2. We can utilize volatility plugin `pstree` to search for the process. In this case, it uses **GIMP** to edit the image.
3. After that, we can dump that process using plugin **memdump** to dump the process and then change the format of that dumped data into `.data`.
4. Now we can use GIMP to analyze that file as `raw data` and find the correct offset to get the password.

## For Text File Password:
1. First we need to find the PID of the notepad using `pslist` plugin, then we use volatility's `volshell` to analyze the heap segment data inside the process, since that's where unsaved notepad data is located.
2. Now open a new tab or window, and then using volatility again we dump the raw memory into a windows dump file using plugin `raw2dmp` and output it as `win3.dmp`. The reason we need to do this is because we can analyze the heap segment with more detail using **WinDBG**.
3. Opening the dump file, we first need to set our effective machine using command `.effmach amd64`.
4. After that we need to search for the process address of notepad.exe using command `!process 0 0 notepad.exe`. Then we need to set the process we want to analyze deeper using command `.process /r /p ffffe38d10685240`.
5. Now we can analyze the heap segment of this notepad.exe process. Using command `!heap -s -v -a` we need to search for heap with `user_flag` since that's where our data is saved.
6. Once we found the heap, copy the heap address and its size to volshell, and use command `db(0x000001a83de34860,0xd0)` to get the flag

Reference: https://infosecwriteups.com/extracting-an-unsaved-memory-content-by-walking-through-windows-heaps-but-how-6992589d872e
