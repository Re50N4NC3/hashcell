# hashcell
_Hashing function based on cellular automata_

This script can be used to inefficently hash provided string using one of the provided cellular automata rules. 

Arguments schema: 

`0: phrase, 1: salt, 2: grid size, 3: steps, 4: image draw, 5: image deletion, 6: bin save, 7: hash printing, 8: picked rule`

## How it works
### Initializatoin
Provided string is turned into binary representation, and all bits are joined together. After that, on the automata grid, the cells state is defined based on those bits. To make the output more unique and less prone to repetitions, the bits are laid out in spiral, counter clockwise fashion, starting from the middle of the grid.

Example starting point is shown below.

![grid starting point](https://raw.githubusercontent.com/Re50N4NC3/hashcell/main/initial_image.png)

Ones are alive cells (white), and zeros remain dead (black).

### Rules
There are few predefined automata rules, like gnarl, life without death, replicator, but they can be easily switched and added using S/B form, where S (survival neighbourhood amount) goes into `rules_survival` list and B (birth neighbourhood amount) into `rules_birth` list. Neighbourhood is checked based on Moore rules, so eight surrounding neighbours are checked. Rules are executed for defined number of steps, base value is 256 steps.

The best place to read about other possible rules is [Mirek Wójtowicz site](http://www.mirekw.com/ca/rullex_life.html), but those presented here work fine.
Obviously increasing size of the grid and amount of simulation steps decreases chance of hash repetition, with considerable increase in computation time, although even with grid of size 200x200 and 200 simulation steps, there were no repetitions found for 10000 tested strings.

### Output
After computing all the steps, the image is created, which is then transforemd, where, again as in the beggining, alive cells are considered as ones, and dead as zeros. It allows to generate new string based on created image.

Example output image is shown below. It was generated for string _password_, on 256x256 grid for 256 steps, using _replicator_ ruleset. More output images are in files.

![password example output](https://raw.githubusercontent.com/Re50N4NC3/hashcell/main/password_hash.png)


[And here is the output string which is way too long to put it here.](https://github.com/Re50N4NC3/hashcell/blob/main/example_hash.bin)

## Possible upgrades and changes
- [ ] Borders are skipped for simplicity, but the grid size maybe should/can be dynamic
- [ ] Make it more user friendly with possible options
- [ ] Shorten output string somehow
- [ ] Clean up code

It's not secure in any way, and I don't think it's capabe of hashing the tables properly, not to mention the passwords.
