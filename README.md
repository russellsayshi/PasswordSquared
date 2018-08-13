# PasswordSquared
Short little repo.

This is based upon the idea that if I want to store some passwords, all I need to do to make my encryption pretty much unbreakable is to make a master key equal to or greater than the length of all my passwords, and then I just essentially do a letter by letter caesar cipher with the password and master key (add their characters together w/ a mod).

It's deceptively simple, but it works wonders. This is just a short little tool to help me manage my passwords.

There's an example password which has been ciphered with the master key "password" if you want to download it and try it out.

Each password is stored as its own file on the filesystem. Never fear though, because it doesn't matter if someone grabs your password files, because they don't have the master key, so the information (besides password length) is mostly useless unless they are extremely clever. If you use a different master key for different passwords (perhaps based upon which letter they begin with) you can really throw 'em off.

However, if you use this, and something happens to your data/passwords, the liability is all yours. Use this at your own risk! I'm just putting this out there in case anyone finds it helpful.

To get help, just run `python ps.py -h`. Here's what it outputs:

```
usage: ps.py [-h] [--list] [--store TAG] [--get TAG] [--remove TAG] [--verify]
             [--printpass] [--printkey] [--override]

Stores and retrieves passwords through the use of a master key.

optional arguments:
  -h, --help            show this help message and exit
  --list, -l, --ls      Lists the tags of passwords stored
  --store TAG, -s TAG   Store password at tag.
  --get TAG, -g TAG     Get value from tag.
  --remove TAG, -r TAG  Removes item from database. Requires override argument
                        to be present as well.
  --verify, -v          Asks for the master key and/or password twice.
  --printpass           Prints password back after being asked for it.
  --printkey            Prints key back after being asked for it.
  --override, -f        Allows overwriting of preexisting data.
```
