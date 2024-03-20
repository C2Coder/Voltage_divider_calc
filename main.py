#!/bin/python3

import sys


class config:
    v_in = 8.5
    v_out_min = 2.9
    v_out_max = 3.1


class resistors:
    values = []

    out = []

    def format_value(num: float) -> str:
        int_part = int(num)

        decimal_part = 0

        suffix = ""
        if int_part >= 1_000_000:
            suffix = "M"
            decimal_part = num - (int(int_part / 1_000_000)) * 1_000_000
            int_part //= 1_000_000
        elif int_part >= 1_000:
            suffix = "k"
            decimal_part = num - (int(int_part / 1_000)) * 1_000
            int_part //= 1_000

        int_str = str(int_part)

        # Step 4: Convert the decimal part to a string and append the decimal point
        if decimal_part != 0:
            decimal_str = str(decimal_part).replace("0", "").replace(".", "")
            if decimal_str[-1] == ".":
                decimal_str = decimal_str[:-1]
            decimal_str = "." + decimal_str
        else:
            decimal_str = ""

        # Step 5: Combine the integer and decimal parts to get the final string
        return int_str + decimal_str + suffix

    def calculate():
        for r1 in resistors.values:
            for r2 in resistors.values:
                value = (r2 / (r1 + r2)) * config.v_in
                if value > config.v_out_min and value < config.v_out_max:
                    resistors.out.append([r1, r2, value])

    def print():
        tmp = []
        r1_len = 0
        r2_len = 0
        out_len = 0
        mA_len = 0

        for o in resistors.out:
            r1_len = max(len(resistors.format_value(o[0])), r1_len)
            r2_len = max(len(resistors.format_value(o[1])), r2_len)
            out_len = max(len(str(round(o[2], 3))), out_len)

        print("")
        print("  ┌──────────┐            ")
        print("  │         ┌┴┐           ")
        print("  │         │ │ R1        ")
        print("+_│_        └┬┘           ")
        print("  ┬  Vin     ├─────────○  ")
        print("  │         ┌┴┐        ↑  ")
        print("  │         │ │ R2    Vout")
        print("  │         └┬┘        ↓  ")
        print("  └──────────┴─────────○  ")                      



        print("")
        print(f"Vin = {config.v_in}V")
        print(f"Vout min = {config.v_out_min}V")
        print(f"Vout max = {config.v_out_max}V")
        print("")

        for o in resistors.out:

            r1 = resistors.format_value(o[0])
            r2 = resistors.format_value(o[1])

            out = str(round(o[2], 3))

            mA = round(round(config.v_in/(o[0] + o[1]), 9) * 1000, 3) # conv to mA

            print(
                f"R1 = {r1} {' ' * (r1_len - len(r1))} R2 = {r2} {' ' * (r2_len - len(r2))} -> Vout = {out}V {' ' * (out_len - len(str(out)))} I = {mA}mA"
            )
        print("")


class file:
    def read():
        lines = []
        with open("resistors.txt", "r") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip().lower()

            if "k" in line:
                value = float(line.replace("k", "")) * 1_000
            elif "m" in line:
                value = float(line.replace("m", "")) * 1_000_000
            else:
                value = float(line)

            if str(value) == str(int(value)):
                resistors.values.append(int(value))
            else:
                resistors.values.append(value)


file.read()
resistors.calculate()
resistors.print()
