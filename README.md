# friezy-peasy
Friezes generator given an image in Python.

## Usage
```console
usage: friezy_peasy [-h] image-path destiny-path pattern N

Frieze images generator

positional arguments:
  image-path    Image path which is used to generate the frieze.
  destiny-path  Destiny image path where the generated image will be saved.
  pattern       Frieze pattern group that will be used to generate the frieze.
  N             Number of times the resulting frieze image will be repeated.

options:
  -h, --help    show this help message and exit
  ```
  
  To generate a p2 (only halfturns) frieze with six repetitions of the motif:
  ```console
  python3 -m friezy_peasy img/image.jpg dest/result.jpg p2 6
  ```
