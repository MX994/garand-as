# Garand Assembler

## Documentation

-   Simulator: [Garand](https://github.com/Tensor497/garand)
-   `graph.yml` contains decode schema for all supported instructions

## Build & Run

### Requirement

-   Python 3.11+
-   Pillow (for image pixel data conversion)

## Examples

### test.gar

Label & branch testing program.

### Fibb.gar

Generating Fibonacci sequence and write it to the memory.

### Chip

This program will perform memory copy. With graphic buffer turning on,
an image will be rendered.
First, generate image data by calling `img-mk.py chip.png chip.bin`,
then assemble `chip.gar`

### Exchange sort

`exchange_sort.data` is an example file of 100 random integers.
Assemble it into `exchange_sort.rdata`, and then assemble `exchange_sort.garand`.

<!-- `python gen_arr.py` will generate a new `exchange_sort.data`. You can specify the size with the `SIZE` variable. NOTE: If you change the size variable, you need to update the `R0` register in exchange_sort.garand -->

### Matrix multiply

`matrix_multiply.data` is an example file of 2 4x4 matrices.
Assemble it into `matrix_multiply.rdata`, and then assemble `matrix_multiply.garand`.
