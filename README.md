# friezy-peasy
Python frieze generator.

## Set up
We recomment using a [venv](https://docs.python.org/3/library/venv.html)
environment to install the required packages and run the program. However,
this is choosen by the user.

First of all, some packages may need to be installed:

```bash
pip install -r requirements.txt
```

## Usage
The [Hermann-Mauguin notation](https://en.wikipedia.org/wiki/Hermann%E2%80%93Mauguin_notation)
is used to describe the [seven frieze groups](https://en.wikipedia.org/wiki/Frieze_group#Descriptions_of_the_seven_frieze_groups).

```console
usage: friezy_peasy [-h] image-path destiny-path pattern N

Frieze images generator

positional arguments:
  image-path    Path to the image used to generate the frieze.
  destiny-path  Path to the file where the generated image will be saved.
  pattern       IUCr frieze pattern group that will be used to generate the frieze.
  N             Number of times the resulting frieze image will be repeated.

options:
  -h, --help    show this help message and exit
  ```
  
  To generate a p2 (only halfturns) frieze with six repetitions of the motif:
  ```console
  python3 -m friezy_peasy img/image.jpg dest/result.jpg p2 6
  ```
